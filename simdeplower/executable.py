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

import argparse
import logging
import sys
import time

from simdeplower.ovfhelper import OvfHelper
from simdeplower.vmrunhelper import VmrunHelper
from simdeplower import simprov

def _setup_parser():
    """

    :return ArgumentParser:
    """
    parser = argparse.ArgumentParser(
        description='Standard arguments for simdeplower'
    )

    parser.add_argument(
        '-d',
        '--dest',
        required=True,
        action='store',
        help="Full path on file system where OVA will be extracted."
    )

    parser.add_argument(
        '-f',
        '--ovftool-path',
        required=False,
        action='store',
        help="Full path to the ovftool to use for deployment."
    )

    parser.add_argument(
        '-g',
        '--nogui',
        required=False,
        action='store_true',
        default=False,
        help="Default is false which provides a gui form fusion or workstation"
             " Set true if you want the VirtualMachine GUI to not be shown."
    )

    parser.add_argument(
        '-l',
        '--log-level',
        required=False,
        action='store',
        help="Set log level. Valid values are debug, info or warn"
    )

    parser.add_argument(
        '-n',
        '--name',
        required=False,
        action='store',
        default="simdeplower-{0}".format(int(time.time())),
        help="Set name of the new vm."
    )

    parser.add_argument(
        '-o',
        '--ova-path',
        required=True,
        action='store',
        help="Full path to the OVA file to use for deployment."
    )

    parser.add_argument(
        '-p',
        '--provider',
        required=False,
        action='store',
        help="Set provider type. Valid values are fusion or ws for workstation"
    )

    parser.add_argument(
        '-r',
        '--vmrun',
        required=False,
        action='store',
        help="Full path to vmrun"
    )

    parser.add_argument(
        '-s',
        '--script-path',
        required=True,
        action='store',
        help="Full path to the script used to configure the VCSA simulator."
    )

    parser.add_argument(
        '-t',
        '--target',
        required=True,
        action='store',
        help="Supported values are fusion or ws for workstation."
    )

    return parser



def execute():
    logging.basicConfig()
    log = logging.getLogger("simdeplower")
    parser = _setup_parser()
    provided_args = parser.parse_args(sys.argv[1:])
    if provided_args.log_level:
        if provided_args.log_level == "debug":
            log.setLevel(logging.DEBUG)
        elif provided_args.log_level == "info":
            log.setLevel(logging.INFO)
        else:
            log.setLevel(logging.WARN)

    log.debug("Parsed args.")
    ovftool_path = provided_args.ovftool_path
    ovftool = OvfHelper(ovftool_path=ovftool_path)
    log.debug("OvfTool found. {0}".format(ovftool.ovftool_path))
    source = provided_args.ova_path
    dest = provided_args.dest
    log.info("Extracting ova to disk. This may take a while.")
    vmx_path = ovftool.extract_ovf_to_file_system(source=source, dest=dest,
                                                  name=provided_args.name)
    log.info("Extracted ova to disk.")
    vmrun = VmrunHelper(vmrun_path=provided_args.vmrun,
                        nogui=provided_args.nogui,
                        target=provided_args.target)
    log.debug("Starting VM.")
    vmrun.start_vmx(vmx_path=vmx_path)
    vm_ip = vmrun.get_vmx_ip(vmx_path=vmx_path)
    log.debug("Found VM running on IP: {0}".format(vm_ip))
    sim_ouput = simprov.provision_simulator(script_path=provided_args.script_path, host=vm_ip)
    for item in sim_ouput:
        item = item.rsplit("\n")[0]
        log.debug(item)

    print "You can now log into your vcsa at: {0}".format(vm_ip)

if __name__ == "__main__":
    execute()
