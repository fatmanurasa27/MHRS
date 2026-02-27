pipeline {
    agent any
    stages {
        stage('Kodu Cek') {
            steps {
                // GitHub'dan main dalindaki en guncel kodlari ceker
                git branch: 'main', url: 'https://github.com/fatmanurasa27/MHRS.git'
            }
        }
        stage('Dosyalari Kontrol Et') {
            steps {
                // Jenkins icine inen dosyalari listeler
                sh 'ls -la'
                echo 'Dosyalar basariyla Jenkins icine alindi!'
            }
        }
        stage('Test') {
            steps {
                echo 'CI/CD Otomasyonu basariyla tetiklendi! MHRS ucus modunda!'
            }
        }
    }
}