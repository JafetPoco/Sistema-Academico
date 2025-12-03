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
    LINT_REPORT_DIR = "reports/lint"
    SECURITY_REPORT_DIR = "reports/security"
    SONAR_HOST_URL = "http://localhost:9000"  // Replace with your SonarQube server URL
    SONAR_TOKEN = credentials('sonar-token')  // Replace with your Jenkins credential ID for SonarQube token
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
        script {
          echo "Branch: ${env.BRANCH_NAME ?: 'unknown'}"
        }
      }
    }

    stage('Setup Python') {
      steps {
        sh '''
          python3 -m venv venv
          . venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
          mkdir -p ${TEST_REPORT_DIR} ${COVERAGE_HTML_DIR} ${LINT_REPORT_DIR} ${SECURITY_REPORT_DIR}
        '''
      }
    }

    stage('Unit Tests & Coverage') {
      steps {
        sh '''
          . venv/bin/activate
          coverage run -m pytest tests/domain tests/application tests/infrastructure --junitxml=${TEST_REPORT_DIR}/junit.xml
          coverage xml -o reports/coverage/coverage.xml
          coverage html -d ${COVERAGE_HTML_DIR}
          coverage report -m
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
          
          withSonarQubeEnv('SonarQube') { 
            sh 'sonar-scanner -Dsonar.login=${SONAR_TOKEN}'
          }
        }
      }
    }

    stage ('Build') {
      steps {
        echo 'Build stage - no build steps for Python app.'
      }
      post {
        always {
          echo 'Build stage completed.'
        }
      }
    }

    stage('Deploy') {
      when { branch 'main' }
      steps {
        script {
          // Local developer deploy: start the app using Python run.py on localhost:8000
          // Uses the venv created earlier; each developer can run on their own Jenkins machine
          sh '''
            . venv/bin/activate
            nohup python run.py > deploy.log 2>&1 & echo $! > deploy.pid
          '''
          echo 'Application (run.py) started locally on http://localhost:8000'
        }
      }
      post {
        always {
          // Keep PID file for later stages to stop the app after tests
          archiveArtifacts artifacts: 'deploy.log', fingerprint: true
        }
      }
    }

    stage('ZAP Security Scan (Baseline)') {
      steps {
        script {
          sleep time: 5, unit: 'SECONDS'

          zap toolName: 'ZAP_DEFAULT', 
              session: '', 
              includePaths: [], 
              excludePaths: [], 
              targetUrl: 'http://localhost:8000', 
              failBuild: false, 
              generateReports: true, 
              reportDir: "${SECURITY_REPORT_DIR}", 
              attackMode: false, 
              quickScan: true
        }
      }
      post {
        always {
          archiveArtifacts artifacts: "${SECURITY_REPORT_DIR}/**", fingerprint: true
        }
      }
    }

    // Optional functional smoke tests against the running app
    stage('Functional Smoke Tests') {
      steps {
        script {
          // Simple curl checks as placeholders; replace with your real test harness
          sh 'curl -sSf http://localhost:8000/ || (echo "Home endpoint failed" && exit 1)'
          sh 'curl -sSf http://localhost:8000/health || (echo "Health endpoint failed" && exit 1)'
        }
      }
    }

    // Final cleanup: stop the app once all tests are complete
    stage('Stop App') {
      when { branch 'main' }
      steps {
        sh 'test -f deploy.pid && kill $(cat deploy.pid) || true'
      }
    }
  }

  post {
    always {
      echo 'Pipeline finished.'
    }
  }
}
