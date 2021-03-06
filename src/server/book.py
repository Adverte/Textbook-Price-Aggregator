#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        book.py
# Purpose:     Contains all Request Handlers pertaining to book request
#
# Author:      Andre Wiggins
#
# Created:     04/07/2011
# Copyright:   (c) Jacob Marsh, Andrew Stewart, Andre Wiggins 2011
# License:
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#-------------------------------------------------------------------------------

import server
import parsers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import parsers.retailers.halfdotcom as halfdotcom

class BookPage(webapp.RequestHandler):
    
    def get(self):
        url = self.request.get('url')
        retailer_name = self.request.get('retailer')
        
        if url and retailer_name:
            retailer = parsers.import_parser(retailer_name)
            isbn = retailer.lookup_isbn(url).isbn13
            
            newurl = '/book/%s' % isbn
            self.redirect(newurl)
            return
            
        elif url or retailer_name:
            msg = "Incorrect syntax: /book a valid url and url-retailer."
            url = "/error/400?msg=%s" % msg
            self.redirect(url)

        else:
            isbn = self.request.path.rstrip('/').split('/')[-1]
            if isbn == 'book':
                msg = "Incorrect syntax: /book requires an isbn."
                url = "/error/400?msg=%s" % msg
                self.redirect(url)
            else:        
                path = '../static/templates/book.html'
                self.response.out.write(template.render(path, {}, True))   
    

class TextbookLookup(webapp.RequestHandler):
    
    def get(self):
        isbn = self.request.path.rstrip('/').split('/')[-1]
        textbook = server.getjson(halfdotcom.lookup_isbn(isbn))
        
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(textbook)
    

class TextbookListingsLookup(webapp.RequestHandler):
    
    def get(self):
        retailer_name, isbn = self.request.path.rstrip('/').split('/')[-2:]
        retailer = parsers.import_parser(retailer_name)
        
        listings = ''
        if retailer:
            listings = server.getjson(retailer.lookup_listings(isbn))
        
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(listings)
        