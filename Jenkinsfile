pipeline {
    agent any
    stages {
        stage('Kodu Cek') {
            steps {
                // Kodlari GitHub'dan Jenkins'in icine ceker
                git branch: 'main', url: 'https://github.com/fatmanurasa27/MHRS.git'
            }
        }
        stage('Ubuntu Sunucusuna Deploy Et') {
            steps {
                echo 'Ubuntu sunucusuna baglaniliyor ve MHRS projesi ayaga kaldiriliyor...'
                // Jenkins, Ubuntu'ya baglanir ve komutlari orada calistirir
                sh '''
                ssh -o StrictHostKeyChecking=no user@172.20.10.2 "
                    if [ ! -d 'MHRS' ]; then
                        git clone https://github.com/fatmanurasa27/MHRS.git
                    fi
                    cd MHRS
                    git pull origin main
                    docker compose up -d --build
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