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

        stage('Building and Pushing Docker Image to GCR'){
            steps{
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        sh '''
                        # AUTO-FIX: Install gcloud (your missing piece)
                        if ! command -v gcloud; then
                        echo "Installing gcloud..."
                        cd /tmp && curl -sSL https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz | tar xzf -
                        /tmp/google-cloud-sdk/install.sh --quiet
                        export PATH=$PATH:/tmp/google-cloud-sdk/bin
                        fi
                        
                        gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                        gcloud config set project useful-lattice-483309-k5
                        gcloud auth configure-docker gcr.io --quiet
                        cd ${env.WORKSPACE}
                        docker build -t gcr.io/{GCP_PROJECT}/ml-project:latest .
                        docker push gcr.io/useful-lattice-483309-k5/ml-project:latest
                        '''
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



