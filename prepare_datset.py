from numpy.core.numeric import NaN
from numpy.lib.shape_base import split
import pandas as pd
import sklearn_crfsuite


df = pd.read_csv("data\world-universities.csv")
# print(df.head())

# data = {'Sentence #': ['Sentence 1', NaN, NaN], 'Word': ['University', 'of', 'California'], 'Tag': ['UNI', 'UNI', 'UNI']}
# ner_df = pd.DataFrame(data)
# print(ner_df.head())

# ner_df = df['University'].apply(lambda x: pd.Series(x.split(' '))).stack()
ner_df = df['University'].str.split(' ').apply(pd.Series, 1).stack().add_prefix('Sentence: ').to_frame()
ner_df['Tag']='UNI'
# ner_df.drop(ner_df.columns[1], axis=1)
print(ner_df.head())
ner_df.to_csv('data\\ner_out.csv')