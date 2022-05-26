# Build jenkins job from Github Action :rocket:

This action builds/triggers a jenkins job, waiting it to be finished and enabling to pass job params.

## Inputs

### `jenkins-token`

**Required**
 
 ### `jenkins-url`

**Required** 

### `jenkins-user`

**Required** 

### `job-path`

**Required** 

E.g.
```
if job inside folder:
 "job/folder_name/job/job_name"

if job in jenkins root: 
 "job/job_name"
```

### `job-params`

**Not mandatory**

Set jenkins params as JSON string:  

E.g.
```
 "{'param1': 'value1', 'param2': 'value2'}"
``` 

### `include-logs`

**Not mandatory**

Whether or not to include the build logs as output. They will be base64 encoded. Default is false:  

E.g.
```
 "true"
``` 


## Outputs

###  `job_status`
* FAILURE
* SUCCESS
* ABORTED

###  `job_number`
Job number

###  `job_url`
URL of the job

###  `job_log_info`
Base64 encoded logs of the job for some easy access


## Example usage
```
    - name: "Trigger jenkins job"
      uses: GoldenspearLLC/build-jenkins-job@master
      with:
        jenkins-url: ${{ secrets.JENKINS_URL }}
        jenkins-token: ${{ secrets.JENKINS_TOKEN }}
        user: "jenkins-username"
        job-path: "job/folder_name/job/job_name"
        job-params: "{'param1': 'value1', 'param2': 'value2'}"
        include-logs: "true"
        
    - name: Notify Slack
      uses: ravsamhq/notify-slack-action@v1
      if: always()
      with:
        status: ${{ job.status }}
        notification_title: ''
        message_format: '{emoji} <{{ steps.job-build.outputs.job_url }}|Jenkins Job {{ steps.job-build.outputs.job_number }}> was *{{ steps.job-build.outputs.job_status }}*.'
        footer: '<{run_url}|View Run>'
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```
