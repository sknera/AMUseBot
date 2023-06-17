
import re
import json
from os import walk
import spacy
from tqdm import tqdm
import csv

path_to_file_input = "./recipe"

recipe_files = []
for (dirpath, dirnames, filenames) in walk(path_to_file_input):
    recipe_files.extend(filenames)
    break

recipes_names=[]

recipes_ingredients=dict()
for recipe in recipe_files:
    with open(path_to_file_input+"/"+recipe) as f:
        data=json.load(f)
        recipe_ingredients=[]
        for row in data["content"]:
            if row['type']=='ingredient':
                recipe_ingredients.append(" ".join(re.findall("[a-zA-z]+",row['text'])))
            recipes_ingredients[int(recipe[:3])]=[re.sub('json|(I+)',' ', ' '.join(re.findall("[a-zA-Z]+",recipe)))]+recipe_ingredients
text_list = []

for k,v in recipes_ingredients.items():
    text_list.append(str(k)+' '+' '.join(v))
tok_text=[]

nlp=spacy.load("en_core_web_sm")
stopwords=['can','cans','inch','cup','cups','and','or','what','teaspoon','teaspoons','chopped','cut']
for doc in tqdm(nlp.pipe(text_list, disable=['tagger', 'parser', 'ner'])):
    tok=[t.text for t in doc if not t.text in stopwords]
    tok_text.append(tok)

print(tok_text)
with open('ingredients_recipes_merged.csv', 'w') as f:
    wr=csv.writer(f)
    wr.writerows(tok_text)




