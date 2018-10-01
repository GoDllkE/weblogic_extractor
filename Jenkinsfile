pipeline {
	agent {
		kubernetes {
			label 'python2-builder'
			serviceAccount 'jenkins'
			yamlFile 'KubernetesPod.yaml'
		}
	}
	environment {
		// Notification environment
		SLACK_CHANNEL = '#infra-automation'
	}

	stages {
		stage('Recuperando informacoes do modulo') {
			steps {
				container('py2-builder') {
					script {
						// Devilery environment
						PROJECT = sh(script: "echo $JOB_NAME | cut -d '/' -f2 | tr -d [:space:]", returnStdout: true)
						COMPONENT = sh(script: "echo $JOB_NAME | cut -d '/' -f4 | tr -d [:space:]", returnStdout: true)
						APP_NAME = sh(script: "echo $JOB_NAME | cut -d '/' -f5 | tr -d [:space:]", returnStdout: true)
						APP_VERSION = sh(script: "cat version.txt | tr -d [:space:]", returnStdout: true)
					}
				}
			}
		}
		//stage('Instalando dependencias do modulo') {
		//	steps {
		//		container('py2-builder') {
		//			script { ON_STAGE = "${STAGE_NAME}" }
		//			sh(script: "pip install --upgrade pyyaml requests pyinstaller", returnStdout: true)
		//		}
		//	}
		//}

		stage('Empacotando o  modulo') {
			steps {
				container('py2-builder') {
					script {ON_STAGE = "${STAGE_NAME}"}
					sh(script: "zip -r '$APP_NAME'.zip functions resources weblogic_query.py", returnStdout: true)
				}
			}
		}

		stage('Realizando upload para o repositorio') {
			steps {
				container('py2-builder') {
					script { ON_STAGE = "${STAGE_NAME}"}

					// Upload artifact into nexus
					nexusArtifactUploader (
						nexusVersion: 'nexus2',							  // Keep
						protocol: 'http',									  // Keep
						nexusUrl: 'nexus.pontoslivelo.com.br/nexus',		  // Nexus base url
						groupId: "br.com.pontoslivelo.$PROJECT.$COMPONENT", // Repo url
						version: "${APP_VERSION}",						  // Artifact version
						repository: 'site-automations',					  // Repo id
						credentialsId: 'jenkins-nexus',
						artifacts: [[
							artifactId: "${APP_NAME}",					  // Artifact name
							classifier: 'python26',						  // Artifact tecnology type
							file: "${APP_NAME}.zip",						  // File to upload
							type: 'zip'									  // File extension
						]]
					)
				}
			}
			// End of stage
		}
	}
	post {
		failure {
			slackSend channel: env.SLACK_CHANNEL, color: 'danger',
			message: "Build failed at ${ON_STAGE}: '<${BUILD_URL}|${JOB_NAME}:${BUILD_NUMBER}>'"
		}
		success {
			slackSend channel: env.SLACK_CHANNEL, color: 'good',
			message: "Build with Success: '<${BUILD_URL}|${JOB_NAME}:${BUILD_NUMBER}>'"
		}
	}
}
