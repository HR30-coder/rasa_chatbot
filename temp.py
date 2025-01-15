import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_sm")

# print(nlp.pipe_names)

text = "please mail me at hritikrao07@gmail.com , Barack Obama became president of USA in 2010"

doc = nlp(text)

for tok in doc.ents:
    print(tok.text)