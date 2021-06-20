# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 20:34:46 2021

@author: tapan
"""

from pydoc import doc
import sys
import nltk, re
import pandas as pd
from pdf_text_extractor import convert_pdf_to_text # type: ignore

class Parse():
    inputDF = pd.DataFrame()
    def __init__(self,verbose=False):
        print(" Starting Program ")
        self.inputDF = self.tokenize(self.readResumeFiles())

        for index, text, tokens in self.inputDF.itertuples(): 
            print("Started processing document %s" %index)

            extractedInfo = {}

            extractedInfo['file'] = index # change this with file name

            #handle name extraction --
            self.setName(text, extractedInfo)

            #handle email extraction--
            self.setEmail(text, extractedInfo)

            #handle phone number extraction--
            self.setPhone(text, extractedInfo)

            #handle experience extraction --
            self.setExperience(text, extractedInfo)
            
            #handle skills extraction--
            self.setSkills(text, extractedInfo)

            #handle qualification extraction--
            self.setQualification(text, extractedInfo)

            print(extractedInfo)
        
    def readResumeFiles(self):
        try:
           return convert_pdf_to_text()
        except:
            return ''
            pass
    def preprocess(self, document):
        df = pd.DataFrame()
        for indx, row in document.itertuples(name='Frame'): 
            sentences = nltk.tokenize.sent_tokenize(row) #split into sentences
            sentences = [nltk.tokenize.word_tokenize(sent) for sent in sentences] #split/tokenize sentences into words

            tokens = sentences
            finalTokenList = []
            for token in tokens:
                finalTokenList += token
            
            tokens = finalTokenList

            df = df.append(pd.DataFrame(
                    [[row, tokens]], 
                    columns = ['parsedText','tokens']),
                    ignore_index=True
                )

        return df

    def tokenize(self, inputDF):
        try:
            return self.preprocess(inputDF)
        except Exception as e:
            print(e)

    def setName(self, text, infoDict):
        try:
           return ''
        except:
            return ''
            pass

    def setEmail(self, text, infoDict):
        email = None
        try:
            pattern = re.compile(r'\S*@\S*')
            matches = pattern.findall(text) # Gets all email addresses as a list
            email = matches
        except Exception as e:
            print(e)

        infoDict['email'] = email
        return email
    
    def setPhone(self, text, infoDict):
        try:
           infoDict['Phone'] = 'TODO ---'
        except:
            return ''
            pass
        
    def setExperience(self, text, infoDict):
        try:
           infoDict['Experience'] = 'TODO ---'
        except:
            return ''
            pass

    def setSkills(self, text, infoDict):
        try:
           infoDict['Skills'] = 'TODO ---'
        except:
            return ''
            pass
        
    def setQualification(self, text, infoDict):
        try:
           infoDict['Qualification'] = 'TODO ---'
        except:
            return ''
            pass

if __name__ == "__main__":
    verbose = False
    if "-v" in str(sys.argv):
        verbose = True
    p = Parse(verbose)