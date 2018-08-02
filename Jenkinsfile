pipeline {
  agent { docker { image 'livelo/rh7_wls1213:latest' } }
  options { buildDiscarder(logRotator(numToKeepStr: '7')) }
  environment { SLACK_CHANNEL = '#infra-automation' }

//  stages {
//
//    stage('Data Collector') {
//      steps {
//        script { 
//					//
//					ON_STAGE = "${STAGE_NAME}"
//
//					// Retrieve username that triggers this event
//          withCredentials([string(credentialsId: 'slack_search_user_api_token', variable: 'SLACK_TOKEN')]) {
//						env.SLACK_USER = sh(script: "/app/tmp/data_collector.sh ${SLACK_TOKEN}", returnStdout: true)
//					}
//
//        	// Notify channel on master, notify commiter on other branches
//        	if (env.BRACH_NAME == 'master') { env.SLACK_DESTINATION = env.SLACK_CHANNEL }
//					else { env.SLACK_DESTINATION = "@" + env.SLACK_USER }
//				}
//			}
//		}
//
//		stage('Weblogic to query') {
//			steps {
//				script {
//					//
//					ON_STAGE = "${STAGE_NAME}"
//
//					// After a successful user info retrievement, ask about the host
//					env.EXTRACT_HOST = input(id: 'get_hostname', message: 'Qual o hostname para extrair os dados?', parameters: [
//						[$class: 'StringParameterDefinition', description: 'Insira o hostname do weblogic para extrair os dados:', name: 'host_to_extract']
//					])
//				
//					// Update template
//					sh(script: "sed \"s/<some-hostname>/${EXTRACT_HOST}/g\" -i template.yaml", returnStdout: false)
//				}
//			}
//		}
//		
//	stage('Weblogic credentials') {
//			steps {
//				script {
//					//
//					ON_STAGE = "${STAGE_NAME}"
//
//					env.WLST_USERNAME = input(id: 'get_username', message: 'Informe o usuario desta instancia do weblogic', parameters: [
//						[$class: 'StringParameterDefinition', description: 'Username:', name: 'wlst_username']
//					])
//
//					env.WLST_PASSWORD = input(id: 'get_password', message: 'Informe a senha desta instancia do weblogic:', parameters: [
//					//	[$class: 'TextParameterDefinition', description: 'Password:', name: 'wlst_password']
//							[$class: 'PasswordParameterDefinition', description: 'Password:', name: 'wlst_password']
//					])
//
//					// Update template
//					sh(script: "sed \"s/<some-username>/${WLST_USERNAME}/g\" -i template.yaml", returnStdout: false)
//					sh(script: "sed \"s/<some-password>/${WLST_PASSWORD}/g\" -i template.yaml", returnStdout: false)
//				}
//			}
//		}
//
//    // Build a module package and store it on Jenkins
//    stage('Run') {
//      steps {
//        script { ON_STAGE = "${STAGE_NAME}" }
//				sh(script: "python weblogic_query.py -d", returnStdout: true)
//      }
//    }
//
//		stage('Store results') {
//			steps {
//				script { ON_STAGE = "${STAGE_NAME}" }
//				sshagent(['stash_acesskey']) {
//					sh(script: """
//							# Get out from git dir
//							# Get data from stash
//							cd /app/product/oracle
//							git clone ssh://git@stash.pontoslivelo.com.br:7999/pup/data.git
//
//							# Create/Update host content from git
//							mkdir -p data/profile_weblogic/extracted || echo "Already exists..."
//							cp -uvf gathered-data.yaml data/profile_weblogic/extracted/${EXTRACT_HOST}.yaml
//
//							# Push content
//							git add data/profile_weblogic/extracted/${EXTRACT_HOST}.yaml
//							git commit -m 'Extraction gathered from automation.'
//							git push origin master
//						""", returnStdout: true)
//				}
//			}
//		}
//  }

//	post {
//    failure {
//      slackSend channel: env.SLACK_DESTINATION, color: 'danger',
//      	message: "Extraction failed at ${ON_STAGE}: '<${BUILD_URL}|${JOB_NAME}:${BUILD_NUMBER}>'"
//    }
//    success {
//      slackSend channel: env.SLACK_DESTINATION, color: 'good',
//        message: "Extaction with Success: '<${BUILD_URL}|${JOB_NAME}:${BUILD_NUMBER}>'"
//    }
//  }
}
