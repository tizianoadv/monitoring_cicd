pipeline {
   agent any
   stages {
        stage('Checkout') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/tizianoadv/monitoring_cicd.git']])
            }
        }     
    }
}