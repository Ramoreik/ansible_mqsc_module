#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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
# Pass in a message
- name: Test with a message
  my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_test:
    name: fail me
'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
    returned: always
message:
    description: The output message that the test module generates
    type: str
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule

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

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['original_message'] = module.params['name']
    result['message'] = 'goodbye'

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['new']:
        result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()