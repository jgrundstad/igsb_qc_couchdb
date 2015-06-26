"""
View, and edit igsb_qc CouchDB documents.

Usage:
    igsb_qc_couchdb_util.py [-s server] -d database -c credentials -b BionimbusID
        [-D delete_fields] [-A add_fields]

Options:
    -s server            Server URI [default: http://127.0.0.1:5984]
    -d database          CouchDB database name
    -c credentials       username:password
    -b BionimbusID       e.g. 2014-2232
    -D delete_fields     comma-delimited list of field names
    -A add_fields        comma-delimited list of field:value pairs
"""
__author__ = 'A. Jason Grundstad'
from docopt import docopt
from couchdbreq import Server
import requests
import requests.auth
import pprint


def connect_to_db(server_name, credentials):
    """ Returns server object used to access db
    """
    u = credentials.split(':')[0]
    p = credentials.split(':')[1]
    auth = requests.auth.HTTPBasicAuth(u, p)
    session = requests.session()
    session.auth = auth
    print "Session auth: {}".format(auth)
    server = Server(uri=server_name, session=session)
    print "Connected!\n{}".format(server.get_info())
    return server

def delete_document(db, doc):
    """ Careful
    """
    print "Deleting document {}".format(doc['_id'])
    db.delete_doc(doc)


def view_docs_by_bnid(db, bnid):
    """ Access the 'all' view.  Returns all docs containing Bionimbus_id
    """
    rows = db.view('igsb_qc/all', key=bnid, descending=True)
    pp = pprint.PrettyPrinter(indent=4)
    for row in rows:
        pp.pprint(row['value'])
        print row['value']['_id']
    return rows

def find_duplicate_docs(rows, db):
    """
    find docs that match on 'fields', disregard analysis date fields
    """
    fields = ('Bionimbus_id', 'Date', 'Machine', 'Run', 'BarCode', 'Lane',
              'aligned_bp_ot', 'total_reads', 'target_size')
    docs = []
    dup_documents = []

    for row in rows:
        document_values = ''
        for field in fields:
            document_values += row['value'][field] + '|'
        if document_values not in docs:
            docs.append(document_values)
        else:
            print "Candidate for deletion: {}".format(row['value']['_id'])
            dup_documents.append(db.get_doc(row['value']['_id']))
            print "** {}".format(document_values)
        print document_values

    print "Encountered {} documents that appear to be duplicates".format(len(dup_documents))
    return dup_documents

def main():
    args = docopt(__doc__)
    bnid = args['-b']
    server_name = args['-s']
    db_name = args['-d']
    credentials = args['-c']

    print "Connect to db: {} on server: {}".format(db_name, server_name)
    server = connect_to_db(server_name, credentials)
    db = server.get_db(db_name)

    print "Searching for document with BNid: {}".format(bnid)
    rows = view_docs_by_bnid(db, bnid)

    # search through and remove all documents that appear to be duplicates
    all_docs = db.view('igsb_qc/all', descending=True)
    duplicate_docs = find_duplicate_docs(all_docs, db)
    for d in duplicate_docs:
        delete_document(db, d)

    #delete_fields = args['-D']
    #print "Delete these fields: {}".format(delete_fields)
    #add_fields_values = args['-A']
    #print "Add these field:values {}".format(add_fields_values)


if __name__ == '__main__':
    main()
