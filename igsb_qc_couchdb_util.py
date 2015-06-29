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
import ast
from docopt import docopt
from couchdbreq import Server
import requests
import requests.auth
import pprint
import json
import sys


def connect_to_server(server_name, credentials):
    """
    Connect to provided server with the given credentials
    :param server_name: e.g. 'http://127.0.0.1:5984'
    :param credentials: e.g. 'name:password'
    :return: couchdbreq server object
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
    """
    This does what you think it does.
    :param db: CouchDB obj
    :param doc: document
    :return:
    """
    print "Deleting document {}".format(doc['_id'])
    try:
        db.delete_doc(doc)
    except Exception, e:
        print >>sys, "Error when deleting document: {}".format(doc)
        raise


def view_docs_by_bnid(db, bnid):
    """
    Access the 'all' view.  Returns all docs containing the given Bionimbus_id
    :param db: CouchDB obj
    :param bnid: Bionimbus ID
    :return:
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
    :param rows: set of documents (returned from a view)
    :param db: CouchDB obj
    :return:
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


def delete_field(db, doc, field, subfield=None):
    """
    Delete a field from a given CouchDB document
    :param db: CouchDB obj
    :param doc: document
    :param field: field names
    :param subfield: one level deep, for now. intended for coverage stats
    :return:
    """
    try:
        if subfield:
            doc[field].pop(subfield, None)
        else:
            doc.pop(ast.literal_eval(field), None)
        db.save_doc(doc)
    except Exception, e:
        print >>sys.stderr, "Error occurred when deleting field {} " + \
                            "from doc: {}".format(field, json.dumps(doc))
        if subfield:
            print >>sys.stderr, "Subfield detected: {}".format(subfield)
        raise


def add_field_payload(db, doc, field, payload, is_coverage=False):
    """
    Add dict payload to new field in the given document
    :param db: couchdb DB object
    :param doc: document
    :param field: new field name
    :param payload: dict payload
    :param is_coverage: boolean, is this coverage data?
    :return: None
    """
    try:
        if is_coverage:
            if 'coverage' not in doc:
                doc['coverage'] = {}
            doc['coverage'][field] = ast.literal_eval(payload)
        else:
            doc[field] = ast.literal_eval(payload)
        db.save_doc(doc)
    except Exception, e:
        print >>sys.stderr, "Error occurred when adding payload: {} to field: " + \
                            "{} to doc: {}".format(
            json.dumps(payload), field, json.dumps(doc))
        print >>sys.stderr, "Coverage data: {}".format(is_coverage)
        raise


def main():
    args = docopt(__doc__)
    bnid = args['-b']
    server_name = args['-s']
    db_name = args['-d']
    credentials = args['-c']

    print "Connect to db: {} on server: {}".format(db_name, server_name)
    server = connect_to_server(server_name, credentials)
    db = server.get_db(db_name)

    print "Searching for document with BNid: {}".format(bnid)
    rows = view_docs_by_bnid(db, bnid)

    # search through and remove all documents that appear to be duplicates
    #all_docs = db.view('igsb_qc/all', descending=True)
    #duplicate_docs = find_duplicate_docs(all_docs, db)
    #for d in duplicate_docs:
    #    delete_document(db, d)

    #delete_fields = args['-D']
    #print "Delete these fields: {}".format(delete_fields)
    #add_fields_values = args['-A']
    #print "Add these field:values {}".format(add_fields_values)


if __name__ == '__main__':
    main()
