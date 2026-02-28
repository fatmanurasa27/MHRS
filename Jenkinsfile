pipeline {
    agent any
    stages {
        stage('Kodu Cek') {
            steps {
                git branch: 'main', url: 'https://github.com/fatmanurasa27/MHRS.git'
            }
        }
        stage('Ubuntu Deploy') {
            steps {
                echo 'Ubuntu sunucusuna baglaniliyor ve MHRS projesi ayaga kaldiriliyor...'
                sh '''
                ssh -o StrictHostKeyChecking=no user@172.20.10.2 "
                    if [ ! -d 'MHRS' ]; then
                        git clone https://github.com/fatmanurasa27/MHRS.git
                    fi
                    cd MHRS
                    git pull origin main
                    docker-compose up -d --build
                "
                '''
            }
        }
        stage('Test') {
            steps {
                echo 'CI/CD Otomasyonu KUSURSUZ! MHRS uygulamasi Ubuntu sunucusunda yayinda!'
            }
        }
    }
}