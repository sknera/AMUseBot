# Cooking taskbot project

## Run system

#### With Conda
    
    conda create -n "my_env" python=3.9.12 ipython
    conda activate my_env
    pip install -r requirements.txt
    streamlit run ai_talks\chat.py

After running system, model saves in dir:

Linux

    ~/.cache/huggingface/transformers

Windows

    C:\Users\username\.cache\huggingface\transformers

To use the purely experimental generative features, for now, an OpenAI API key is needed. Insert it into the following file:

    AMUseBot/.env_template
    
## Requirements

    Python 3.9.12

## Dataset

[YiweiJiang2015/CookDial](https://github.com/YiweiJiang2015/CookDial)

## NLU model HF repo

[kedudzic/roberta-base-cookdial](https://huggingface.co/AMUseBot/roberta-base-cookdial-v1_1)
