pipeline {
    agent { label 'worker1' }

    environment {
        DOCKER_IMAGE = 'belyaevedu/restapi-currency'
        DEPLOY_BRANCH = 'master'
    }

    stages {
        stage('Lint') {
            steps {
                echo 'linting Dockerfile with Hadolint'
                sh 'docker run --rm -i hadolint/hadolint < Dockerfile'
            }
        }
        stage('Build') {
            steps {
                echo 'building via docker compose'
                sh 'docker compose build'
            }
        }
        stage('Deploy') {
            when {
                branch DEPLOY_BRANCH
            }
            steps {
                echo 'pushing image to dockerhub'
                sh "docker push ${DOCKER_IMAGE}:latest"

                echo 'launching the same image'
                withCredentials([file(credentialsId: 'restapi-currency-env', variable: 'ENV_FILE')]) {
                    sh 'cp $ENV_FILE .env'
                    sh 'docker compose pull'
                    sh 'docker compose up -d'
                }
            }
        }
    }

    post {
        always {
            echo 'cleanup'

            sh "docker rmi ${DOCKER_IMAGE}:latest || true"

            cleanWs()
        }
    }
}
