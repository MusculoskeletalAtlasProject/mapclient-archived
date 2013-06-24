'''
MAP Client, a program to generate detailed musculoskeletal models for OpenSim.
    Copyright (C) 2012  University of Auckland
    
This file is part of MAP Client. (http://launchpad.net/mapclient)

    MAP Client is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MAP Client is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MAP Client.  If not, see <http://www.gnu.org/licenses/>..
'''
from os.path import join, dirname
import re

SECTION_HEADER_RE = '\[(.*)\]'

class AnnotationTool(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._vocab = Vocabulary()
    
    def _readVocabulary(self):
        with open(join(dirname(__file__), 'annotation.voc')) as f:
            content = f.readlines()
    
        section_header_re = re.compile(SECTION_HEADER_RE)
        
        section = ''
        for line in content:
            hash_index = line.find('#')
            line = line[:hash_index]
            if line:
                section_header = section_header_re.match(line)
                if section_header:
                    section = section_header.group(1)
                else:
                    if section == 'terms':
                        self._vocab.addTerm(line.strip())
                    else:
                        split_line = line.split(': ')
                        if len(split_line) == 2:
                            tag, value = split_line[0], split_line[1]
                            if tag == 'namespace':
                                self._vocab.setNamespace(value.strip())
                            elif tag == 'version':
                                self._vocab.setVersion(value.strip())          
    
    def getTerms(self):
        return self._vocab._terms
    
    
class Vocabulary(object):
    
    
    def __init__(self):
        self._namespace = None
        self._version = None
        self._terms = []
            
    def setNamespace(self, namespace):
        self._namespace = namespace
        
    def setVersion(self, version):
        self._version = version
        
    def addTerms(self, terms):
        self._terms.extend(terms)
        
    def addTerm(self, term):
        self._terms.append(term)
        
        
            
            
            
        
        
        