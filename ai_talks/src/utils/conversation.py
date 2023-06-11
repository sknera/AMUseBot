import string
from random import randrange, choices

import streamlit as st
from openai.error import InvalidRequestError, OpenAIError
from streamlit_chat import message
from .stt import show_voice_input
from .tts import show_audio_player

from AMUseBotBackend.src.DP.dp import DP
from AMUseBotBackend.src.DST.dst import DST
from AMUseBotBackend.src.NLU.nlu import NLU

@st.cache_resource
def get_nlu_model(intent_dict_path = 'AMUseBotFront/ai_talks/AMUseBotBackend/utils/intent_dict.json', model_identifier_path = 'AMUseBotFront/ai_talks/AMUseBotBackend/models/NLU/roberta-base-cookdial.txt'):
    return NLU(intent_dict_path=intent_dict_path,
                            model_identifier_path=model_identifier_path)

def clear_chat() -> None:
    st.session_state.generated = []
    st.session_state.past = []
    st.session_state.messages = []
    st.session_state.user_text = ""
    st.session_state.seed = randrange(10 ** 8)  # noqa: S311
    st.session_state.costs = []
    st.session_state.total_tokens = []

def get_user_input():
    # match st.session_state.input_kind:
    #     case st.session_state.locale.input_kind_1:
    #         show_text_input()
    #     case st.session_state.locale.input_kind_2:
    #         show_voice_input()
    #     case _:
    #         show_text_input()
    st.session_state.user_text = st.text_input("You: ", "Hello, how are you?", key="primary")

def on_send():
    st.session_state.past.append(st.session_state.user_text)

def show_chat_buttons() -> None:
    b0, b1, b2 = st.columns(3)
    with b0, b1, b2:
        b0.button(label=st.session_state.locale.chat_run_btn, on_click=on_send)
        b1.button(label=st.session_state.locale.chat_clear_btn, on_click=clear_chat)
        b2.download_button(
            label=st.session_state.locale.chat_save_btn,
            data="\n".join([str(d) for d in st.session_state.messages[1:]]),
            file_name="ai-talks-chat.json",
            mime="application/json",
        )

# def show_chat(ai_content: str, user_text: str) -> None:
#     first_message = True
# 
#     if user_text not in st.session_state.past:
#         if len(st.session_state.past) == 0:
#             first_message = False
#             print('message 1')
#             message(st.session_state.generated[0], key=str(0), seed=st.session_state.seed)
#         else:
#             #     # store the ai content
#             st.session_state.past.append(user_text)
#             st.session_state.generated.append(ai_content)
# 
#     if st.session_state.generated:
#         for i in range(len(st.session_state.past)):
#             print('message 2')
#             message(st.session_state.generated[i], key=str(i), seed=st.session_state.seed)
#             message(st.session_state.past[i], is_user=True, key=str(i) + "_user", seed=st.session_state.seed)
#         if first_message:
#             print('message 3')
#             message(st.session_state.generated[-1], key=str(-1), seed=st.session_state.seed)
        
def show_chat() -> None:
    for i in range(len(st.session_state.past)):
        message(st.session_state.generated[i], key=str(i), seed=st.session_state.seed)
        message(st.session_state.past[i], is_user=True, key=str(i) + "_user", seed=st.session_state.seed)        
    message(st.session_state.generated[-1], key=str(-1), seed=st.session_state.seed)
    
def show_conversation() -> None:
    if st.session_state.messages:
        st.session_state.messages.append({"role": "user", "content": st.session_state.user_text})
    else:
        ai_role = f"{st.session_state.locale.ai_role_prefix} {st.session_state.role}. {st.session_state.locale.ai_role_postfix}"  # NOQA: E501
        st.session_state.messages = [
            {"role": "system", "content": ai_role},
            {"role": "user", "content": st.session_state.user_text},
        ]
    
    if len(st.session_state.past):
        user_message = st.session_state.past[-1]
        # ai_content = "Dummy respone from AI"
        intents = get_nlu_model().predict(user_message)
        st.session_state.dst.update_dialog_history(
                                    system_message='', 
                                    user_message=user_message, 
                                    intents=intents,
                                    )
        system_message = st.session_state.dp.generate_response(intents)
        st.session_state.generated.append(system_message)

    # delete random before deploying with our model
    #random_str = ''.join(choices(string.ascii_uppercase + string.digits, k=5))
    ai_content = st.session_state.generated[-1]
    st.session_state.messages.append({"role": "assistant", "content": ai_content})
    show_chat()
    st.divider()
    show_audio_player(ai_content)
