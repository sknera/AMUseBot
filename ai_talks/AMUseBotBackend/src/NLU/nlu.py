import json
from simpletransformers.classification import MultiLabelClassificationModel

class NLU:
  def __init__(self, intent_dict_path, model_identifier_path):
    with open(intent_dict_path, encoding='utf-8') as f:
        self.int2intent = json.load(f)
    with open(model_identifier_path, encoding='utf-8') as f:
        model_identifier = f.read().strip()

    print(f'Using model: {model_identifier}')

    self.model = MultiLabelClassificationModel('roberta', model_identifier, num_labels=len(self.int2intent), use_cuda=False, args={'silent': True})

  def predict(self, utterance):
    predictions_vector, raw_outputs = self.model.predict([utterance])
    predictions_vector = predictions_vector[0]
    predicted_intents = []
    for i in range(len(predictions_vector)):
      if predictions_vector[i] == 1:
        predicted_intents.append(self.int2intent[str(i)])
    return predicted_intents
