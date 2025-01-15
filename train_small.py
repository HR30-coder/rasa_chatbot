import spacy
import json
from spacy.tokens import DocBin

with open("annotations.json", "r") as file:
    data = json.load(file)

# Step 2: Convert JSON to spaCy training format
train_data = []
for item in data["annotations"]:
    if item:  # Check if the item is not null
        text = item[0].strip()
        entities = item[1]["entities"]
        formatted_entities = [(start, end, label) for start, end, label in entities]
        train_data.append((text, {"entities": formatted_entities}))

# print(train_data)

# Load the small English model
nlp = spacy.load("en_core_web_sm")
db = DocBin()

for text, annotations in train_data:
    doc = nlp.make_doc(text)
    ents = []
    for start, end, label in annotations["entities"]:
        span = doc.char_span(start, end, label=label)
        if span:
            ents.append(span)
    doc.ents = ents  # Set the entities for the doc
    db.add(doc)

db.to_disk("train.spacy")