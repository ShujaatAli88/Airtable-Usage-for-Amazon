pipeline {
    agent any

    environment {
        EMAIL_USERNAME = credentials('EMAIL_USERNAME')       // your email address
        EMAIL_PASSWORD = credentials('EMAIL_PASSWORD')       // email app password
        EMAIL_TO       = credentials('EMAIL_TO')             // recipient email

        TWILIO_ACCOUNT_SID = credentials('TWILIO_ACCOUNT_SID')
        TWILIO_AUTH_TOKEN  = credentials('TWILIO_AUTH_TOKEN')
        TWILIO_SMS_FROM    = credentials('TWILIO_SMS_FROM')
        SMS_TO             = credentials('SMS_TO')
        WHATSAPP_FROM      = credentials('TWILIO_WHATSAPP_FROM')
        WHATSAPP_TO        = credentials('WHATSAPP_TO')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Simulate Build') {
            steps {
                echo "Building the project..."
                sleep 5
                echo "Done."
            }
        }

        stage('Send Email Notification') {
            steps {
                emailext (
                    subject: "✅ Jenkins Build - ${currentBuild.currentResult}",
                    body: """
-------------------------------------------------------
✅ Jenkins CI Notification
-------------------------------------------------------

Repository:  ${env.GIT_URL}
Branch:      ${env.GIT_BRANCH}
Build:       #${env.BUILD_NUMBER}
Status:      ${currentBuild.currentResult}

Job URL:
${env.BUILD_URL}

-------------------------------------------------------
This is an automated email from Jenkins.
""",
                    to: "${env.EMAIL_TO}",
                    from: "${env.EMAIL_USERNAME}"
                )
            }
        }

        stage('Send SMS & WhatsApp Notification') {
            steps {
                script {
                    writeFile file: 'notify.py', text: """
import os
from twilio.rest import Client

client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])

message_body = f\"""✅ Jenkins Notification
Repo: {os.environ.get('GIT_URL')}
Branch: {os.environ.get('GIT_BRANCH')}
Build: #{os.environ.get('BUILD_NUMBER')}
Status: {os.environ.get('BUILD_STATUS')}
🔗 {os.environ.get('BUILD_URL')}
\""" 

sms = client.messages.create(
    body=message_body,
    from_=os.environ["TWILIO_SMS_FROM"],
    to=os.environ["SMS_TO"]
)
print("SMS sent:", sms.sid)

whatsapp = client.messages.create(
    body=message_body,
    from_=os.environ["WHATSAPP_FROM"],
    to=os.environ["WHATSAPP_TO"]
)
print("WhatsApp sent:", whatsapp.sid)
"""
                    sh 'pip install twilio'
                    withEnv([
                        "BUILD_STATUS=${currentBuild.currentResult}",
                        "GIT_URL=${env.GIT_URL}",
                        "GIT_BRANCH=${env.GIT_BRANCH}",
                        "BUILD_NUMBER=${env.BUILD_NUMBER}",
                        "BUILD_URL=${env.BUILD_URL}"
                    ]) {
                        sh 'python3 notify.py'
                    }
                }
            }
        }
    }
}
