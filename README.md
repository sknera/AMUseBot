# Cooking taskbot project

## Run system

#### With Conda
    
    conda create -n "my_env" python=3.9.12 ipython
    conda activate my_env
    pip install -r requirements.txt
    python main.py

After running system, model saves in dir:

Linux

    ~/.cache/huggingface/transformers

Windows

    C:\Users\username\.cache\huggingface\transformers.


## Requirements

    Python 3.9.12

## Dataset

[YiweiJiang2015/CookDial](https://github.com/YiweiJiang2015/CookDial)

## NLU model HF repo

[kedudzic/roberta-base-cookdial](https://huggingface.co/AMUseBot/roberta-base-cookdial-v1_1)
