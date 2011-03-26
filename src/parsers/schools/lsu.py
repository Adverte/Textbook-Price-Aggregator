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


import string
import urllib2
import BeautifulSoup


def get_terms():
    url = 'http://lsu.bncollege.com/webapp/wcs/stores/servlet/TBWizardView?catalogId=10001&storeId=19057&langId=-1'
    soup = BeautifulSoup.BeautifulSoup(urllib2.urlopen(url))
    
    options = {}
    for option in soup.find('select').findAll('option'):
        if option['value']:
            options[option.string.lower()] = int(option['value'])
    
    return options


def get_options(term='', dept='', course=''):
    url = 'http://lsu.bncollege.com/webapp/wcs/stores/servlet/TextBookProcessDropdownsCmd?campusId=17548053&termId=%s&deptId=%s&courseId=%s&sectionId=&storeId=19057&catalogId=10001&langId=-1&dojo.transport=xmlhttp&dojo.preventCache=1301120964177'
    url = url % (term, dept, course)
    soup = BeautifulSoup.BeautifulSoup(urllib2.urlopen(url).read())
    
    options = {}
    for option in soup.find('select').findAll('option'):
        if option['value']:
            value = prepare_value(option['value'])
            options[option.string.lower()] = int(value)
    
    return options


def prepare_value(value):
    removechars = string.letters + string.punctuation
    removechars_table = dict((ord(char), None) for char in removechars)
    
    return value.translate(removechars_table)


def main():
    terms = get_terms()
    term = terms.values()[0]
    print terms
    
    depts = get_options(term=term) 
    dept = depts.values()[0]
    print depts
    
    courses = get_options(term=term, dept=dept) 
    course = courses.values()[0]
    print courses
    
    print term, dept, course
    print get_options(term=term, dept=dept, course=course)


if __name__ == '__main__':
    main()