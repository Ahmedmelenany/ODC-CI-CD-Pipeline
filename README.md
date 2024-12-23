# Jenkins CI/CD Pipeline with Git, Docker, and Ansible

This project demonstrates a Jenkins CI/CD pipeline that automates the building, Pushing and deployment of applications.

![](./Images/image6.PNG)

## Technologies Used 
    - Python
    - Jenkins
    - Git
    - Docker
    - Ansible
    - Gmail SMTP Server

## Prerequisites

- Jenkins installed and configured.
- Git repository containing the application code, Dockerfile and Jenkinsfile.
- Docker installed and configured.
- Access to a Docker registry.
- Ansible installed and configured.
- SMTP configuration for Gmail in Jenkins.

## Pipeline Stages

1. **Git**
   - Clones the last changes of the source code from a specified Git repository.

2. **Docker Build**
   - Builds a Docker image using a provided Dockerfile.

3. **Docker Push**
   - Pushes the Docker image to a Docker registry (e.g., Docker Hub).

4. **Ansible Deployment**
   - Deploys the application to a remote machine using Ansible playbooks.

5. **Post: Email Notification (Gmail)**
   - Sends a summary email via Gmail about the pipeline’s status (success or failure).


## Setup Instructions

### Cloning the Repository

   ``` 
    git clone https://github.com/Ahmedmelenany/ODC-CI-CD-Pipeline.git
   ``` 

   ```
    cd ODC-CI-CD-Pipeline.git
   ```

### Jenkins Configuration

1. **Jenkins Pipeline Configuration**
   - Open Jenkins and Choose new item .
   - Choose the name of your project and select "Pipeline" type for your Jenkins job.

2. **Set Up Git in Your Pipeline**
   - Choose Jenkinsfile from SCM and replace by your repo based on your credentials (HTTP,SSH):

   ```
   https://github.com/Ahmedmelenany/ODC-CI-CD-Pipeline.git

   git@github.com:Ahmedmelenany/ODC-CI-CD-Pipeline.git
   ```

3. **Test Git Configuration**
   - Save the pipeline and run the job.
   - Check the logs to ensure the repository is cloned successfully.

4. **Verify the Cloned Repository**
   - Jenkins will clone the repository into its workspace directory.
   - You can access the workspace by navigating to the Jenkins job and clicking on **Workspace** in the sidebar or in your machine open jenkins_home/workspaces/your-job-name

### Additional Configuration for Private Repositories

- If your repository is private, ensure you:
  - Generate an SSH key or create a Personal Access Token (PAT) for HTTPS.
  - Add the PAT or SSH key to your Git hosting provider.
  - Configure the credentials in Jenkins.

## Pipeline Script (Jenkinsfile)

```groovy
pipeline {
    agent any 
    environment {
        IMAGE_NAME = 'ahmedelenany703/weather-app'
        Docker= 'Docker'
    }
    stages {
        stage('Clone and Pull Repository') {
            steps {
                    git branch: 'main', url: 'git@github.com:Ahmedmelenany/ODC-CI-CD-Pipeline.git (Replace This url with your repo)'
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
                """, cc: '', subject: 'Jenkins Pipeline State', to: 'Your-Gmail'
            }
        }
}

```

### Final Pipeline View 
The final pipeline view will display the following stages and their corresponding steps:
- **Build Docker Image**: This stage will build the Docker image using the Dockerfile in the src directory. The image will be named after the variable IMAGE_NAME.
- **Push Docker Image To Docker Hub**: This stage will push the Docker image to Docker Hub 
using the Docker registry credentials.
- **Ansible for Deploying**: This stage will deploy the application using Ansible. The playbook
will be executed with the inventory file.
- **Post Build**: This stage will send an email with the job details after the build is complete.

![](./Images/image1.PNG)


### Deployed application in the target machine view

![](./Images/image2.PNG)
![](./Images/image3.PNG)
![](./Images/image4.PNG)


### SMTP Gmail Configuration

#### Configure Gmail Account

1. Log in to your Gmail account.
2. Navigate to **Manage your Google Account > Security**.
3. Enable **2-Step Verification**.
4. Generate an **App Password**:
   - Under "Signing in to Google," click **App Passwords**.
   - Click **Generate** to get the app password.
5. Save the generated app password for use in Jenkins.

#### Configure Jenkins SMTP Settings

1. Open Jenkins and navigate to **Manage Jenkins > Configure System**.
2. Scroll down to the **E-mail Notification** section.
3. Fill in the following details:
   - **SMTP server**: `smtp.gmail.com`
   - Check **Use SMTP Authentication**.
   - Enter your Gmail address and the generated app password.
   - Check **Use SSL** and set the SMTP port to `465`.
4. Save the configuration.
5. Test the configuration by sending a test email from Jenkins.

### Post Gmail Email Notifaction View

![](./Images/image5.PNG)


## Troubleshooting

- **Git Checkout Failure**: Verify repository URL, branch name and credentials in .ssh in your jenkins server.
- **Docker Errors**: Check the Dockerfile for correctness and ensure Docker is running, Also Check for right Docker hub Credentials.
- **Ansible Deployment Issues**: Validate inventory file and playbook syntax with ensuring right permissions in private key (600 or 400).
- **Email Notifications Not Working**: Ensure Gmail SMTP settings and credentials are correct.

## End Of The Project
