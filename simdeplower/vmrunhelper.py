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

import subprocess32

LOG = logging.getLogger("simdeplower")

class VmrunHelper(object):
    """
    Helper class to make running vmrun commands a bit easier..
    No that they are hard.. but what ever.
    """

    def __init__(self, vmrun_path=None, nogui=None, target=None):
        """
        Constructor

        :param vmrun_path: str path to vmrun binary
        :param nogui: bool
        :return:
        """
        if vmrun_path is None:
            LOG.debug("vmrun path not set. Attempting OSX settings")
            osx_path = "/Applications/VMware Fusion.app/Contents/Library/vmrun"
            osx_path = expanduser(osx_path)
            if isfile(osx_path):
                vmrun_path = osx_path
                target = "fusion"
                LOG.debug("OSX settings successful.")
            else:
                raise ValueError(
                    "vmrun_path not supplied. vmrun not found on file system."
                    " Please supply full path to vmrun binary.")
        elif not isfile(expanduser(vmrun_path)):
            raise ValueError("vmrun not found at path provided. Please provide"
                             " full path to vmrun binary.")

        if target != "fusion" and target != "ws":
            msg = "Only supported target is 'fusion' or 'ws' for workstation."
            raise ValueError(msg)

        self.target = target
        self.vmrun = expanduser(vmrun_path)
        if nogui is None:
            self.gui_setting = "nogui"
        if nogui:
            self.gui_setting = "nogui"
        else:
            self.gui_setting = "gui"
        LOG.debug("Using gui: {0}".format(self.gui_setting))
        LOG.debug("Using target: {0}".format(self.target))
        LOG.debug("Using vmrun: {0}".format(self.vmrun))

    def start_vmx(self, vmx_path=None):
        """
        If no exception is thrown it started the vm.

        :param vmx_path:
        :return:
        """
        vmx_path = expanduser(vmx_path)
        self._verify_vmx_path(vmx_path)
        cli_msg = subprocess32.check_call(
            [
                self.vmrun,
                "-T",
                self.target,
                "start",
                vmx_path,
                self.gui_setting
            ]
        )

    def stop_vmx(self, vmx_path=None):
        vmx_path = expanduser(vmx_path)
        self._verify_vmx_path(vmx_path)
        cli_msg = subprocess32.check_call(
            [
                self.vmrun,
                "-T",
                self.target,
                "stop",
                vmx_path
            ]
        )
        LOG.debug(cli_msg)

    def get_vmx_ip(self, vmx_path=None):
        vmx_path = expanduser(vmx_path)
        self._verify_vmx_path(vmx_path)
        output = subprocess32.check_output(
            [
                self.vmrun,
                "-T",
                self.target,
                "getGuestIPAddress",
                vmx_path,
                "-wait"
            ]
        )
        return output.rstrip('\n')

    @staticmethod
    def _verify_vmx_path(vmx_path=None):
        if vmx_path is None:
            raise ValueError("vmx_path was None. "
                             "Im sorry Dave, Im afraid I cant do that.")
        if not isfile(vmx_path):
            raise ValueError("File not found using vmx_path {0}".format(vmx_path))
        if not vmx_path.endswith(".vmx"):
            raise ValueError("vmx_path does not end with .vmx fix the file.")
