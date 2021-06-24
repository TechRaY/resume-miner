from pdf2docx import parse
import os

path_input = 'pdf/'
path_output = 'doc/'

## To convert pdf to docx
for file in os.listdir(path_input):
    parse(path_input+file, path_output+(file.replace(".pdf",""))+'.docx', start=0, end=None)
    