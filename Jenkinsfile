pipeline {
    agent any

    environment {
        DB_PASSWORD    = credentials('DB_PASSWORD')
        DB_USER        = credentials('DB_USER')
        DB_HOST        = credentials('DB_HOST')
        DB_NAME        = credentials('DB_NAME')
        SECRET_KEY     = credentials('SECRET_KEY')
        EMAIL_USER     = credentials('EMAIL_USER')
        EMAIL_PASSWORD = credentials('EMAIL_PASSWORD')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Debug Agent') {
            steps {
                sh 'echo "Running on agent: $(hostname)"'
                sh 'pwd'
                sh 'ls -la'
            }
        }

        stage('Build and Run Containers') {
            steps {
                script {
                    sh 'docker-compose down -v'
                    sh 'docker-compose up -d --build'
                }
            }
        }

        stage('Wait for Services') {
            steps {
                sh 'sleep 15'
            }
        }
    }

    post {
        always {
            sh 'docker-compose down -v'
        }
    }
}

