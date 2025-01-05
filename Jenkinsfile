pipeline{

	agent any

	environment {
		DOCKER_IMAGE_NAME='flask-voting-app-web'
		K8S_NAMESPACE='dev'
		HELM_RELEASE_NAME='flask-voting-app'
	}

	stages {
	    stage('Fetch Code') {
			steps {
                git branch: 'main', 
                url: 'https://github.com/sandeepgit32/flask-voting-app.git'
            }
		}

		stage('Code Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh """
                    ${tool 'SonarQube_scanner'}/bin/sonar-scanner
                    """
                }
            }
        }

		stage('Build') {
			steps {
				sh "docker build -t ${DOCKER_IMAGE_NAME}:${BUILD_NUMBER} ."
			}
		}

		stage('Load Docker Image to Minikube') {
            steps {
                script {
                    echo "Loading Docker image into Minikube..."
                    sh "minikube image load ${DOCKER_IMAGE_NAME}:${BUILD_NUMBER}"
                }
            }
        }

		stage('Deploy to Minikube with Helm') {
            steps {
                script {
                    echo "Deploying to Minikube using Helm..."
                    sh """
                        helm upgrade --install ${HELM_RELEASE_NAME} ./helm-charts \
						--values helm-charts/values-${K8S_NAMESPACE}.yaml
                        --set flaskApp.image.repository=${DOCKER_IMAGE_NAME} \
                        --set flaskApp.image.tag=${BUILD_NUMBER} \
                        --namespace ${K8S_NAMESPACE} \
                        --create-namespace
                    """
                }
            }
        }
	}

	post {
		success {
			echo 'Pipeline completed successfully!'
		}
		failure {
            echo 'Pipeline failed. Please check the logs.'
        }
	}

}