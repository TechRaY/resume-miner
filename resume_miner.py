# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 20:34:46 2021

@author: tapan
"""

import sys
import nltk
import pandas as pd
from pdf_text_extractor import convert_pdf_to_text

class Parse():
    inputDF = pd.DataFrame()
    def __init__(self,verbose=False):
        print(" Starting Program ")
        self.inputDF = self.readResumeFiles()
        
    def readResumeFiles(self):
        try:
           convert_pdf_to_text() 
        except:
            return ''
            pass
     
    def preprocess(self,document):
        pass
    
    def tokenize(self,inputDF):
        pass
        

if __name__ == "__main__":
    verbose = False
    if "-v" in str(sys.argv):
        verbose = True
    p = Parse(verbose)