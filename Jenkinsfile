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
    FRONTEND_BASE_URL = "http://localhost:${FRONTEND_PREVIEW_PORT}"

    SELENIUM_REMOTE_URL = "http://localhost:4444/wd/hub"
    SELENIUM_CONTAINER_NAME = "selenium-chrome"

    RELEASE_DIR = "release"
  }

  stages {

    /* ------------------------------------------------------------------ */
    stage('Checkout') {
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
    stage('Backend: Install') {
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
    stage('Frontend: Install') {
      agent { docker { image 'node:24' } }
      steps {
        sh '''
          cd ${FRONTEND_DIR}
          mkdir -p ${WORKSPACE}/.npm-cache
          export npm_config_cache=${WORKSPACE}/.npm-cache
          npm install --no-audit --no-fund
        '''
      }
    }

    /* ------------------------------------------------------------------ */
    stage('Build Backend') {
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
    /* ------------------------------------------------------------------ */

    stage('Build Frontend') {
      agent { 
        docker { 
          image 'node:24'
          args '-u root'
        } 
      }
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
      agent any
      steps {
        sh 'docker build -t ${DOCKER_IMAGE} -f Dockerfile .'
      }
    }

    /* ------------------------------------------------------------------ */
    stage('Selenium Chrome Driver Container') {
      steps {
        sh '''
          docker rm -f ${SELENIUM_CONTAINER_NAME} || true
          docker run -d --name ${SELENIUM_CONTAINER_NAME} --network host selenium/standalone-chrome:latest
          for i in {1..20}; do
            if curl -fs ${SELENIUM_REMOTE_URL}/status >/dev/null 2>&1; then
              echo "Selenium hub is up"
              break
            fi
            sleep 1
          done
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
        echo "Deploying frontend"
        sh '''
          apt-get update
          apt-get install -y nodejs npm curl
          cd ${FRONTEND_DIR}
          npm install --no-audit --no-fund
          npm run build
          npm run preview -- --host 0.0.0.0 --port ${FRONTEND_PREVIEW_PORT} &
          cd -
          echo "Loading test data"
          cd ${BACKEND_DIR}
          . venv/bin/activate
          PYTHONPATH=$PWD python scripts/test_data.py
          export FRONTEND_BASE_URL=${FRONTEND_BASE_URL}
          python run.py &
          sleep 5
          echo "Running tests"
          pytest --junitxml=reports/tests/junit.xml --cov=app --cov-report=xml:reports/coverage/coverage.xml tests || true
        '''
      }
      post {
        success {
          junit allowEmptyResults: true, testResults: "${TEST_REPORT_DIR}/junit.xml"
          archiveArtifacts artifacts: "${TEST_REPORT_DIR}/**", fingerprint: true
        }
      }
    }
    /* ------------------------------------------------------------------ */

    stage('SonarQube Static Analysis') {
      steps {
        script {
          sh 'curl -f ${SONAR_HOST_URL}/api/system/status || (echo "SonarQube server not running" && exit 1)'

          withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
            sh '''
              docker run --rm \
                --name sonar-scanner \
                --network=host \
                -v "$PWD":/usr/src \
                -w /usr/src \
                sonarsource/sonar-scanner-cli:latest \
                sonar-scanner \
                  -Dsonar.projectKey=sys:acad \
                  -Dsonar.projectName="Sistema Académico" \
                  -Dsonar.sources=backend/app,frontend/src,frontend/package.json,Dockerfile \
                  -Dsonar.python.version=3.12 \
                  -Dsonar.python.coverage.reportPaths=reports/coverage/coverage.xml \
                  -Dsonar.python.xunit.reportPath=reports/tests/junit.xml \
                  -Dsonar.host.url=${SONAR_HOST_URL} \
                  -Dsonar.token=$SONAR_TOKEN

            '''
          }
        }
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

    stage('Performance Tests - JMeter') {
      steps {
        sh '''
          mkdir -p ${PERFORMANCE_REPORT_DIR}/html_report
          
          docker run --rm \
            -u $(id -u):$(id -g) \
            -v ${WORKSPACE}:/backend \
            -w /backend \
            justb4/jmeter \
            -n \
            -t backend/tests/performance/TestRendimiento.jmx \
            -l backend/reports/performance/performance_results.jtl \
            -e \
            -o ${PERFORMANCE_REPORT_DIR}/html_report
        '''
      }
      post {
        always {
          archiveArtifacts artifacts: "${PERFORMANCE_REPORT_DIR}/**", allowEmptyArchive: true
        }
      }
    }
    /* ------------------------------------------------------------------ */
    stage('OWASP ZAP Security Scan') {
      steps {
        sh '''
          mkdir -p ${SECURITY_REPORT_DIR}
          
          docker run --rm \
            --network host \
            -u 0 \
            -v ${WORKSPACE}/${SECURITY_REPORT_DIR}:/zap/wrk/:rw \
            zaproxy/zap-stable \
            zap-full-scan.py \
              -t ${ZAP_TARGET} \
              -r zap_report.html \
              -I
        '''
      }
      post {
        success {
          archiveArtifacts artifacts: "${SECURITY_REPORT_DIR}/zap_report.html", allowEmptyArchive: true
        }
      }
    }


  }

  post {
    always {
      cleanWs()
        script {
          sh 'docker rm -f ${APP_CONTAINER} || true'
          sh 'docker rm -f ${SELENIUM_CONTAINER_NAME} || true'
          sh 'docker rm -f ${FRONTEND_PREVIEW_CONTAINER} || true'
          sh 'pkill gunicorn || true'
        }
    }
  }
}
