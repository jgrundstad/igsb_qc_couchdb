"""
Interact with the hgac_md5sum couchdb

Usage:
    hgac_md5.py add -u USERNAME -p PASSWORD -f FILENAME -m MD5SUM
    hgac_md5.py get -u USERNAME -p PASSWORD -f FILENAME

Options:
    -u USERNAME     couchdb username
    -p PASSWORD     couchdb password
    -f FILENAME     filename
    -m MD5SUM       calculated md5sum
"""
import datetime
from docopt import docopt
import requests
import requests.auth
from couchdbreq import Server
import sys

__author__ = 'A. Jason Grundstad'


class HGACmd5:

    def __init__(self, username=None, password=None):
        auth = requests.auth.HTTPBasicAuth(username, password)
        session = requests.session()
        session.auth = auth
        server = Server(uri="http://128.135.219.167:5984",
                        session=session)
        self.db = server.get_db('hgac_md5', is_verify_existance=True)

    def add_md5(self, filename=None, md5sum=None):
        doc = {"filename": filename,
               "md5sum": md5sum,
               "upload_date": str(datetime.datetime.now())}
        self.db.save_doc(doc)

    def get_md5sum_by_filename(self, filename=None):
        rows = self.db.view('hgac_md5/md5sum_by_filename', key=filename)
        md5sum = ''

        if rows.count() > 1:
            err_string = "ERROR: More than one md5sum retrieved for " + \
                "filename: {}"
            print >>sys.stderr, err_string.format(filename)
            for row in rows:
                print "{}  {}".format(row.get('value'), row.get('key'))
            sys.exit(1)

        for row in rows:
            md5sum = row.get('value')
        return md5sum

def main():
    args = docopt(__doc__)
    h = HGACmd5(username=args['-u'], password=args['-p'])
    if args['get']:
        print >>sys.stdout, h.get_md5sum_by_filename(args['-f'])
    if args['add']:
        h.add_md5(filename=args['-f'], md5sum=args['-m'])


if __name__ == '__main__':
    main()