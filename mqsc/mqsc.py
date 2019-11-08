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


class QMGR():
    def __init__(self, name):
        self.name = name
        self.commands_pending = []

    def exists(self):
        cmd = shlex.split((IMPORTANT_BINARIES_LOCATION['DSPMQ']))
        result = execute_command(cmd)
        result_stdout = retrieve_stdout(result)
        if self.name in result_stdout:
            return True

    def create(self):
        cmd = shlex.split("%s %s" % (IMPORTANT_BINARIES_LOCATION['CRTMQM'], self.name))
        self.commands_pending.append(cmd)

    def start(self):
        cmd = shlex.split("%s %s" % (IMPORTANT_BINARIES_LOCATION['STRMQM'], self.name))
        self.commands_pending.append(cmd)
    
    def stop(self):
        cmd = shlex.split("%s %s" % (IMPORTANT_BINARIES_LOCATION['ENDMQM'], self.name))
        self.commands_pending.append(cmd)
    
    def delete(self):
        cmd = shlex.split("%s %s" % (IMPORTANT_BINARIES_LOCATION['DLTMQM'], self.name))
        self.commands_pending.append(cmd)

    def commit(self):
        execute_commands(self.commands_pending)


def retrieve_stdout(cmd_result):
    stdout = ""
    for line in cmd_result.stdout:
        stdout += line
    return stdout

def execute_commands(cmds):
    return_code = 0
    for c in cmds:
        p = subprocess.Popen(c, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = p.communicate()
        yield result
        return_code = p.returncode
        if return_code != 0:
            break

def execute_command(cmd):
    try:
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        return output
    except Exception:
        module.fail_json(msg=traceback.format_exc())


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
        qmgr=dict(required=True, type='list', elements='dict', options=dict(
            name=dict(required=True, type='str'),
            state=dict(type='str', default='present',choices=['present', 'absent']),
            queues=dict(type='list', elements='dict', options=dict(
                name=dict(required=True, type='str'),
                type=dict(required=True, type='str', choices=["QLOCAL", "QMODEL", "QALIAS", "QREMOTE"]),
                state=dict(required=True, type='str', default='present', choices=['present', 'absent']),
                desc=dict(type='str'),
                opts=dict(type='list', elements='dict', options=dict(
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
        )),
        name=dict(type='str', required=True),
        new=dict(type='bool', required=False, default=False)
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

    qmgr_name = module.params['qmgr'][0]['state']
    qmgr_state = module.params['qmgr'][0]['name']
    qmgr = QMGR(qmgr_name)
    if qmgr_state == "present":
        if not qmgr.exists():
            qmgr.create()
            qmgr.start()
            qmgr.commit()
            result['changed'] = True

    if qmgr_state == "absent":
        if qmgr.exists():
            qmgr.stop()
            qmgr.delete()
            qmgr.commit()
            result['changed'] = True

    if module.check_mode:
        module.exit_json(**result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()