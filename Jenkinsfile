pipeline {
    agent any
    stages {
        stage('Kodu Cek') {
            steps {
                git 'https://github.com/fatmanurasa27/MHRS.git'
            }
        }
        stage('Test') {
            steps {
                echo 'MHRS kodlari Jenkins uzerine basariyla indirildi!'
            }
        }
    }
}