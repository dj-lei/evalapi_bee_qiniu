pipeline {
    agent {
        node { label 'python' }
    }

    options {
        gitLabConnection('gitlab-conn')
    }

    stages {
        stage('test') {
            steps {
                sh 'printenv'
                updateGitlabCommitStatus name: 'jenkins-evalapi_bee', state: 'running'
                sh 'docker build . -t evalapi_bee_${GIT_COMMIT}_${BUILD_ID} -f Dockerfile-test'
                sh 'docker run -dt --name evalapi_bee_${GIT_COMMIT}_${BUILD_ID} evalapi_bee_${GIT_COMMIT}_${BUILD_ID}'
                sh 'docker exec -t evalapi_bee_${GIT_COMMIT}_${BUILD_ID} tox'
            }
        }

        stage('Release latest developing version') {
            environment {
                GIT = credentials('18b72514-6351-42bc-b8ba-8cb60b190292')
            }
            when {
                branch 'dev'
            }
            steps {
                sh 'git config --global user.email "djlei@gongpingjia.com"'
                sh 'git config --global user.name "leidengjun"'

                sh "git tag -af latest -m 'latest commit on dev'"
                sh 'git push http://$(echo $GIT_USR | sed "s/@/%40/g"):${GIT_PSW}@${GIT_URL#http://} latest -f'
                sh 'git config --global --unset user.email'
                sh 'git config --global --unset user.name'
            }
        }

        stage('Release') {
            environment {
                GIT = credentials('18b72514-6351-42bc-b8ba-8cb60b190292')
                OSS = credentials('2ec0bb5f-5d52-4bfc-88cf-65077f48cfd4')
                VERSION = '0.0.33'                      //发布之前需要在这里指定版本号
            }
            when {
                branch 'master'
            }
            steps {
                sh 'git config --global user.email "djlei@gongpingjia.com"'
                sh 'git config --global user.name "leidengjun"'

                sh "git tag -af release-v${VERSION} -m 'release ${VERSION}'"
                sh 'git push http://$(echo $GIT_USR | sed "s/@/%40/g"):${GIT_PSW}@${GIT_URL#http://} release-v${VERSION}'
                sh 'docker exec -t evalapi_bee_${GIT_COMMIT}_${BUILD_ID} pip install -qr requirements_fc.txt  -t /app/proj/evalapi_bee/'
                sh 'docker exec -t evalapi_bee_${GIT_COMMIT}_${BUILD_ID} bash -c \"rm -rf /app/proj/evalapi_bee/numpy* /app/proj/evalapi_bee/scipy*\"'
                sh 'docker exec -t evalapi_bee_${GIT_COMMIT}_${BUILD_ID} bash -c \"cd /app/proj/evalapi_bee && find ./ -name \'*.pyc\' -exec rm -f {} \\; && zip -qr evalapi_${GIT_COMMIT}.zip .\"'
                sh 'docker exec -t evalapi_bee_${GIT_COMMIT}_${BUILD_ID} bash -c \"wget -qO /usr/local/bin/ossutil \'http://docs-aliyun.cn-hangzhou.oss.aliyun-inc.com/assets/attach/50452/cn_zh/1516454058701/ossutil64\' && chmod +x /usr/local/bin/ossutil\"'
                sh 'docker exec -t evalapi_bee_${GIT_COMMIT}_${BUILD_ID} ossutil config -e oss-cn-beijing-internal.aliyuncs.com -k ${OSS_PSW} -i ${OSS_USR}'
                sh 'docker exec -t evalapi_bee_${GIT_COMMIT}_${BUILD_ID} ossutil cp /app/proj/evalapi_bee/evalapi_${GIT_COMMIT}.zip oss://gpj-evaluation-models/functions/ > /dev/null 2>&1'

                sh 'git config --global --unset user.email'
                sh 'git config --global --unset user.name'

            }
        }
    }

    post {
        failure {
            updateGitlabCommitStatus name: 'jenkins-evalapi_bee', state: 'failed'
        }
        success {
            updateGitlabCommitStatus name: 'jenkins-evalapi_bee', state: 'success'
        }
        always {
            sh 'docker ps | grep -w evalapi_bee_${GIT_COMMIT}_${BUILD_ID} && docker rm -f evalapi_bee_${GIT_COMMIT}_${BUILD_ID}'
            sh 'docker images | grep -w evalapi_bee_${GIT_COMMIT}_${BUILD_ID} && docker rmi evalapi_bee_${GIT_COMMIT}_${BUILD_ID}'
        }
    }
}