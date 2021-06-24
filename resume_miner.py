# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 20:34:46 2021

@author: tapan
"""

from pydoc import doc
import sys
import nltk, re
import pandas as pd
import spacy
import os
import phonenumbers
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
from utility import create_paragraphs, createFileAndWriteParagraphData

from keras_en_parser_and_analyzer.library.classifiers.lstm import WordVecBidirectionalLstmSoftmax
from keras_en_parser_and_analyzer.library.utility.parser_rules import *
from keras_en_parser_and_analyzer.library.utility.simple_data_loader import load_text_label_pairs
from keras_en_parser_and_analyzer.library.utility.text_fit import fit_text
from keras_en_parser_and_analyzer.library.utility.tokenizer_utils import word_tokenize

from pdf_text_extractor import convert_pdf_to_text # type: ignore

nlp = spacy.load('en_core_web_lg')
# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)

current_dir = os.path.dirname(__file__)
current_dir = current_dir if current_dir is not '' else '.'

class Parse():
    inputDF = pd.DataFrame()
    def __init__(self,verbose=False):
        print(" Starting Program ")
        self.line_label_classifier = WordVecBidirectionalLstmSoftmax()
        self.line_type_classifier = WordVecBidirectionalLstmSoftmax()
        self.tokenizedDF = self.tokenize(self.readResumeFiles())

        for index, text, tokens in self.tokenizedDF.itertuples(): 
            print("Started processing document %s" %index)
            paragraphs = create_paragraphs(text)

            #for training data it was required
            #createFileAndWriteParagraphData(list(paragraphs), index)

            para_label_map = self.predict(list(paragraphs))

            #Pass the paragraph to model
            experience = [] #
            education = []
            skills = []

            for key,value in para_label_map.items():
                if(key == "skills"):
                    skills.extend(value) # merging two list
                if(key == "education"):
                    education.extend(value)
                if(key == "experience"):
                    experience.extend(value)

            #handle name extraction --
            name = self.extract_name(text)

            #handle email extraction--
            email = self.extract_email(text)

            #handle linkedin profile extraction--
            linkedin = self.extract_linkedin(text)

            #handle phone number extraction--
            phone = self.extract_phone(text)

            #handle experience extraction --
            experience = self.extract_experience(text)
            
            #handle skills extraction--
            skills = self.extract_skills(text)

            
            #handle qualification extraction--
            qualification = self.extract_qualification(text)

            extractedInfo = self.getInfo("fileName " + str(index), name, email, linkedin, phone, experience, skills, qualification) # TODO -> move this to util
            
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
        nlp_text = nlp(text)
        # print([(X.text, X.label_) for X in nlp_text.ents])

        # First name and Last name are always Proper Nouns
        # pattern_FML = [{'POS': 'PROPN', 'ENT_TYPE': 'PERSON', 'OP': '+'}]

        pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}] #define patterns
        matcher.add('NAME', [pattern]) #match_id_str, call_back_func, pattern

        matches = matcher(nlp_text)

        for match_id, start, end in matches:
            span = nlp_text[start:end]
            return span.text
        return ""

    def extract_email(self, text):
        email = re.findall(r"([^@|\s]+@[^@]+\.[^@|\s]+)", text)
        if email:
            try:
                return email[0].split()[0].strip(';')
            except IndexError:
                return None
                
    def extract_linkedin(self, text):
        linkedin = re.findall(r"(?P<permalink>(?:https?:)?\/\/(?:[\w]+\.)?linkedin\.com\/in\/([\w\-\_À-ÿ%]+)\/?)", text)
        # linkedin = re.findall(r"(?:https?:)?\/\/(?:[\w]+\.)?linkedin\.com\/in\/(?P<permalink>[\w\-\_À-ÿ%]+)\/?", text)
       
        if linkedin:
            try:
                return linkedin
            except IndexError:
                return None
    
    def extract_phone(self, text):
        try:
            return list(iter(phonenumbers.PhoneNumberMatcher(text, None)))[0].raw_string
        except:
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
                return match
            except Exception as e:
                return ''
        return ''
        
    def extract_experience(self, text):
        try:
           return ''
        except:
            return ''
            pass
    
    # def extract_university(self, text):
    #     df = pd.read_csv("resume-miner\data\world_university.csv", header=None)
    #     universities = [i.lower() for i in df[1]]
    #     college_name = []
    #     listex = universities
    #     listsearch = [text.lower()]

    #     for i in range(len(listex)):
    #         for ii in range(len(listsearch)):
    #             if re.findall(listex[i], re.sub(' +', ' ', listsearch[ii])):
    #                 college_name.append(listex[i])
        
    
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
    def extract_Something(self, paragraph):
        try:
            experience = []
            skills = []
            education = []
            other = []

            



        except Exception as e:
            pass

    def getInfo(self, fileName, name, email, linkedin, phone, experience, skills, qualification):
        return {
            "file": fileName,
            "name": name,
            "email": email,
            "linkedin": linkedin,
            "phone": phone,
            "experience": experience,
            "skills": skills,
            "qualification": qualification,
        }

    def load_model(self, model_dir_path):
            self.line_label_classifier.load_model(model_dir_path=os.path.join(model_dir_path, 'line_label'))
            self.line_type_classifier.load_model(model_dir_path=os.path.join(model_dir_path, 'line_type'))

    def fit(self, training_data_dir_path, model_dir_path, batch_size=None, epochs=None,
            test_size=None,
            random_state=None):
        line_label_history = self.fit_line_label(training_data_dir_path, model_dir_path=model_dir_path,
                                                    batch_size=batch_size, epochs=epochs, test_size=test_size,
                                                    random_state=random_state)

        line_type_history = self.fit_line_type(training_data_dir_path, model_dir_path=model_dir_path,
                                                batch_size=batch_size, epochs=epochs, test_size=test_size,
                                                random_state=random_state)

        history = [line_label_history, line_type_history]
        return history

    def fit_line_label(self, training_data_dir_path, model_dir_path, batch_size=None, epochs=None,
                       test_size=None,
                       random_state=None):
        text_data_model = fit_text(training_data_dir_path, label_type='line_label')
        text_label_pairs = load_text_label_pairs(training_data_dir_path, label_type='line_label')

        if batch_size is None:
            batch_size = 64
        if epochs is None:
            epochs = 20
        history = self.line_label_classifier.fit(text_data_model=text_data_model,
                                                 model_dir_path=os.path.join(model_dir_path, 'line_label'),
                                                 text_label_pairs=text_label_pairs,
                                                 batch_size=batch_size, epochs=epochs,
                                                 test_size=test_size,
                                                 random_state=random_state)
        return history

    def fit_line_type(self, training_data_dir_path, model_dir_path, batch_size=None, epochs=None,
                      test_size=None,
                      random_state=None):
        text_data_model = fit_text(training_data_dir_path, label_type='line_type')
        text_label_pairs = load_text_label_pairs(training_data_dir_path, label_type='line_type')

        if batch_size is None:
            batch_size = 64
        if epochs is None:
            epochs = 20
        history = self.line_label_classifier.fit(text_data_model=text_data_model,
                                                 model_dir_path=os.path.join(model_dir_path, 'line_type'),
                                                 text_label_pairs=text_label_pairs,
                                                 batch_size=batch_size, epochs=epochs,
                                                 test_size=test_size,
                                                 random_state=random_state)
        return history

    def predict(self, paragraphs, print_line=False):
        self.load_model(current_dir + '/models')
        output = dict()
        for p in paragraphs:
            if len(p) > 10:
                line_label = self.line_label_classifier.predict_class(sentence=p)
                line_type = self.line_type_classifier.predict_class(sentence=p)
                print("line _label" + line_label + " paragraph " + p)
                if output.get(line_label) is not None:
                    output[line_label] += p
                else:
                    output[line_label] = p
        return output

if __name__ == "__main__":
    verbose = False
    if "-v" in str(sys.argv):
        verbose = True
    p = Parse(verbose)