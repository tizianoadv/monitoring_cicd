pipeline {
   agent { label 'agentCI' }
   stages {
        stage('Checkout') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/tizianoadv/monitoring_cicd.git']])
            }
        }
        stage('Build') {
            steps {
                sh 'bash jenkins/build_run.sh'
            }
        }
        stage('Unit Test') {
            steps {
                sh 'bash jenkins/test.sh' 
            }
        } 
        stage('Push') {
            steps {
                sh 'bash jenkins/push.sh' 
            }
        }   
    }
}