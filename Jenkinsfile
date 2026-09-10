pipeline {
    agent any

    environment {
        DOCKER_USER = 'shaffat01' 
        APP_NAME    = 'web-app-2'
        IMAGE_TAG   = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
        FULL_IMAGE  = "${DOCKER_USER}/${APP_NAME}"
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Build & Test') {
            steps {
                sh "docker build -t ${FULL_IMAGE}:${IMAGE_TAG} ."
                sh "docker run --rm ${FULL_IMAGE}:${IMAGE_TAG} pytest --version"
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh "echo \$PASS | docker login -u \$USER --password-stdin"
                    sh "docker push ${FULL_IMAGE}:${IMAGE_TAG}"
                }
            }
        }

        stage('Deploy via Ansible') {
            steps {
                script {
                    // Branch অনুযায়ী Port নির্ধারণ
                    def DEPLOY_PORT = (env.BRANCH_NAME == 'main') ? '8001' : '9001'
                    
                    echo "🚀 Triggering Ansible for ${env.BRANCH_NAME} on Port ${DEPLOY_PORT}"
                    
                    sh """
                    ansible-playbook -i localhost, -c local /home/jenkins/ansible-master/deploy.yml \
                    -e "container_name=${APP_NAME}-${env.BRANCH_NAME}" \
                    -e "app_port=${DEPLOY_PORT}" \
                    -e "docker_image=${FULL_IMAGE}:${IMAGE_TAG}" \
                    --vault-password-file /home/jenkins/ansible-master/.vault_pass
                    """
                }
            }
        }
    }
}
