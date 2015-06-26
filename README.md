# igsb_qc_couchdb
Tools for interacting with the IGSB alignment QC CouchDB

```bash
View, and edit igsb_qc CouchDB documents.

Usage:
    edit_upload_json.py [-s server] -d database -c credentials -b BionimbusID
        [-D delete_fields] [-A add_fields]

Options:
    -s server            Server name [default: http://127.0.0.1:5984]
    -d database          CouchDB database name
    -c credentials       username:password
    -b BionimbusID       e.g. 2014-2232
    -D delete_fields     comma-delimited list of field names
    -A add_fields        comma-delimited list of field:value pairs
```
