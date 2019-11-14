#!/usr/bin/python


ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['alpha'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: mqsc

short_description: Simple module to manage an IBM MQ9 installation.

version_added: "2.9"

description:
    - "This module was made in order to manage an IBM MQ 9 installation.
    it can create Channels, Queues and QManagers."

options:
    name:
        description:
            - This is the message to send to the test module
        required: true
    new:
        description:
            - Control to demo if the result of this module is changed or not
        required: false

author:
    - Charl-Alexandre Le Brun (@Ramoreik)
'''

EXAMPLES = '''
TODO
'''

RETURN = '''
TODO
'''
import os
import re
import time
import shlex
import traceback
import subprocess
from ansible.module_utils.basic import AnsibleModule

module = None

IMPORTANT_BINARIES_LOCATION = {
    'RUNMQSC' : '/usr/bin/runmqsc',
    'CRTMQM' : '/usr/bin/crtmqm',
    'STRMQM' : '/usr/bin/strmqm',
    'DSPMQ' : '/usr/bin/dspmq',
    'DSPMQVER' : '/usr/bin/dspmqver',
    'ENDMQM' : '/usr/bin/endmqm',
    'DLTMQM' : '/usr/bin/dltmqm'
}

# ================================================================================
# DEVNOTE:
# Classes that manage the different MQSC concepts, QMGR, QUEUES and CHANNELS.

class QMGR():
    DSPMQ_REGEX = r"QMNAME\(([A-Za-z0-9]*)\) *STATUS\(([A-Za-z]*)\)"

    def __init__(self, name, queues):
        self.name = name
        self.commands_pending = []
        self.queues = queues
        self.mqsc_cmds = []

    def execute_mqsc_script(self):
        print("execute mqsc script")

    def generate_mqsc_script(self):
        print("execute mqsc script")

    def run_isolated_mqsc_cmd(self, out, cmd):
        cmd = "echo '%s' | %s %s" % (
            cmd,
            IMPORTANT_BINARIES_LOCATION["RUNMQSC"],
            self.name
            )
        output = execute_raw_command(cmd)
        stdout = retrieve_stdout(output)
        open(out, 'w').write(stdout)

    def parse_dspmq(self):
        cmd = IMPORTANT_BINARIES_LOCATION['DSPMQ']
        result = execute_command(cmd)
        matches = []
        for line in result.stdout:
            match = re.match(self.DSPMQ_REGEX, line)
            if match:
                module.log("MATCH : %s" % match)
                matches.append(list(match.groups()))
        module.log("groups : %s" % matches)
        return matches

    def exists(self):
        parsed_dspmq = self.parse_dspmq()
        module.log("DSPMQ RESULTS : %s" % str(parsed_dspmq))
        if parsed_dspmq:
            for entry in parsed_dspmq:
                module.log("ENTRY : %s" % str(entry))
                if self.name in entry:
                    return True

    def create(self):
        cmd = shlex.split("%s %s" % (IMPORTANT_BINARIES_LOCATION['CRTMQM'], self.name))
        output = execute_command(cmd)
        print_command_output(output)

    def start(self):
        cmd = shlex.split("%s %s" % (IMPORTANT_BINARIES_LOCATION['STRMQM'], self.name))
        output = execute_command(cmd)
        print_command_output(output)

    def stop(self):
        cmd = shlex.split("%s -w %s" % (IMPORTANT_BINARIES_LOCATION['ENDMQM'], self.name))
        output = execute_command(cmd)
        print_command_output(output)

    def delete(self):
        cmd = shlex.split("%s %s" % (IMPORTANT_BINARIES_LOCATION['DLTMQM'], self.name))
        output = execute_command(cmd)
        print_command_output(output)

    def create_queues(self):
        for queue_config in self.queues:
            queue = Queue(queue_config["name"], queue_config["type"], queue_config["opts"])
            self.run_isolated_mqsc_cmd('/tmp/queues.out',queue.generate_define_cmd())

    def display_queues(self):
        self.run_isolated_mqsc_cmd('/tmp/display_queues.out',"DISPLAY QUEUE(*)")

    def display_channels(self):
        self.run_isolated_mqsc_cmd('/tmp/display_channels.out', "DISPLAY CHANNEL(*)")


class Queue():
    QTYPES = [
        'QLOCAL',
        'QREMOTE',
        'QALIAS',
        'QMODEL'
    ]

    VALID_ATTRIBUTES = {
        "QLOCAL" : [
            'ACCTQ', 'BOQNAME', 'BOTHRESH',
            'CLCHNAME', 'CLUSNL', 'CLUSTER',
            'CLWLPRTY', 'CLWLRANK', 'CLWLUSEQ',
            'CUSTOM', 'DEFBIND', 'DEFPRESP',
            'DEFPRTY', 'DEFPSIST', 'DEFREADA',
            'DEFSOPT', 'DESCR', 'DISTL',
            'FORCE', 'GET', 'IMGRCOVQ',
            'INDXTYPE', 'INITQ', 'LIKE',
            'MAXDEPTH', 'MAXMSGL', 'MONQ',
            'MSGDLVSQ', 'NOREPLACE', 'NPMCLASS',
            'PROCESS', 'PROPCTL', 'PUT',
            'QDEPTHHI', 'QDEPTHLO', 'QDPHIEV',
            'QDPLOEV', 'QDPMAXEV', 'QSVCIEV',
            'QSVINT', 'REPLACE', 'RETINTVL',
            'SCOPE', 'SHARE', 'NOSHARE',
            'STATQ', 'TRIGDATA', 'TRIGDPTH',
            'TRIGGER', 'NOTRIGGER', 'TRIGMPRI',
            'TRIGTYPE', 'USAGE'
        ],
        "QMODEL" : [
            'ACCTQ', 'BOQNAME', 'BOTHRESH',
            'CUSTOM', 'DEFPRESP', 'DEFPRTY',
            'DEFPSIST', 'DEFREADA', 'DEFSOPT',
            'DEFTYPE', 'DESCR', 'DISTL',
            'GET', 'INDXTYPE', 'INITQ',
            'LIKE', 'MAXDEPTH', 'MAXMSGL',
            'MONQ', 'MSGDLVSQ', 'NOREPLACE',
            'NPMCLASS', 'PROCESS', 'PROPCTL',
            'PUT', 'QDEPTHHI', 'QDEPTHLO',
            'QDPHIEV', 'QDPLOEV', 'QDPMAXEV',
            'QSVCIEV', 'QSVCINT', 'REPLACE',
            'RETINTVL', 'SHARE', 'NOSHARE',
            'STATQ', 'TRIGDATA', 'TRIGDTPH',
            'TRIGGER', 'NOTRIGGER', 'TRIGMPRI',
            'TRIGTYPE', 'USAGE'
        ],
        "QALIAS" : [
            'CLUSNL', 'CLUSTER', 'CLWLPRTY',
            'CLWLRANK', 'CUSTOM', 'DEFBIND',
            'DEFPRESP', 'DEFPRTY', 'DEFPSIST',
            'DEFREADA', 'DESCR', 'FORCE',
            'GET', 'LIKE', 'NOREPLACE',
            'PROPCTL', 'PUT', 'REPLACE',
            'SCOPE', 'TARGET', 'TARGQ',
            'TARGTYPE'
        ],
        "QREMOTE" : [
            'CLUSNL', 'CLUSTER', 'CLWLPRTY',
            'CLWLRANK', 'CUSTOM', 'DEFBIND',
            'DEFPRESP', 'DEFPRTY', 'DEFPSIST',
            'DESCR', 'FORCE', 'LIKE',
            'NOREPLACE', 'PUT', 'REPLACE',
            'RNAME', 'RQMNAME', 'SCOPE',
            'XMITQ'
        ]
    }

    def __init__(self, name, qtype, options):
        if qtype in self.QTYPES:
            self.type = qtype
        else:
            raise Exception("Unknown Queue type")
        self.name = name
        self.options = options
        self.args = []
        print("class for a queue")

    def generate_define_cmd(self):
        cmd = "DEFINE %s(%s)" % (self.type, self.name)
        if self.options:
            self.handle_options()
        if len(self.args) > 0:
            for arg in self.args:
                cmd += " %s" % arg
        return cmd

    def generate_alter_cmd(self):
        print("function that will generate an alter string from known queues")

    def handle_option(self, attribute, value):
        print("function that will generate the argument to define")

    def handle_options(self):
        if self.VALID_ATTRIBUTES.get(self.type, False):
            for option in self.options:
                if option in self.VALID_ATTRIBUTES[self.type]:
                    self.handle_option(option, self.options[option])




class Channel():

    def __init__(self):
        print("class for a channel")

    def generate_defined_cmd(self):
        print("class to generate the channel objects define string")


# ================================================================================
# DEVNOTE:
# possible refactoring into a class with static methods that will only execute commands and
# manage the interactions with the underlaying system

def print_command_output(pipe):
    stdout = ""
    for line in pipe.stdout:
        stdout += line
    module.log(stdout)

def retrieve_stdout(cmd_result):
    stdout = ""
    for line in cmd_result.stdout:
        stdout += line
    return stdout

def execute_command(cmd):
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        output.wait()
        return output

def execute_raw_command(cmd):
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        output.wait()
        return output

# ================================================================================
# DEVNOTE:
# This portions contains the functions pertaining to the presence of the necessary binaries on the FS
# It will search the PATH, conventional locations and then fail if the binaries are not found.
# I plan to add arguments that could be passed to the module to specify where to find these binaries (normally /opt/mqm/bin)

def validate_binaries():
    for binary in IMPORTANT_BINARIES_LOCATION:
        binary_location = IMPORTANT_BINARIES_LOCATION[binary]
        if not os.path.exists(binary_location):
            module.warn("Missing mq binary : %s, the module may fail"\
                % binary_location)


def run_module():
# QUEUE MQSC COMMANDS :  https://www.ibm.com/support/knowledgecenter/SSFKSJ_9.1.0/com.ibm.mq.ref.adm.doc/q085690_.htm
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        qmgr=dict(required=True, type='dict', options=dict(
            name=dict(required=True, type='str'),
            state=dict(type='str', default='present',choices=['present', 'absent']),
            queues=dict(type='list', elements='dict', options=dict(
                name=dict(required=True, type='str'),
                type=dict(required=True, type='str', choices=["QLOCAL", "QMODEL", "QALIAS", "QREMOTE"]),
                state=dict(type='str', default='present', choices=['present', 'absent']),
                desc=dict(type='str'),
                opts=dict(type='dict', options=dict(
                  ACCTQ=dict(type='str', choices=['ON', 'OFF', 'QMGR']),
                  BOQNAME=dict(type='str'),
                  BOTHRESH=dict(type='int'),
                  CLCHNAME=dict(type='str'),
                  CLUSNL=dict(type='list', elements='str'),
                  CLUSTER=dict(type='str'),
                  CLWLPRTY=dict(type='int'),
                  CLWLRANK=dict(type='int'),
                  CLWLUSEQ=dict(type='str', choices=['QMGR', 'ANY', 'LOCAL','*','']),
                  CUSTOM=dict(type='str'),
                  CAPEXPRY=dict(type='int'),
                  DEFBIND=dict(type='str', choice=['OPEN', 'NOTFIXED', 'GROUP']),
                  DEFPRESP=dict(type='str', choice=['SYNC', 'ASYNC']),
                  DEFPRTY=dict(type='int'),
                  DEFPSIST=dict(type='str', choices=['NO','YES']),
                  DEFREADA=dict(type='str', choices=['NO', 'YES', 'DISABLED']),
                  DEFSOPT=dict(type='str', choices=['EXCL', 'SHARED']),
                  DEFTYPE=dict(type='str', choices=['PERMDYN', 'TEMPDYN']),
                  DISTL=dict(type='str', choices=['YES', 'NO']),
                  FORCE=dict(type='bool'),
                  GET=dict(type='str', choices=['ENABLED', 'DISABLED']),
                  IMGRCOVQ=dict(type='str', choices=['YES', 'NO', 'QMGR']),
                  INITQ=dict(type='str'),
                  LIKE=dict(type='str'),
                  MAXDEPTH=dict(type='int'),
                  MAXMSGL=dict(type='int'),
                  MONQ=dict(type='str', choices=['QMGR', 'OFF', 'LOW', 'MEDIUM', 'HIGH']),
                  MSGDLVSQ=dict(type='str', choices=['PRIORITY', 'FIFO']),
                  NPMCLASS=dict(type='str', choices=['NORMAL', 'HIGH']),
                  PROCESS=dict(type='str'),
                  PROPCTL=dict(type='str', choices=['ALL', 'FORCE', 'COMPAT', 'NONE']),
                  PUT=dict(type='str', choices=['ENABLED', 'DISABLED']),
                  QDEPTHHI=dict(type='int'),
                  QDEPTHLO=dict(type='int'),
                  QDPHIEV=dict(type='str', choices=['ENABLED', 'DISABLED']),
                  QDPLOEV=dict(type='str', choices=['ENABLED', 'DISABLED']),
                  QDPMAXEV=dict(type='str', choices=['ENABLED', 'DISABLED']),
                  QSVCIEV=dict(type='str', choices=['HIGH', 'OK', 'NONE']),
                  QSVCINT=dict(type='int'),
                  REPLACE=dict(type='bool'),
                  NOREPLACE=dict(type='bool'),
                  RETINTVL=dict(type='int'),
                  RNAME=dict(type='str'),
                  RQMNAME=dict(type='str'),
                  SCOPE=dict(type='str', choices=['QMGR', 'CELL']),
                  SHARE=dict(type='bool'),
                  NOSHARE=dict(type='bool'),
                  STATQ=dict(type='str', choices=['QMGR', 'ON', 'OFF']),
                  TARGET=dict(type='str'),
                  TARGTYPE=dict(type='str'),
                  TRIGDATA=dict(type='str'),
                  TRIGDPTH=dict(type='int'),
                  TRIGGER=dict(type='bool'),
                  NOTRIGGER=dict(type='bool'),
                  TRIGMPRI=dict(type='int'),
                  TRIGTYPE=dict(type='str', choices=['FIRST', 'EVERY', 'DEPTH', 'NONE']),
                  USAGE=dict(type='str', choices=['NORMAL', 'XMITQ']),
                  XMITQ=dict(type='str')
                ))
            )),
            channels=dict(type='list', elements='dict', option=dict(
                name=dict(required=True, type='str'),
                type=dict(required=True, type='str'),

            ))
        ))
    )

    global module

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    qmgr_name = module.params['qmgr']['name']
    qmgr_state = module.params['qmgr']['state']
    qmgr_queues = module.params['qmgr']['queues']
    qmgr = QMGR(qmgr_name, qmgr_queues)
    if qmgr_state == "present":
        if not qmgr.exists():
            qmgr.create()
            qmgr.start()
            qmgr.create_queues()
            qmgr.display_queues()
            result['changed'] = True

    if qmgr_state == "absent":
        if qmgr.exists():
            qmgr.stop()
            qmgr.delete()
            result['changed'] = True

    if module.check_mode:
        module.exit_json(**result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()