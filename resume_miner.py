# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 20:34:46 2021

@author: tapan
"""

from pydoc import doc
import sys
import nltk, re
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from pdf_text_extractor import convert_pdf_to_text # type: ignore

class Parse():
    inputDF = pd.DataFrame()
    def __init__(self,verbose=False):
        print(" Starting Program ")
        self.tokenizedDF = self.tokenize(self.readResumeFiles())

        for index, text, tokens in self.tokenizedDF.itertuples(): 
            print("Started processing document %s" %index)

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

            extractedInfo = self.getInfo("fileName " + str(index), name, email, phone, experience, skills, qualification) # TODO -> move this to util
            
            print(extractedInfo) #TODO -> remove this  print
        
        #TODO -> Dump all jsonRespnses to csv or excel sheet
        
    def readResumeFiles(self):
        try:
           return convert_pdf_to_text()
        except:
            return ''
            pass
    def preprocess(self, document):
        df = pd.DataFrame()
        lemmatizer = WordNetLemmatizer()
        for indx, row in document.itertuples(name='Frame'): 
            sentences = nltk.tokenize.sent_tokenize(row) #split into sentences
            sentences = [nltk.tokenize.word_tokenize(sent) for sent in sentences] #split/tokenize sentences into words
            tokens = sentences
            finalTokenList = []
            for token in tokens:
                finalTokenList += token
            tokens = finalTokenList
            tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in set(stopwords.words('english'))]
            
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
        number = None
        try:
            pattern = re.compile(r'([+(]?\d+[)\-]?[ \t\r\f\v]*[(]?\d{2,}[()\-]?[ \t\r\f\v]*\d{2,}[()\-]?[ \t\r\f\v]*\d*[ \t\r\f\v]*\d*[ \t\r\f\v]*)')
                # Understanding the above regex
                # +91 or (91) -> [+(]? \d+ -?
                # Metacharacters have to be escaped with \ outside of character classes; inside only hyphen has to be escaped
                # hyphen has to be escaped inside the character class if you're not incidication a range
                # General number formats are 123 456 7890 or 12345 67890 or 1234567890 or 123-456-7890, hence 3 or more digits
                # Amendment to above - some also have (0000) 00 00 00 kind of format
                # \s* is any whitespace character - careful, use [ \t\r\f\v]* instead since newlines are trouble
            match = pattern.findall(text)
            # match = [re.sub(r'\s', '', el) for el in match]
                # Get rid of random whitespaces - helps with getting rid of 6 digits or fewer (e.g. pin codes) strings
            # substitute the characters we don't want just for the purpose of checking
            match = [re.sub(r'[,.]', '', el) for el in match if len(re.sub(r'[()\-.,\s+]', '', el))>6]
                # Taking care of years, eg. 2001-2004 etc.
            match = [re.sub(r'\D$', '', el).strip() for el in match]
                # $ matches end of string. This takes care of random trailing non-digit characters. \D is non-digit characters
            match = [el for el in match if len(re.sub(r'\D','',el)) <= 15]
                # Remove number strings that are greater than 15 digits
            try:
                for el in list(match):
                    # Create a copy of the list since you're iterating over it
                    if len(el.split('-')) > 3: continue # Year format YYYY-MM-DD
                    for x in el.split("-"):
                        try:
                            # Error catching is necessary because of possibility of stray non-number characters
                            # if int(re.sub(r'\D', '', x.strip())) in range(1900, 2100):
                            if x.strip()[-4:].isdigit():
                                if int(x.strip()[-4:]) in range(1900, 2100):
                                    # Don't combine the two if statements to avoid a type conversion error
                                    match.remove(el)
                        except:
                            pass
            except:
                pass
            number = match
        except Exception as e:
            print(e)

        return number
        
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

    def getInfo(self, fileName, name, email, phone, experience, skills, qualification):
        return {
            "file": fileName,
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