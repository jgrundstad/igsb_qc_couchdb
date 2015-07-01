"""
Update a json document with a .json file (format included in template.json)

Usage:
    update_document.py -c credentials (-f json_file | -j json_string) [-d dry-run]

Options:
    -c credentials  'user:password'
    -f json_file    .json Document file
    -j json_string  "{'example': {'json_string': 'things'}}"
    -d dry-run      Run without committing any changes to Database
"""
__author__ = 'jgrundst'
import igsb_qc_couchdb_util as qc_util
from docopt import docopt
import json
import ast
import pprint


class DocumentUpdater():

    def __init__(self, credentials, json_string=None, json_file=None):
        if(json_file):
            with open(json_file, 'r') as js_f:
                self.json_obj = json.load(js_f)
        else:
            self.json_obj = ast.literal_eval(json_string)

        #pprint.pprint(self.json_obj)
        self.readgroup = self.json_obj['READGROUP']
        print "Working with readgroup: {}".format(self.readgroup)
        self.qc_couch_db = qc_util.connect_to_db(
            'https://128.135.219.167:6984', credentials, 'igsb_qc_test')



    def _find_doc_by_readgroup(self):
        pass


def main():
    args = docopt(__doc__)
    print args
    DU = DocumentUpdater(json_string=args['-j'], json_file=args['-f'])

if __name__ == '__main__':
    main()
