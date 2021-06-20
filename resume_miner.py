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

            extractedInfo['file'] = index # Todo - change this with file name

            #handle name extraction --
            name = self.extract_name(text)

            #handle email extraction--
            email = self.extract_email(text)

            #handle phone number extraction--
            phone = self.extract_phone(text)

            #handle experience extraction --
            experience = self.extract_experience(text)
            
            #handle skills extraction--
            skills = self.extract_skills(text)

            #handle qualification extraction--
            qualification = self.extract_qualification(text)

            extractedInfo = self.getInfo(name, email, phone, experience, skills, qualification) # TODO -> move this to util

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

    def extract_name(self, text):
        try:
           return ''
        except:
            return ''
            pass

    def extract_email(self, text):
        email = re.findall(r"([^@|\s]+@[^@]+\.[^@|\s]+)", text)
        if email:
            try:
                return email[0].split()[0].strip(';')
            except IndexError:
                return None
    
    def extract_phone(self, text):
        try:
           return ''
        except:
            return ''
            pass
        
    def extract_experience(self, text):
        try:
           return ''
        except:
            return ''
            pass

    def extract_skills(self, text):
        try:
            return ''
        except:
            return ''
            pass
        
    def extract_qualification(self, text):
        try:
           return ''
        except:
            return ''
            pass

    def getInfo(self, name, email, phone, experience, skills, qualification):
        return {
            "name": name,
            "email": email,
            "phone": phone,
            "experience": experience,
            "skills": skills,
            "qualification": qualification,
        }

if __name__ == "__main__":
    verbose = False
    if "-v" in str(sys.argv):
        verbose = True
    p = Parse(verbose)