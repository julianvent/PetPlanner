pipeline {
    agent any

    environment {
        DB_PASSWORD = credentials('DB_PASSWORD')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
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
                // espera a que la base de datos y la app estén listas
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
