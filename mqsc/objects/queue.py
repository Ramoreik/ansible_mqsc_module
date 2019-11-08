
QTYPES = [
    'QLOCAL',
    'QREMOTE',
    'QALIAS',
    'QMODEL'
]

QLOCAL_VALID_ATTRIBUTES = [
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
]


QMODEL_VALID_ATTRIBUTES = [
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
]


QALIAS_VALID_ATTRIBUTES = [
    'CLUSNL', 'CLUSTER', 'CLWLPRTY',
    'CLWLRANK', 'CUSTOM', 'DEFBIND', 
    'DEFPRESP', 'DEFPRTY', 'DEFPSIST',
    'DEFREADA', 'DESCR', 'FORCE',
    'GET', 'LIKE', 'NOREPLACE',
    'PROPCTL', 'PUT', 'REPLACE',
    'SCOPE', 'TARGET', 'TARGQ',
    'TARGTYPE'
]


QREMOTE_VALID_ATTRIBUTES = [
    'CLUSNL', 'CLUSTER', 'CLWLPRTY',
    'CLWLRANK', 'CUSTOM', 'DEFBIND',
    'DEFPRESP', 'DEFPRTY', 'DEFPSIST',
    'DESCR', 'FORCE', 'LIKE', 
    'NOREPLACE', 'PUT', 'REPLACE',
    'RNAME', 'RQMNAME', 'SCOPE',
    'XMITQ'
]


class queue():
    def __init__(self, qmgr, qtype, name):
        self.qmgr = qmgr
        self.name = name 
        if qtype in QTYPES:
            self.qtype = qtype
    
    def generate_mqsc(self):
        print("Generates mqsc line based on the queue to create")

    def fetch_current(self):
        print("verify if queue exists and then gets mqsc output")
    
    def parse_current(self):
        print("parse output from the fetched current if it existed")

    def display(self):
        print("function to display the queue")
    
        
        

