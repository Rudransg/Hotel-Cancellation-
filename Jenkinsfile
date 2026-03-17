pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "useful-lattice-483309-k5"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Rudransg/Hotel-Cancellation-.git']])
                }
            }
        }

        stage('Setting up our Virtual Environment and Installing dependancies'){
            steps{
                script{
                    echo 'Setting up our Virtual Environment and Installing dependancies............'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

        stage('Building and Pushing Docker Image to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        sh """
                        set -e

                        # Ensure gcloud is on PATH for this shell
                        if ! command -v gcloud >/dev/null 2>&1; then
                        # If installed under /google-cloud-sdk
                        if [ -d /google-cloud-sdk/bin ]; then
                            export PATH=\$PATH:/google-cloud-sdk/bin
                        elif [ -d /tmp/google-cloud-sdk/bin ]; then
                            export PATH=\$PATH:/tmp/google-cloud-sdk/bin
                        fi
                        fi

                        gcloud --version

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker gcr.io --quiet

                        cd ${env.WORKSPACE}
                        docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .
                        docker push gcr.io/${GCP_PROJECT}/ml-project:latest
                        """
                    }
                }
            }
        }


        stage('Deploy to Google Cloud Run'){
            steps{
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        sh '''
                        # gcloud already installed above
                        gcloud run deploy ml-project \
                            --image=gcr.io/useful-lattice-483309-k5/ml-project:latest \
                            --platform=managed \
                            --region=us-central1 \
                            --allow-unauthenticated \
                            --port=5000
                        '''
                    }
                }
            }
        }

        
    }
}



