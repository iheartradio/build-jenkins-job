#!/usr/bin/env python3
import base64
import json
import sys
import time

# use of https://python-jenkins.readthedocs.io/en/latest/index.html
import jenkins


def mandatory_arg(argv):
    if argv == "":
        raise ValueError("Only job_params can be empty. Required fields: url, token, user and path")
    return argv


# mandatory
JENKINS_URL = mandatory_arg(sys.argv[1])
JENKINS_TOKEN = mandatory_arg(sys.argv[2])
JENKINS_USER = mandatory_arg(sys.argv[3])
JOB_PATH = mandatory_arg(sys.argv[4])

# not mandatory
JOB_PARAMS = sys.argv[5] or '{}'
INCLUDE_LOGS = sys.argv[6] or False


class JenkinsProxy:

    def __init__(self):
        self.server = jenkins.Jenkins(f"http://{JENKINS_URL}", username=JENKINS_USER, password=JENKINS_TOKEN)

    @property
    def job_name(self) -> str:
        return "".join(JOB_PATH.split("job/"))

    def build_job(self):
        return self.server.build_job(self.job_name, parameters=json.loads(JOB_PARAMS), token=JENKINS_TOKEN)

    def get_queue_item(self, item_id):
        while True:
            item = self.server.get_queue_item(item_id)
            if "executable" in item:
                return item

            time.sleep(3)

    def poll_build(self, build_number: int):
        while True:
            build_info = self.server.get_build_info(name=self.job_name, number=build_number)
            if not build_info["result"]:
                time.sleep(1)
                continue
            return build_info


jp = JenkinsProxy()
queue_item_id = jp.build_job()
queue_item = jp.get_queue_item(queue_item_id)

info = jp.poll_build(build_number=queue_item["executable"]["number"])

if INCLUDE_LOGS:
    log_info = jp.server.get_build_console_output(jp.job_name, info['number'])
    log_info = str(base64.b64encode(log_info.encode('utf-8'))).strip()
    print(f"::set-output name=job_log_info::{log_info}")
else:
    print(f"::set-output name=job_log_info::")

print(f"::set-output name=job_status::{info['result']}")
print(f"::set-output name=job_number::{info['number']}")
print(f"::set-output name=job_url::{info['url']}")

if info['result'] != "SUCCESS":
    sys.exit(1)
