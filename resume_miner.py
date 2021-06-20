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

        for indx, row in self.inputDF.itertuples(name='Frame'): 
            print("Started processing document %s" %indx)

            extractedInfo = {}

            extractedInfo['file'] = indx # change this with file name

            #handle name extraction --
            self.setName(row, extractedInfo)

            #handle email extraction--
            self.setEmail(row, extractedInfo)

            #handle phone number extraction--
            self.setPhone(row, extractedInfo)

            #handle experience extraction --
            self.setExperience(row, extractedInfo)
            
            #handle skills extraction--
            self.setSkills(row, extractedInfo)

            #handle qualification extraction--
            self.setQualification(row, extractedInfo)

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

    def tokenize(row, inputDF):
        try:
            self.tokens = self.preprocess(inputDF)
            return self.tokens
        except Exception as e:
            print(e)

    def setName(row, document):
        try:
           return ''
        except:
            return ''
            pass

    def setEmail(row, infoDict):
        email = None
        try:
            pattern = re.compile(r'\S*@\S*')
            matches = pattern.findall(row) # Gets all email addresses as a list
            email = matches
        except Exception as e:
            print(e)

        infoDict['email'] = email
        print("\n" + infoDict)
        return email
    
    def setPhone(row, document):
        try:
           return ''
        except:
            return ''
            pass
        
    def setExperience(row, document):
        try:
           return ''
        except:
            return ''
            pass

    def setSkills(row, document):
        try:
           return ''
        except:
            return ''
            pass
        
    def setQualification(row, document):
        try:
           return ''
        except:
            return ''
            pass

if __name__ == "__main__":
    verbose = False
    if "-v" in str(sys.argv):
        verbose = True
    p = Parse(verbose)