import os
import re

ignoreWords = ["github", "gmail", "email", "page"]


#https://stackoverflow.com/questions/55499989/correctly-parse-pdf-paragraphs-with-python
#https://stackoverflow.com/questions/58606054/how-to-split-pdf-into-paragraphs-using-tika
def create_paragraphs(file_data_content):
    lines = file_data_content.splitlines(True)
    paragraph = []
    count = 0
    for line in lines:
        if line.isspace():
            if paragraph:
                count = count + 1
                if count > 1:
                    yield ''.join(paragraph)
                    #print([paragraph])
                    paragraph = []
                    count = 0
        else:
            if 'github' not in line:
                line = line.strip('\n')
                line = line.strip('\t')
                paragraph.append(line + " ")
    if paragraph:
        yield ''.join(paragraph)
    return paragraph

def createFileAndWriteParagraphData(paragraphs, fileName):
    output_file_path = "trainingData/" + str(fileName) + ".txt" #os.path.join("training_data/", str(fileName) + '.txt')
    # if os.path.exists(output_file_path):
    #     return
    try:
        with open(output_file_path, 'wt') as file:
            for paragraph in paragraphs:
                file.write(paragraph)
                file.write('\n')
    except Exception as e:
        print(e)
    finally:
        file.close();
