CouchDB ViewStrap
=================

Simple project to create databases and views for [CouchDB](https://couchdb.apache.org/) from [YAML](http://yaml.org/) configuration files.

Requires [Python](http://www.python.org/) 2.6 and above or 3.x

## Installation

It is preferrable to use [virtualenv](https://github.com/pypa/virtualenv), but if you do not mind damaging your environment (or are using [Docker](http://www.docker.io/)):
```
$ pip install -r requirements.pip
```

## Usage

```
$ python couchvs/couchvs.py  --username guest --password guest examples/*.yaml
```

```
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
```

## Configuration

Configuration is stored in the [YAML](http://yaml.org/) format. One database per file. There is currently no support for recursively directory structures.
See [example-database.yaml](https://github.com/hekar/couchdb-viewstrap/blob/master/examples/example-database.yaml)
```
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
```
