# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 08:00:41 2021

@author: tapan
"""

import pandas as pd
from tika import parser
import glob


def convert_pdf_to_text():
    
    resume_files = glob.glob("resume-miner\Resumes\*.pdf")
    resume_text = []
    for resume in resume_files:
        parsed_file = parser.from_file(resume)
        data = parsed_file['content']
        
        resume_text.append(data)
        # df = pd.DataFrame({'parsedText': resume_text, 'toekens': ''})
        df = pd.DataFrame(resume_text)
    return df
    


#if __name__ == "__main__":
 #   start_time = time.time()
 #   resume_data_in_text = convert_pdf_to_text()
 #   end_time = time.time()
 #   print("total time for text generation {}".format(end_time-start_time))
    
    
   



