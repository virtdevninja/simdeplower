#   Copyright 2015 Michael Rice <michael@michaelrice.org>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import logging

from os.path import expanduser, isfile

import paramiko

from simdeplower import simconfigs

LOG = logging.getLogger("simdeplower")

def provision_simulator(script_path=None, user=None,
                        passwd=None, host=None):
    if host is None:
        raise ValueError("No host provided to connect to.")
    if user is None:
        user = "root"
    if passwd is None:
        passwd = "vmware"
    if script_path is not None:
        script_path = expanduser(script_path)
        if not isfile(script_path):
            raise ValueError("Invalid script path provided.")
        LOG.debug("Reading script into memory.")
        with open(script_path) as script:
            script_data = script.read()
    else:
        LOG.debug("No script provided. Using default")
        script_data = simconfigs.default_config()

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(
        paramiko.AutoAddPolicy()
    )
    ssh.connect(hostname=host, username=user, password=passwd)
    LOG.info("Successful connection to vCenter made.")
    LOG.info("Simulator provisioning in process. This may take a while!")
    stdin, stdout, stderr = ssh.exec_command(script_data)
    output = stdout.readlines()
    return output
