CouchDB ViewStrap
=================

Create databases and views for CouchDB from YAML configuration

Requires Python >2.6 and 3.x

h1. Usage
...
$ python couchvs/couchvs.py --help
usage: couchvs/couchvs.py [-h] [--url URL] [--host HOST] [--username USERNAME]
                          [--password PASSWORD] [-v] [-q]
                          <file> [<file> ...]

Write Views to CouchDB

positional arguments:
  <file>               Files to scan

optional arguments:
  -h, --help           show this help message and exit
  --url URL            CouchDB server url (ie. http://localhost:5984/)
  --host HOST          CouchDB server hostname (ie. localhost:5984)
  --username USERNAME  CouchDB server username (ie. guest)
  --password PASSWORD  CouchDB server password (ie. guest)
  -v, --verbose
  -q, --quiet
...


h1. Configuration example
...
database: example-database
design: example-design
language: javascript
views:
    example-view:
        map: |
            function(doc) {
                if (doc.key.contains('hello'))
                    emit(doc.key, doc);
            }
        reduce: |
            function(key, values) {
                return true;
            }
    second-view:
        map: |
            function(test) {
                emit(doc.key, doc);
            }
...
