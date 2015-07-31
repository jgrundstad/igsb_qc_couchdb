import argparse
import datetime
import requests
import requests.auth
from couchdbreq import Server
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
        md5sum_list = list()
        for row in rows:
            md5sum_list.append(row.get('value'))
        return md5sum_list

def main():
    parser = argparse.ArgumentParser(description="interact with the " + \
                                                 "hgac_md5sum couchdb.")
    parser.add_argument("-u", "--username", required=True,
                        help="username", action='store', dest='u')
    parser.add_argument("-p", "--password", required=True,
                        help="password", action='store', dest='p')
    args = parser.parse_args()
    print args


if __name__ == '__main__':
    main()