import re
import time

from pycorenlp.corenlp import StanfordCoreNLP

"""
Extra Steps:
Install python package:
   pip install pycorenlp
Downlaod CoreNLP:
   wget https://nlp.stanford.edu/software/stanford-corenlp-4.0.0.zip https://nlp.stanford.edu/software/stanford-corenlp-4.0.0-models-english.jar
   unzip stanford-corenlp-4.0.0.zip
   mv stanford-corenlp-4.0.0-models-english.jar stanford-corenlp-4.0.0
   cd stanford-corenlp-4.0.0
Run the server using all jars in the current directory (e.g., the CoreNLP home directory):
   java -mx1g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
"""



#host = "http://d58a66e1e16d.ngrok.io"
#port = "80"
host = "http://localhost"
port = "9000"
nlp = StanfordCoreNLP(host + ":" + port)


def generate_ngrams(s, n):
    # Replace all none alphanumeric characters with spaces
    s = s.replace('\n','*')
    s = re.sub('[^0-9a-zA-Z\s]+', '*', s)
    # s = re.sub(r'[^a-zA-Z0-9\s]', '*', s)
    independent_strings= s.split('*')
    # Break sentence in the token, remove empty tokens
    ngrams_list=[]
    for string in independent_strings:
        tokens = [token for token in string.replace('*','').split(" ") if token != ""]
        # Use the zip function to help us generate n-grams
        # Concatentate the tokens into ngrams and return
        ngrams = zip(*[tokens[i:] for i in range(n)])
        temp =[" ".join(ngram) for ngram in ngrams]
        ngrams_list.extend(temp)
    return ngrams_list

def find_name(s):
    # s = " Operational Analyst (SQL DBA) Engineer Alok Khandai - UNISYS Bengaluru, Karnataka - Email me on Indeed"
    bigrams = generate_ngrams(s, n=2)
    name = "NOT_FOUND"
    for bigram in bigrams:
        bigram=bigram.replace("\n", " ")
        output = nlp.annotate(
            bigram,
            properties={
                "outputFormat": "json",
                "timeout":"50000",
                "annotators": "ner,entitymentions"
            }
        )
        tokens =output.get('sentences')[0].get('tokens')
        # print(tokens)
        if len(tokens)==2:
            isPerson = True
            person=""
            for token in tokens:
                isPerson = isPerson and  (token.get('ner')=='PERSON')
                person= person+" "+token.get('originalText')
            if isPerson:
                name=person.strip()
                break
def find_org(s,n):
    ngrams = generate_ngrams(s, n)
    orgs=[]
    for ngram in ngrams:
        output = nlp.annotate(
            ngram,
            properties={
                "outputFormat": "json",
                "annotators": "ner,entitymentions"
            }
        )
        tokens =output.get('sentences')[0].get('tokens')
        # print(tokens)
        if len(tokens)==n:
            isOrg = True
            org=""
            for token in tokens:
                isOrg = isOrg and  (token.get('ner')=='ORGANIZATION' or (token.get('ner')=='PERSON') or (token.get('pos')=='NNP' and token.get('ner')=='O'))
                if isOrg:
                    org= org+" "+token.get('originalText')
            if isOrg:
                org=org.strip()
                orgs.append(org)

    return orgs

#call this to get list of org in sentence with max_length
def get_orgs_list(s, max_length=5):
    orgs = []
    for i in range(max_length,0, -1):
        i_list = find_org(s,i)
        print(i_list)
        to_remove = []
        # Removing substrings
        for i_item in i_list:
            if any(i_item.strip() in org for org in orgs):
                to_remove.append(i_item)
        for item in to_remove:
            i_list.remove(item)

        orgs.extend(i_list)
    return orgs
text = "JP Morgan Chase"
print(get_orgs_list(text))
