pipeline {
  // Build in a docker image with puppet-agent
  agent { docker { image 'livelo/rh7-wls1213:latest' } }

  // Remove old builds
  options { buildDiscarder(logRotator(numToKeepStr: '7')) }
  environment { 
		SLACK_CHANNEL = '#infra-automation' 
		EXTRACT_HOST = 'myhostname.pontoslivelo.com.br'
	}

  stages {

    stage('Data Collector') {
      steps {
        script { 
					//
					ON_STAGE = "${STAGE_NAME}"

					// Retrieve username that triggers this event
          withCredentials([string(credentialsId: 'slack_search_user_api_token', variable: 'SLACK_TOKEN')]) {
						env.SLACK_USER = sh(script: "/home/jenkins/tools/data_collector.sh '${SLACK_TOKEN}'", returnStdout: true)
					}

        	// Notify channel on master, notify commiter on other branches
        	if (env.BRACH_NAME == 'master') { env.SLACK_DESTINATION = env.SLACK_CHANNEL }
					else { env.SLACK_DESTINATION = "@" + env.SLACK_USER }

					// After a successful user info retrievement, ask about the host
					env.EXTRACT_HOST = input(id: 'get_hostname', message: 'Qual o hostname para extrair os dados?', parameters: [
						[$class: 'TextParameterDefinition', defaultValue='myhostname.pontoslivelo.com.br', description: 'vbn', name: 'host_to_extract']
					])

					// Check if input was valid
					if ( env.EXTRACT_HOST == 'myhostname.pontoslivelo.com.br' ) { sh(script: "exit 1", returnStdout: false) }
      	}
    	}
    }

    stage('Preparation') {
      steps {
        script { ON_STAGE = "${STAGE_NAME}" }
				sh(script: "sed \"s/<some-hostname>/${EXTRACT_HOST}/g\" -i template.yaml", returnStdout: true)
    	}
    }

    // Build a module package and store it on Jenkins
    stage('Run') {
      steps {
        script { ON_STAGE = "${STAGE_NAME}" }
				sh(script: "python weblogic_query.py", returnStdout: true)
      }
    }

		stage('Store results') {
			steps {
				script { ON_STAGE = "${STAGE_NAME}" }
				sshagent(['stash_acesskey']) {
					sh(script: """
							# Get data from stash
							git clone ssh://git@stash.pontoslivelo.com.br:7999/pup/data.git

							# Create/Update host content from git
							mkdir -p data/profile_weblogic/extracted || echo "Already exists..."
							cp -uvf gathered-data.yaml data/profile_weblogic/extracted/${EXTRACT_HOST}.yaml

							# Push content
							git add data/profile_weblogic/extracted/${EXTRACT_HOST}.yaml
							git commit -m 'Extraction gathered from automation.'
							git push origin master
						""", returnStdout: true)
				}
			}
		}
  }

  post {
    failure {
      slackSend channel: env.SLACK_DESTINATION, color: 'danger',
      	message: "Extraction failed at ${ON_STAGE}: '<${BUILD_URL}|${JOB_NAME}:${BUILD_NUMBER}>'"
    }
    success {
      slackSend channel: env.SLACK_DESTINATION, color: 'good',
        message: "Extaction with Success: '<${BUILD_URL}|${JOB_NAME}:${BUILD_NUMBER}>'"
    }
  }
}
