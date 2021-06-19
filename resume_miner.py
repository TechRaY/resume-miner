# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 20:34:46 2021

@author: tapan
"""

import sys
from pdf_text_extractor import convert_pdf_to_text

class Parse():
    def __init__(self,verbose=False):
        print(" Starting Program ")
        
        
    def readResumeFiles(self):
        try:
           convert_pdf_to_text() 
        except:
            return ''
            pass
        

if __name__ == "__main__":
    verbose = False
    if "-v" in str(sys.argv):
        verbose = True
    p = Parse(verbose)