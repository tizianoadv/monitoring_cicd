pipeline {
   agent { label 'agentCI' }
   stages {
        stage('Checkout') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/tizianoadv/monitoring_cicd.git']])
            }
        }
        // stage('Build') {
        //     steps {
        //         docker build -t monitoring:latest app/.

        //     }
        // }
        // stage('Test') {
        //     steps {
        //         sh'python3 -m venv venv-pytest'
        //         source env/bin/activate
        //         pip3 install -r app/requirements.txt
        //         pip3 install bs4 requests pytz
        //     }
        // }   
        // stage('Build') {
        //     steps {
        //         checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/tizianoadv/monitoring_cicd.git']])
        //     }
        // }
        // stage('Run') {
        //     steps {
        //         checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/tizianoadv/monitoring_cicd.git']])
        //     }
        // }
    }
}