pipeline {
    agent any
    stages {
        stage('Kodu Cek') {
            steps {
                // Buraya kendi GitHub MHRS linkini yapistir
                git 'https://github.com/KULLANICI_ADIN/MHRS.git'
            }
        }
        stage('Test') {
            steps {
                echo 'MHRS kodlari Jenkins uzerine basariyla indirildi!'
            }
        }
    }
}