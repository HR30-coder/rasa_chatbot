import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_lg")

# print(nlp.pipe_names)

sentence1 = "hi"
sentence2 = "bye"

# Process the sentences with the NLP model

doc1 = nlp(sentence1)
doc2 = nlp(sentence2)

# Calculate similarity between the two sentences
similarity_score = doc1.similarity(doc2)

print(f"Similarity between the sentences: {similarity_score:.3f}")