pipeline {
  agent any

  options {
    timestamps()
    timeout(time: 30, unit: 'MINUTES')
  }

  environment {
    REPORT_ROOT = "reports"
    TEST_REPORT_DIR = "reports/tests"
    COVERAGE_HTML_DIR = "reports/coverage/html"
    PERFORMANCE_REPORT_DIR = "reports/performance"
    SECURITY_REPORT_DIR = "reports/security"
    
    SONAR_HOST_URL = "http://localhost:9000"
    DOCKER_IMAGE = "sistema-academico:ci"
    APP_CONTAINER = "sistema-academico-app"

    SONAR_SCANNER_HOME = tool 'SonarQube'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    
    stage('Pipeline Info') {
      steps {
        script {
          echo '<--Parameter Initialization-->'
          echo """
           Parameters:
            REPORT_ROOT = ${REPORT_ROOT}
            TEST_REPORT_DIR = ${TEST_REPORT_DIR}
            COVERAGE_HTML_DIR = ${COVERAGE_HTML_DIR}
            PERFORMANCE_REPORT_DIR = ${PERFORMANCE_REPORT_DIR}
            SECURITY_REPORT_DIR = ${SECURITY_REPORT_DIR}
            SONAR_HOST_URL = ${SONAR_HOST_URL}
            DOCKER_IMAGE = ${DOCKER_IMAGE}
            APP_CONTAINER = ${APP_CONTAINER}
          """ 
        }
      }
    }
    stage('Prepare Workspace') {
      steps {
        sh '''
          mkdir -p ${TEST_REPORT_DIR} ${COVERAGE_HTML_DIR} ${PERFORMANCE_REPORT_DIR} ${SECURITY_REPORT_DIR} reports/coverage
        '''
      }
    }

    stage('Build Docker Image') {
      steps {
        sh '''
          docker build -t ${DOCKER_IMAGE} .
        '''
      }
    }

    stage('Unit Tests & Coverage') {
      steps {
        sh '''
          docker run --rm \
            -v "$PWD":/app \
            -w /app \
            ${DOCKER_IMAGE} \
            sh -c "coverage run -m pytest tests/domain tests/application tests/infrastructure --junitxml=/app/${TEST_REPORT_DIR}/junit.xml && \
                   coverage xml -o /app/reports/coverage/coverage.xml && \
                   coverage html -d /app/${COVERAGE_HTML_DIR} && \
                   coverage report -m"
        '''
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: "${TEST_REPORT_DIR}/junit.xml"
          archiveArtifacts artifacts: "${TEST_REPORT_DIR}/**", fingerprint: true
          archiveArtifacts artifacts: "${COVERAGE_HTML_DIR}/**", fingerprint: true
        }
      }
    }

    stage('SonarQube Analysis') {
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
                  -Dsonar.sources=. \
                  -Dsonar.tests=tests \
                  -Dsonar.python.version=3.13 \
                  -Dsonar.python.coverage.reportPaths=reports/coverage/coverage.xml \
                  -Dsonar.python.xunit.reportPath=reports/tests/junit.xml \
                  -Dsonar.host.url=${SONAR_HOST_URL} \
                  -Dsonar.login=$SONAR_TOKEN

            '''
          }
        }
      }
    }

    stage ('Build') {
      steps {
        echo 'Build stage - no build steps for Python app. poetry'
      }
      post {
        always {
          echo 'Build stage completed.'
        }
      }
    }

    stage('Deploy') {
      steps {
        script {
          sh 'docker rm -f ${APP_CONTAINER} || true'
            sh '''
              docker run --rm \
                --env-file .env.example \
                ${DOCKER_IMAGE} \
                python scripts/seed_admin.py
            '''
          sh '''
            docker run -d --name ${APP_CONTAINER} -p 5000:5000 \
              --env-file .env.example \
              ${DOCKER_IMAGE} \
              gunicorn --bind 0.0.0.0:5000 run:app
          '''
          sh '''
            for i in {1..30}; do
              if curl -sSf http://localhost:5000/health > /dev/null; then
                exit 0
              fi
              sleep 1
            done
            echo 'Health check failed' >&2
            exit 1
          '''
          echo 'Application container started on http://localhost:5000'
        }
      }
      post {
        failure {
          sh 'docker logs ${APP_CONTAINER} > deploy.log || true'
          archiveArtifacts artifacts: 'deploy.log', fingerprint: true
        }
      }
    }

    stage('Performance (JMeter)') {
      steps {
        script {
          sh '''
            JMETER_PLAN=${JMETER_PLAN:-tests/performance/test-plan.jmx}

            if [ ! -f "$JMETER_PLAN" ]; then
              echo "Missing JMeter test plan at $JMETER_PLAN" >&2
              exit 1
            fi

            docker run --rm \
              --network=host \
              -v "$PWD":/workspace \
              -w /workspace \
              justb4/jmeter:5.6.3 \
              -n -t "$JMETER_PLAN" \
              -l ${PERFORMANCE_REPORT_DIR}/jmeter-results.jtl \
              -j ${PERFORMANCE_REPORT_DIR}/jmeter.log \
              -e -o ${PERFORMANCE_REPORT_DIR}/html
          '''
        }
      }
      post {
        always {
          archiveArtifacts artifacts: "${PERFORMANCE_REPORT_DIR}/**", fingerprint: true
        }
      }
    }
    stage('Setting up OWASP ZAP docker container') {
      steps {
        echo 'Pulling up last OWASP ZAP container --> Start'
        sh 'docker pull zaproxy/zap-stable'
        echo 'Pulling up last VMS container --> End'
        echo 'Starting container --> Start'
        sh 'docker run -dt --name owasp zaproxy/zap-stable /bin/bash '
        echo "Preparing ZAP working directory"
        script {
          sh '''
            docker exec owasp \
            mkdir /zap/wrk
          '''
        }
        echo "Scanning target on owasp container"
          sh """
        docker exec owasp \
        zap-full-scan.py \
        -t $target \
        -r report.html \
        -I
            """
      }
      post {
        always {
          echo 'Archiving OWASP ZAP report --> Start'
          sh 'docker cp owasp:/zap/report.html ${SECURITY_REPORT_DIR}/zap_report.html || true'
          echo 'Archiving OWASP ZAP report --> End'
          archiveArtifacts artifacts: "${SECURITY_REPORT_DIR}/zap_report.html", fingerprint: true
          echo 'Stopping and removing OWASP ZAP container --> Start'
          sh 'docker stop owasp || true'
          sh 'docker rm owasp || true'
          echo 'Stopping and removing OWASP ZAP container --> End'
        }
      }
    }

    stage('Functional Smoke Tests') {
      steps {
        script {
          sh 'curl -sSf http://localhost:5000/ || (echo "Home endpoint failed" && exit 1)'
          sh 'curl -sSf http://localhost:5000/health || (echo "Health endpoint failed" && exit 1)'
        }
      }
    }
  }

  post {
    always {
      sh 'docker stop ${APP_CONTAINER} || true'
      sh 'docker rm -f ${APP_CONTAINER} || true'
      echo 'Pipeline finished.'
    }
  }
}
