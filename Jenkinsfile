pipeline{

	agent any

	environment {
		DOCKERHUB_CREDENTIALS=credentials('DockerHub_credentials')
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
				sh 'docker build -t sandeepdh32/flask-voting-app:$BUILD_NUMBER .'
			}
		}

		stage('Login') {
			steps {
				sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
			}
		}

		stage('Push') {
			steps {
				sh 'docker push sandeepdh32/flask-voting-app:$BUILD_NUMBER'
			}
		}
	}

	post {
		always {
			sh 'docker logout'
		}
		failure {
            echo 'Pipeline failed'
        }
	}

}