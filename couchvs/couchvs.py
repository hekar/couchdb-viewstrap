#!/usr/bin/env python
"""
    Copyright (c) 2014 Hekar Khani

    This software is provided 'as-is', without any express or implied
    warranty. In no event will the authors be held liable for any damages
    arising from the use of this software.

    Permission is granted to anyone to use this software for any purpose,
    including commercial applications, and to alter it and redistribute it
    freely, subject to the following restrictions:

       1. The origin of this software must not be misrepresented; you must not
       claim that you wrote the original software. If you use this software
       in a product, an acknowledgment in the product documentation would be
       appreciated but is not required.

       2. Altered source versions must be plainly marked as such, and must not be
       misrepresented as being the original software.

       3. This notice may not be removed or altered from any source
       distribution.
"""

import sys
import argparse
import logging
from databaseview import database_view_from_file
from documentstore import CouchConnectionFactory, DocumentStore

def parse_args(args):
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(args[0], description='Write Views to CouchDB')
    parser.add_argument('--url', help='CouchDB server url (ie. http://localhost:5984/)',
                        default='http://localhost:5984/')
    parser.add_argument('--host', help='CouchDB server hostname (ie. localhost:5984)',
                        default='localhost:5984')
    parser.add_argument('--username', help='CouchDB server username (ie. guest)')
    parser.add_argument('--password', help='CouchDB server password (ie. guest)')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-q', '--quiet', action='store_true')
    parser.add_argument('files', metavar='<file>', type=file, nargs='+',
                   help='Files to scan')
                   
    return parser.parse_args()

def setup_logger(args):
    if not args.quiet:
        logging.basicConfig(level = logging.INFO)
        
    if args.verbose:
        logging.basicConfig(level = logging.DEBUG)
    
def main(args):
    args = parse_args(args)
    setup_logger(args)
    
    for file in args.files:
        view = database_view_from_file(file)
        connection = CouchConnectionFactory(args.url, 
            args.host, args.username, args.password).connect().get()
        
        DocumentStore(connection, view).update()
    

if __name__ == '__main__':
    main(sys.argv)
