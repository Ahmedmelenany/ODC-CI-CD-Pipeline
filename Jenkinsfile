pipeline {
    agent any 
    environment {
        IMAGE_NAME = 'ahmedelenany703/weather-app'
        Docker= 'Docker'
    }
    stages {
        stage('Clone and Pull Repository') {
            steps {
                    git branch: 'main', url: 'git@github.com:Ahmedmelenany/ODC-CI-CD-Pipeline.git'
                    }
                }
            
        stage('Building Docker image') {
            steps {
                    dir('src') {
                        script{
                    docker.build(IMAGE_NAME)
            }
                    }
        }
        }
        
        stage('Push Docker Image To Docker Hub') {
            steps {
                script{
                        withDockerRegistry([credentialsId: 'Docker']) {
                           sh " docker push $IMAGE_NAME "
                        }
                    }
                
            }
            }

        stage('Ansible for Deploying') {
            steps {
                    dir('ansible') {
                        withEnv(["ANSIBLE_HOST_KEY_CHECKING=false"]){
                        ansiblePlaybook(
                    playbook: "playbook.yaml",
                    inventory: "inventory"
                )
                    }
                    }
        }
        }
        
        
    }
    post {
            always {
                mail bcc: '', body: """
                Job: ${JOB_NAME}
                Build Number: ${BUILD_NUMBER}
                Build Status: ${currentBuild.result}
                """, cc: '', subject: 'Jenkins Pipeline State', to: 'ahmedelenany703@gmail.com'
            }
        }
}
