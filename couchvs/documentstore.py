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
import couchdb
import base64
import httplib2 as hl
import json
import logging
from urlparse import urlparse

_log = logging.getLogger(__name__)

class CouchConnectionFactory():
    """Create a connection for the CouchDB database"""
    
    def __init__(self, url, host, username, password):
        """Initialize connection factory

        :param url: the url of the CouchDB server (ie. http://localhost:5984/)
        :type url: str
        :param host: the host of the CouchDB server (ie. localhost:5984)
        :type host: str
        :param username: the username of the CouchDB server (ie. guest)
        :type username: str
        :param password: the password of the CouchDB server (ie. guest)
        :type password: str
        """
        
        self.url = url
        self.host = host
        self.username = username
        self.password = password
        
        self.__couch = None
    
    def __del__(self):
        """Equivalent to close(). Close the connection"""
        
        self.close()
    
    def connect(self):
        """Connect to the CouchDB database"""
        
        self.__couch = couchdb.Server(self.url)
        self.__couch.resource.credentials = (self.username, self.password)
        return self
        
    def __created(self):
        """Is there a connection created"""
        
        return self.__couch is not None
        
    def close(self):
        """Equivalent to __del__(). Close the connection"""
        
        del self.__couch
        
    def get(self):
        """Get the connection. Return 'None' when no connection"""
        if not self.__created():
            return None

        return self.__couch

class DocumentStore():
    def __init__(self, connection, databaseview):
        """
        :param connection: Connection to the respective CouchDB Server
        :type connection: couchdb.Server
        :param databaseview: Connection to the respective CouchDB Server
        :type databaseview: couchvs.DatabaseView
        """
        self.__databaseview = databaseview
        self.__connection = connection
    
        
    def merge(self):
        raise NotImplementedError()
    
    def update(self):
        """Update the respective database with the required views.
        The database is created if it does not exist"""
        dv = self.__databaseview
        c = self.__connection
        
        db = None
        try:
            db = c[dv.database]
        except couchdb.http.ResourceNotFound:
            db = c.create(dv.database)

        self.__write_views(dv, 'POST')
        
    def __write_views(self, databaseview, method='POST'):
        """Write views to the database
        
        :param databaseview: Connection to the respective CouchDB Server
        :type databaseview: couchvs.DatabaseView
        :param method: 'POST' to insert, 'PUT' to update
        :type method: str
        """
        global _log
        
        dv = databaseview
        c = self.__connection
        
        url = '%s%s/' % (c.resource.url, dv.database)
        
        body = json.dumps({
          '_id': ('_design/%s' % dv.name),
          'language': dv.language,
          'views': dv.views
        }, indent=4, separators=(',', ': '), sort_keys=True)
        
        username, password = (c.resource.credentials)
        
        def http_view_create(url, username, password):
            h = hl.Http('.cache')
            parsed_url = urlparse(url)
            headers = {
                'Content-type': 'application/json',
                'Host': parsed_url.netloc,
                'Referer': '%s%s/' % (parsed_url.scheme, parsed_url.netloc)
            }
            
            if (username and password) is not None:
                auth = base64.encodestring('%s:%s' % (username, password))
                headers['Authorization'] = 'Basic %s' % (auth)
            
            resp, content = h.request(url, 
                method, body=body, headers=headers)
                
            return (resp, content)
        
        resp, content = http_view_create(url, username, password)
        
        _log.info(("%s\n\n%s" % (resp, content)).strip())
