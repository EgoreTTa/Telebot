pipeline {
    agent any

    environment {
		PIPENV_VENV_IN_PROJECT	= '1'
        API_TOKEN				= credentials('API_TOKEN')
        DEPLOY_DIR				= '/home/ubuntu/EgoreTTaBot'
        SERVICE     			= 'EgoreTTaBot.service'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
		stage('Stop Service') {
			steps {
				sh 'sudo systemctl stop $SERVICE'
			}
		}
		stage('Install') {
            steps {
				sh 'pipenv install --deploy'
				sh 'sudo mv -f * $DEPLOY_DIR'
				sh 'sudo chmod 777 $DEPLOY_DIR -R'
			}
		}
		stage('Deploy') {
            steps {
                sh 'bash $DEPLOY_DIR/deploy.sh'
            }
        }
		stage('Start Service') {
			steps {
				sh 'sudo systemctl start $SERVICE'
			}
		}
		stage('Get status Service') {
			steps {
				sh '''
					sleep 1
					
					for i in 1 2 3 4 5; do
						if sudo systemctl is-active --quiet $SERVICE; then
							echo "✅ Service is active (running)"
							exit 0
						fi
							echo "⏳ Waiting... ($i)"
						sleep 2
					done
					
					echo "❌ Service failed to start"
						sudo systemctl status $SERVICE --no-pager
						sudo journalctl -u $SERVICE --no-pager -n 20
					exit 1
				'''
			}
		}
	}
}