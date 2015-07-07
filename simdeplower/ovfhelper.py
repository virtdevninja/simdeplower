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

class OvfHelper(object):

    def __init__(self, ovftool_path=None):
        """
        Constructor

        :param ovftool_path:
        :return:
        """
        if ovftool_path is None:

            LOG.info("No ovftool_path set. Attempting to locate ovftool on file system.")
            # try the location of the tool on osx
            if isfile(expanduser("/Applications/VMware OVF Tool/ovftool")):
                ovftool_path = expanduser("/Applications/VMware OVF Tool/ovftool")
            elif isfile(expanduser("/Applications/VMware Fusion.app/Contents/Library/VMware OVF Tool/ovftool")):
                ovftool_path = expanduser("/Applications/VMware Fusion.app/Contents/Library/VMware OVF Tool/ovftool")
            else:
                raise ValueError("ovftool_path required to continue.")
            # default fusion here for osx
            # even though this is a valid path for linux or any other unix
            # its doubtful someone would do such a horrible thing..
            LOG.info("Using {0}".format(ovftool_path))
        elif not isfile(expanduser(ovftool_path)):
            raise ValueError("ovftool not found at specified location.")

        self.ovftool_path = ovftool_path

    def extract_ovf_to_file_system(self, source=None, dest=None, name=None):
        """
        Extract an OVA to a given destination, and return full path to vmx

        vmx_path = extract_ovf_to_file_system("/tmp/myvcsa.ova", "/home/me/vms/")

        :param source:
        :param dest:
        :return:
        """
        if source is None or dest is None:
            raise ValueError("Missing source or dest argument")
        source = expanduser(source)
        if not isfile(source):
            raise ValueError("Invalid source location supplied. File not found.")
        dest = expanduser(dest)
        output = subprocess32.check_output(
            [
                self.ovftool_path,
                "--name={0}".format(name),
                source,
                dest
            ],
            universal_newlines=True
        )
        output = output.split("\n")
        # pattern to look for to match from above output
        mat = "Writing VMX file"
        output = (s for s in output if mat in s)
        val = next(output)
        output = val.split(":")[-1]
        LOG.debug(output)
        del val
        return output.strip()

