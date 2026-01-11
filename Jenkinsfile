pipeline {
  agent any

  parameters {
    booleanParam(name: 'RELEASE_BUILD', defaultValue: false, description: 'Construir el paquete de la aplicación con Poetry')
  }

  environment {
    BACKEND_DIR = "backend"
    FRONTEND_DIR = "frontend"

    REPORT_ROOT = "${BACKEND_DIR}/reports"
    TEST_REPORT_DIR = "${BACKEND_DIR}/reports/tests"
    COVERAGE_HTML_DIR = "${BACKEND_DIR}/reports/coverage/html"
    PERFORMANCE_REPORT_DIR = "${BACKEND_DIR}/reports/performance"
    SECURITY_REPORT_DIR = "${BACKEND_DIR}/reports/security"
    ZAP_TARGET = "http://localhost:5000"

    SONAR_HOST_URL = "http://localhost:9000"
    DOCKER_IMAGE = "sistema-academico:ci"
    APP_CONTAINER = "sistema-academico-app"
    FRONTEND_PREVIEW_CONTAINER = "frontend-preview"
    FRONTEND_PREVIEW_PORT = "4173"

    SELENIUM_REMOTE_URL = "http://localhost:4444/wd/hub"
    SELENIUM_CONTAINER_NAME = "selenium-chrome"

    RELEASE_DIR = "release"
  }

  stages {

    /* ------------------------------------------------------------------ */
    stage('Checkout') {
      agent any
      steps {
        checkout scm
      }
    }

    /* ------------------------------------------------------------------ */
    stage('Prepare Workspace') {
      agent { docker { image 'python:3.12-slim' } }
      steps {
        sh '''
          rm -rf ${REPORT_ROOT} || true
          mkdir -p ${TEST_REPORT_DIR} ${COVERAGE_HTML_DIR} ${PERFORMANCE_REPORT_DIR} ${SECURITY_REPORT_DIR} reports/coverage
          mv .env.example .env || true
        '''
      }
    }

    /* ------------------------------------------------------------------ */
    stage('Backend: Install Dependencies') {
      agent {
        docker {
          image 'python:3.12-slim'
          args '-u root --dns 8.8.8.8'
        }
      }
      steps {
        sh '''
          cd ${BACKEND_DIR}
          python -m venv venv
          . venv/bin/activate
          pip install --upgrade pip
          pip install poetry
          poetry lock
          poetry install --no-root --with dev
        '''
      }
    }

    /* ------------------------------------------------------------------ */
    stage('Frontend: Install & Build') {
      agent { docker { image 'node:24' } }
      steps {
        sh '''
          cd ${FRONTEND_DIR}
          npm i --no-cache
        '''
      }
    }

    /* ------------------------------------------------------------------ */
    stage('Build Python') {
      when {
        expression { return params.RELEASE_BUILD }
      }
      agent {
        docker {
          image 'python:3.12-slim'
          args '-u root --dns 8.8.8.8'
        }
      }
      steps {
        sh '''
          cd ${BACKEND_DIR}
          python -m venv venv
          . venv/bin/activate
          pip install --upgrade pip
          pip install poetry
          poetry lock
          poetry install --no-root --with dev
          poetry build
        '''
        echo "Build package completed."
      }
      post {
        success {
          archiveArtifacts artifacts: 'dist/**', fingerprint: true
        }
      }
    }

    stage('Build Frontend') {
      agent { docker { image 'node:24' } }
      steps {
        sh '''
          cd ${FRONTEND_DIR}
          npm run build
          ls -l dist
        '''
      }
      post {
        success {
          archiveArtifacts artifacts: 'frontend/dist/**', fingerprint: true
        }
      }
    }
    /* ------------------------------------------------------------------ */
    stage('Build Docker Image') {
      steps {
        sh 'docker build -t ${DOCKER_IMAGE} -f Dockerfile .'
      }
    }

    /* ------------------------------------------------------------------ */
    stage('Deploy Backend') {
      steps {
        sh 'docker rm -f ${APP_CONTAINER} || true'
        sh '''
          docker run --rm \
            ${DOCKER_IMAGE} \
            ls app
        '''
        sh '''
          docker run -d --name ${APP_CONTAINER} -p 5000:5000 \
            --env-file .env.example \
            ${DOCKER_IMAGE} \
            gunicorn --bind 0.0.0.0:5000 run:app
        '''
        sleep 5
      }
    }

    /* ------------------------------------------------------------------ */
    stage('Selenium Chrome Driver Container') {
      steps {
        sh '''
          docker rm -f ${SELENIUM_CONTAINER_NAME} || true
          docker run -d --name ${SELENIUM_CONTAINER_NAME} -p 4444:4444 selenium/standalone-chrome:latest
          for i in {1..20}; do
            if curl -fs ${SELENIUM_REMOTE_URL}/status >/dev/null 2>&1; then
              break
            fi
            sleep 1
          done
        '''
      }
    }

    /* ------------------------------------------------------------------ */
    stage('Start Frontend Preview') {
      agent none
      steps {
        sh '''
          docker rm -f ${FRONTEND_PREVIEW_CONTAINER} >/dev/null 2>&1 || true
          docker run -d --name ${FRONTEND_PREVIEW_CONTAINER} \
            -p ${FRONTEND_PREVIEW_PORT}:${FRONTEND_PREVIEW_PORT} \
            -v ${WORKSPACE}/${FRONTEND_DIR}:/app \
            -w /app \
            node:24 \
            sh -c "npm run preview"
            sleep 10
        '''
      }
    }

    /* ------------------------------------------------------------------ */
    stage('Backend: Unit Tests, coverage and functional tests') {
      agent {
        docker {
          image 'python:3.12-slim'
          args '-u root --dns 8.8.8.8 --network host'
        }
      }
      steps {
        echo "Loading test data"
        sh '''
          cd ${BACKEND_DIR}
          . venv/bin/activate
          PYTHONPATH=$PWD python scripts/test_data.py
        '''
        echo "Running unit tests with coverage and functional tests"
        sh '''
          cd ${BACKEND_DIR}
          . venv/bin/activate
          pytest --junitxml=reports/tests/junit.xml --cov=app --cov-report=xml:reports/coverage/coverage.xml tests || true
        '''
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: "${TEST_REPORT_DIR}/junit.xml"
          archiveArtifacts artifacts: "${TEST_REPORT_DIR}/**", fingerprint: true
        }
      }
    }

    /* ------------------------------------------------------------------ */
    stage('SonarQube Static Analysis') {
      agent { docker { image 'sonarsource/sonar-scanner-cli' } }
      steps {
        withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
          sh '''
            sonar-scanner \
              -Dsonar.projectKey=SisAcad\
              -Dsonar.projectName="Sistema Académico" \
              -Dsonar.sources=backend/app,frontend/src,frontend/package.json,Dockerfile,templates,static \
              -Dsonar.tests=tests \
              -Dsonar.python.coverage.reportPaths=backend/reports/coverage/coverage.xml,backend/reports/junit.xml \
              -Dsonar.host.url=${SONAR_HOST_URL} \
              -Dsonar.login=$SONAR_TOKEN
          '''
        }
      }
    }

    /* ------------------------------------------------------------------ */
    stage('Performance Tests - JMeter') {
      agent { docker { image 'justb4/jmeter' } }
      steps {
        sh '''
          mkdir -p ${PERFORMANCE_REPORT_DIR}
          jmeter \
            -n \
            -t tests/performance/TestRendimiento.jmx \
            -l ${PERFORMANCE_REPORT_DIR}/performance_results.jtl \
            -e \
            -o ${PERFORMANCE_REPORT_DIR}/html_report
        '''
      }
      post {
        always {
          archiveArtifacts artifacts: "${PERFORMANCE_REPORT_DIR}/**", fingerprint: true
        }
      }
    }

    /* ------------------------------------------------------------------ */
    stage('OWASP ZAP Security Scan') {
      agent {
        docker {
          image 'zaproxy/zap-stable'
          args '--network host'
        }
      }
      steps {
        sh '''
          mkdir -p ${SECURITY_REPORT_DIR}
          zap-full-scan.py \
            -t ${ZAP_TARGET} \
            -r ${SECURITY_REPORT_DIR}/zap_report.html \
            -I
        '''
      }
      post {
        always {
          archiveArtifacts artifacts: "${SECURITY_REPORT_DIR}/zap_report.html", fingerprint: true
        }
      }
    }


  }

  post {
    always {
      cleanWs()
    }
  }
}
