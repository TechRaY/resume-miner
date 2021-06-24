from pdf2docx import parse
import os

path_input = 'Resumes/pdf/'
path_output = 'Resumes/doc/'

## To convert pdf to docx
def convertToDoc():
    for file in os.listdir(path_input):
        parse(path_input+file, path_output+(file.replace(".pdf",""))+'.docx', start=0, end=None)


if __name__ == "__main__":
    convertToDoc()