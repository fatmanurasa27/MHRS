pipeline {
    agent any
    stages {
        stage('Kodu Cek') {
            steps {
                // Sadece bu satırı değiştirdik, branch adını ekledik:
                git branch: 'main', url: 'https://github.com/fatmanurasa27/MHRS.git'
            }
        }
        stage('Test') {
            steps {
                echo 'MHRS kodlari Jenkins uzerine basariyla indirildi!'
            }
        }
    }
}