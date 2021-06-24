# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 08:00:41 2021

@author: tapan
"""

import pandas as pd
from tika import parser
import glob
<<<<<<< HEAD
from utility import create_paragraphs
from utility import createFileAndWriteParagraphData

def convert_pdf_to_text():
    
    resume_files = glob.glob("resume-miner\Resumes\AbhinayResumeFullStack.pdf")
=======
from utility import create_paragraphs, createFileAndWriteParagraphData

def convert_pdf_to_text():
    resume_files = glob.glob("Resumes\pdf\*.pdf")
>>>>>>> 51ded598124c48a4430172631c603c1b98154227
    resume_text = []
    for resume in resume_files:
        parsed_file = parser.from_file(resume)
        data = parsed_file['content']
<<<<<<< HEAD
        print("****************")
        abc = create_paragraphs(data)
        createFileAndWriteParagraphData(list(abc), "AbhinayResumeFullStack")
        print(list(abc))
        print("****************")
=======
        paragraphs = create_paragraphs(data)
        #print(list(abc))
        createFileAndWriteParagraphData(list(paragraphs), parsed_file['metadata']['resourceName'])
>>>>>>> 51ded598124c48a4430172631c603c1b98154227
        resume_text.append(data)
        df = pd.DataFrame(resume_text)
    return df
    


#if __name__ == "__main__":
 #   start_time = time.time()
 #   resume_data_in_text = convert_pdf_to_text()
 #   end_time = time.time()
 #   print("total time for text generation {}".format(end_time-start_time))
    
    
   



