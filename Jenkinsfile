properties([
        pipelineTriggers([cron('0 5 * * *')]),
        disableConcurrentBuilds()
])
def startDate = new Date()
timestamps {
    try {
        node('kubepods') {
            stage('Checkout') {
                checkout scm
            }
            stage('Run Autotests on Chrome latest') {
                try {
                    sh '''
                        docker build --no-cache -t autotests:1 .
                        docker run -v ${WORKSPACE}/allure-results:/reports autotests:1
                    '''.stripIndent()
                } catch (Exception ex) {
                    println("[WARNING]")
                } finally {
                    stash includes: 'allure-results/', name: 'reports'
                }
            }
        }
        node('master') {
            stage('Generate Allure results') {
                unstash 'reports'
                allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: '${WORKSPACE}/allure-results']]
                ])
                def endDate = new Date()
                def tookTime = groovy.time.TimeCategory.minus(endDate,startDate).toString()
                slackSend color: 'good', message: "Total Autotests time took: ${tookTime}"
            }
        }
    } catch (e) {
        currentBuild.result = "FAILED"
        throw e
    } finally {
        notifySlack(currentBuild.result)
    }
}
def notifySlack(String buildStatus) {
    buildStatus = buildStatus ?: 'SUCCESS' // build status of null means success
    def message = "Autotests was: ${buildStatus}: `${env.JOB_NAME}` #${env.BUILD_NUMBER} :\n${env.BUILD_URL}"
    def color
    if (buildStatus == 'STARTED') {
        color = '#D4DADF'
    } else if (buildStatus == 'SUCCESS') {
        color = '#BDFFC3'
    } else if (buildStatus == 'UNSTABLE') {
        color = '#FFFE89'
    } else {
        color = '#FF9FA1'
    }
    //slackSend (color: color, message: message, channel: 'v2_frontend' )
}
