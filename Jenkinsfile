pipeline {
  agent any

  options {
    timestamps()
    timeout(time: 30, unit: 'MINUTES')
  }

  parameters {
    booleanParam(name: 'RELEASE_BUILD', defaultValue: false, description: 'Run poetry build to produce release artifacts')
  }

  environment {
    REPORT_ROOT = "reports"
    TEST_REPORT_DIR = "reports/tests"
    COVERAGE_HTML_DIR = "reports/coverage/html"
    PERFORMANCE_REPORT_DIR = "reports/performance"
    SECURITY_REPORT_DIR = "reports/security"
    ZAP_TARGET = "http://localhost:5000"
    
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
        echo 'Preparing workspace directories...'
        sh '''
          rm -rf ${REPORT_ROOT} || true
          mkdir -p ${TEST_REPORT_DIR} ${COVERAGE_HTML_DIR} ${PERFORMANCE_REPORT_DIR} ${SECURITY_REPORT_DIR} reports/coverage
        '''
      }
    }

    stage('Installing Dependencies') {
      steps {
        echo 'Installing dependencies from requirements.txt...'
        sh '''
          python -m venv venv
          . venv/bin/activate
          pip install -r requirements.txt
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
          . venv/bin/activate
          python -m coverage run --source=app -m pytest tests/domain tests/application tests/infrastructure --junitxml=${TEST_REPORT_DIR}/junit.xml && \
          python -m coverage xml -o reports/coverage/coverage.xml && \
          python -m coverage html -d ${COVERAGE_HTML_DIR} && \
          python -m coverage report -m

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
                  -Dsonar.sources=. \
                  -Dsonar.tests=tests \
                  -Dsonar.test.inclusions=**/tests/**/*.py \
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

    stage('Build') {
      when {
        expression { params.RELEASE_BUILD }
      }
      steps {
        echo 'Building the App package with Poetry...'
        sh '''
          . venv/bin/activate
          pip list
          pip install poetry
          poetry build
        '''
      }
      post {
        success {
          archiveArtifacts artifacts: 'dist/**', fingerprint: true
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
          echo 'Application container started on http://localhost:5000'
          echo 'Waiting for the application to be ready...'
          sleep 5
        }
      }
      post {
        failure {
          sh 'docker logs ${APP_CONTAINER} > deploy.log || true'
          archiveArtifacts artifacts: 'deploy.log', fingerprint: true
        }
      }
    }

    stage ('Performance Tests - Jmeter') {
      steps {
        echo 'Running performance tests with JMeter...'
        sh '''
          docker run --rm \
          -v $PWD/tests/performance:/tests \
          -v $PWD/${PERFORMANCE_REPORT_DIR}:/results \
          justb4/jmeter \
          -n -t /tests/TestRendimiento.jmx \
          -l /results/performance_results.jtl \
          -e -o /results/html_report
        '''
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
        -t ${ZAP_TARGET} \
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

    stage('Functional Tests - Selenium') {
      steps {
        echo 'Running functional tests with Selenium...'
        sh '''
          . venv/bin/activate
          pytest tests/functional --junitxml=${TEST_REPORT_DIR}/functional_junit.xml
        '''
      }
    }
  }

  post {
    always {
      echo 'Pipeline finished.'
      cleanWs()
    }
  }
}
