pipeline {
    agent any
    stages {
        stage('Kodu Cek') {
            steps {
                git branch: 'main', url: 'https://github.com/fatmanurasa27/MHRS.git'
            }
        }
        stage('Dosyalari Kontrol Et') {
            steps {
                sh 'ls -la'
            }
        }
        stage('Uygulamayi Derle') {
            steps {
                echo 'Docker imaji olusturuluyor...'
                // Dockerfile'i kullanarak mhrs-app adinda bir imaj olusturur
                sh 'docker build -t mhrs-app:latest .'
            }
        }
        stage('Test') {
            steps {
                echo 'CI/CD Otomasyonu tamamlandi! MHRS imaji hazir!'
            }
        }
    }
}