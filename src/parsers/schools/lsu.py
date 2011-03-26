#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        lsu.py
# Purpose:     Contains all parsing functions for Louisiana State University
#              Bookstore
#
# Author:      Andre Wiggins
#
# Created:     03/19/2011
# Copyright:   (c) Andre Wiggins, Jacob Marsh, Andrew Stewart 2011
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

import urllib2
import BeautifulSoup
from pprint import pprint


def getTermID(season, year):
    url = 'http://lsu.bncollege.com/webapp/wcs/stores/servlet/TBWizardView?catalogId=10001&storeId=19057&langId=-1'
    soup = BeautifulSoup.BeautifulSoup(urllib2.urlopen(url))
    select = soup.find('select')
    
    options = {}
    for option in select.findAll('option'):
        if option['value']:
            options[option.string.lower()] = option['value']
    
    term = str(season.lower())+' '+str(year).lower()
    return options.get(term, None)


def getTextbooks(courses):
    pass


def main():
    print getTermID('Fall', 2011)


if __name__ == '__main__':
    main()