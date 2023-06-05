# imports
from src.DST.dst import DST
from src.DP.dp import DP
from src.NLU.nlu import NLU

from sys import argv
import sys, getopt
import argparse

from pprint import pprint

def main(argv):
    debug_mode = False
    # parser = argparse.ArgumentParser()
    opts, args = getopt.getopt(argv, "", ["debug"])
    for opt, arg in opts:
        if "--debug" == opt: 
            debug_mode = True
    # parser.add_argument("--debug", help="Debug mode, show state of dialogue")

    # args = parser.parse_args()

    # initial modules
    dst = DST(recipe_path = "AMUseBotBackend/recipe/", dialog_path = "AMUseBotBackend/dialog/")
    dp = DP(dst=dst)
    nlu = NLU(intent_dict_path='AMUseBotBackend/utils/intent_dict.json', model_identifier_path='AMUseBotBackend/models/NLU/roberta-base-cookdial.txt')

    # main loop
    while True:
        intent = None
        system_message = None

        dst.restart()

        system_message = dp.generate_response(intent)

        print(system_message)

        while True:
            
            user_message = input()
            if "restart" == user_message.lower():
                break
            
            intents =  nlu.predict(user_message)
            # print("intent ", intent)
            dst.update_dialog_history(
                                system_message=system_message, 
                                user_message=user_message, 
                                intents=intents,
                                )

            system_message = dp.generate_response(intents)
            print(system_message)

            if(debug_mode):
                printable_object = {"dialog_state" : dst.generate_state()}
                pprint(printable_object, width=200)

if __name__ == '__main__':
    main(sys.argv[1:])

    
