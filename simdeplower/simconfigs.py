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


def default_config():
    """
    Do not edit this. If you wish to make changes
    do so in your own script and provide the script
    on the command line using the proper args.

    :return:
    """
    return """
    #!/bin/bash
    # See the original work from William Lam at http://www.virtuallyghetto.com/
    ## DO NOT EDIT ##
    echo "Accepting EULA ..."
    /usr/sbin/vpxd_servicecfg eula accept
    echo "Setting default ports ..."
    /usr/sbin/vpxd_servicecfg 'ports' 'defaults'
    echo "Configuring Embedded DB ..."
    /usr/sbin/vpxd_servicecfg 'db' 'write' 'embedded'
    echo "Configuring SSO..."
    /usr/sbin/vpxd_servicecfg 'sso' 'write' 'embedded' 'password'
    #echo "Starting VCSIM ..."
    /usr/bin/vmware-vcsim-start default
    #echo "Starting VCSA ..."
    /usr/sbin/vpxd_servicecfg service start
    """
