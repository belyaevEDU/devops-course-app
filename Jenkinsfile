library 'repeating-functions'

pipeline {
    agent { label 'staging' }

    environment {
        DOCKER_IMAGE = 'belyaevedu/restapi-currency'

        DEPLOY_BRANCH = 'master'
        DEPLOY_TAG = 'v*'

        SEMGREP_RULES_FOLDER = '.semgrep-rules'

        DEFAULT_DOCKER_RUN_PARAMETERS = "--rm -v ${env.WORKSPACE}:/workspace -w /workspace --user \$(id -u):\$(id -g)"

        TESTING_PORT = '8432'

        HADOLINT_VERSION = 'v2.14.0-alpine@sha256:158cd0184dcaa18bd8ec20b61f4c1cabdf8b32a592d062f57bdcb8e4c1d312e2'
        RUFF_VERSION = '0.15.20@sha256:03cc33c3f7f31ba53040fb1f1b8744a03a777033650f543d689d1ed98298f14b'
        SEMGREP_VERSION = '1.168.0@sha256:59fbed6127ea7c5dde3ba6a85142733bb20ea9aaa36120c953904f1539aaf66e'
        NEWMAN_VERSION = '6.1.3-alpine@sha256:d9b5e780ead0026bbb37f3759cd7b10fc8a88cd4030c8266a7c5e343d75a5198'
        TRIVY_VERSION = '0.71.2@sha256:f5d0e600ecda7449e2a9b272805aef698631d3bb3f3a739a750de2c6819acdc9'
    }

    stages {
        stage('Prepare') {
            steps {
                echo 'creating reports folder'
                sh "mkdir -p ${env.WORKSPACE}/reports"

                echo 'setting publish&deploy related variables'
                script {
                    env.PUBLISH_IMAGE_TAG = env.TAG_NAME ?: 'staging'
                }

                echo 'logging into dockerhub'
                script {
                    withCredentials([string(credentialsId: 'dockerhub-pat', variable: 'PAT')]) {
                        sh 'echo $PAT | docker login -u belyaevedu --password-stdin'
                    }
                }
            }
        }
        stage('Source code checks') {
            parallel {
                stage('Lint') {
                    steps {
                        echo 'linting Dockerfile with Hadolint'
                        sh """
                            docker run ${DEFAULT_DOCKER_RUN_PARAMETERS} \
                                hadolint/hadolint:${HADOLINT_VERSION} hadolint Dockerfile \
                                > ./reports/hadolint-report.txt
                        """

                        echo 'linting python source code with ruff'
                        sh """
                            docker run ${DEFAULT_DOCKER_RUN_PARAMETERS} \
                                ghcr.io/astral-sh/ruff:${RUFF_VERSION} check ./app \
                                --output-format=json \
                                > ./reports/ruff-report.json
                        """
                    }
                }
                stage('SAST') {
                    steps {
                        echo 'cloning semgrep\'s rules repo'
                        sh """
                            git clone --depth 1 --branch develop \
                                https://github.com/semgrep/semgrep-rules.git ${env.WORKSPACE}/${SEMGREP_RULES_FOLDER}
                        """

                        echo 'running SAST with semgrep & selected rules from the repo'
                        sh """
                            docker run ${DEFAULT_DOCKER_RUN_PARAMETERS} \
                                -e HOME=/tmp \
                                semgrep/semgrep:${SEMGREP_VERSION} semgrep \
                                --config ./${SEMGREP_RULES_FOLDER}/python/fastapi/security \
                                --config ./${SEMGREP_RULES_FOLDER}/python/requests \
                                --config ./${SEMGREP_RULES_FOLDER}/python/lang \
                                --config ./${SEMGREP_RULES_FOLDER}/python/correctness \
                                --sarif \
                                --output ./reports/semgrep-report.sarif \
                                --error \
                                --disable-version-check \
                                ./app
                        """
                    }
                }
            }
        }
        stage('Build') {
            when {
                anyOf {
                    changeRequest()
                    branch DEPLOY_BRANCH
                    tag DEPLOY_TAG
                }
            }
            steps {
                echo 'building via docker compose'
                sh 'docker compose build'
            }
        }
        stage('Test') {
            when {
                anyOf {
                    changeRequest()
                    branch DEPLOY_BRANCH
                    tag DEPLOY_TAG
                }
            }
            steps {
                echo 'starting a container with the image for testing'
                sh "echo PORT=${TESTING_PORT} > .env"
                sh 'PROMETHEUS_PORT=8001 docker compose up -d'

                healthCheckLoop("127.0.0.1:${TESTING_PORT}/info", 10, 3)

                echo 'testing with newman'
                sh """
                    docker run ${DEFAULT_DOCKER_RUN_PARAMETERS} \
                        --network host \
                        postman/newman:${NEWMAN_VERSION} run testing/postman_tests.json \
                        --env-var "PORT=${TESTING_PORT}" \
                        -r cli,json \
                        --reporter-json-export ./reports/newman-report.json
                """
            }
            post {
                always {
                    sh 'docker compose down -v'
                    sh 'rm .env'
                }
            }
        }
        stage('SCA') {
            when {
                anyOf {
                    changeRequest()
                    branch DEPLOY_BRANCH
                    tag DEPLOY_TAG
                }
            }
            steps {
                echo 'doing SCA with trivy'
                sh """
                    docker_gid=\$(stat -c %g /var/run/docker.sock)
                    docker run ${DEFAULT_DOCKER_RUN_PARAMETERS} \
                        --user \$(id -u):\$docker_gid \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        aquasec/trivy:${TRIVY_VERSION} \
                        --cache-dir ./trivy_cache \
                        image \
                        --exit-code 1 \
                        --severity HIGH,CRITICAL \
                        --output ./reports/trivy-report.txt \
                        ${DOCKER_IMAGE}:latest
                """
            }
        }
        stage('Publish') {
            when {
                anyOf {
                    branch DEPLOY_BRANCH
                    tag DEPLOY_TAG
                }
            }
            steps {
                echo "pushing image with tag ${env.PUBLISH_IMAGE_TAG}"
                sh "docker tag ${DOCKER_IMAGE}:latest ${DOCKER_IMAGE}:${env.PUBLISH_IMAGE_TAG}"
                sh "docker push ${DOCKER_IMAGE}:${env.PUBLISH_IMAGE_TAG}"
            }
        }
    }

    post {
        always {
            echo 'cleanup'

            sh "docker rmi ${DOCKER_IMAGE}:latest ${DOCKER_IMAGE}:${env.PUBLISH_IMAGE_TAG} || true"
            sh 'docker logout || true'

            archiveArtifacts artifacts: 'reports/*', fingerprint: true, allowEmptyArchive: true

            cleanWs()
        }
    }
}
