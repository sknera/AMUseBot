import glob
import sys
import json
import pandas as pd

dataset_path = sys.argv[1] # Path to CookDial's dialog subdirectory

# 1st pass - create intent->integer and integer->intent dicts, save the second one for NLU use
all_intents = set()

for file in list(glob.glob(f'{dataset_path}/*.json')):
  with open(file, encoding='utf-8') as dial_file:
    dial_data = json.load(dial_file)
    for message in dial_data['messages']:
      if message['bot'] == False:
        intents = json.loads(message['annotations'])['intent']
        for intent in [intent.strip() for intent in intents.split(';')]:
          if intent != '':
            all_intents.add(intent)

all_intents.add('choose_recipe') # Add special intent for recipe title recognition

intent2int = dict(zip(sorted(list(all_intents)), range(len(all_intents))))
int2intent = {v: k for k, v in intent2int.items()}
with open('intent_dict.json', 'w', encoding='utf-8') as f:
    json.dump(int2intent, f)


# 2nd pass - preprocess dialogue data for training
preprocessed_data = []

for file in list(glob.glob(f'{dataset_path}/*.json')):
  with open(file, encoding='utf-8') as dial_file:
    dial_data = json.load(dial_file)
    for message in dial_data['messages']:
      if message['bot'] == False:
        annotations = json.loads(message['annotations'])
        intents = [intent.strip() for intent in annotations['intent'].split(';')]
        intents.remove('')
        intents_multi_hot = [0] * len(all_intents)
        for intent in intents:
          intents_multi_hot[intent2int[intent]] = 1
        preprocessed_data.append([message['utterance'], intents_multi_hot])

preprocessed_data_df = pd.DataFrame(preprocessed_data)
preprocessed_data_df.to_csv('preprocessed_data.csv', header = ['utterance', 'intents'], index=False, sep=';')
