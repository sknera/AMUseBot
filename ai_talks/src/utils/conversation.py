import string
from random import randrange, choices

import streamlit as st
from openai.error import InvalidRequestError, OpenAIError
from streamlit_chat import message

from AMUseBot.src.DP.dp import DP
from AMUseBot.src.DST.dst import DST
from AMUseBot.src.NLU.nlu import NLU
from .agi.chat_gpt import create_gpt_completion
from .stt import show_voice_input
from .tts import show_audio_player

import os

absolute_path = os.path.dirname(__file__)


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


def show_chat_buttons() -> None:
    b0, b1, b2 = st.columns(3)
    with b0, b1, b2:
        b0.button(label=st.session_state.locale.chat_run_btn)
        b1.button(label=st.session_state.locale.chat_clear_btn, on_click=clear_chat)
        b2.download_button(
            label=st.session_state.locale.chat_save_btn,
            data="\n".join([str(d) for d in st.session_state.messages[1:]]),
            file_name="ai-talks-chat.json",
            mime="application/json",
        )


def show_chat(ai_content: str, user_text: str) -> None:
    if user_text not in st.session_state.past:
        #     # store the ai content
        st.session_state.past.append(user_text)
        st.session_state.generated.append(ai_content)

    if st.session_state.generated:
        for i in range(len(st.session_state.generated)):
            message(st.session_state.past[i], is_user=True, key=str(i) + "_user", seed=st.session_state.seed)
            message(st.session_state.generated[i], key=str(i), seed=st.session_state.seed)


def amuseAPI():
    recipe_path = os.path.join(absolute_path, "recipe")
    dialog_path = os.path.join(absolute_path, "dialog")
    # initial modules
    dst = DST(recipe_path=recipe_path, dialog_path=dialog_path)
    dp = DP(dst=dst)
    nlu = NLU(intent_dict_path=os.path.join(absolute_path, 'utils/intent_dict.json'),
              model_identifier_path=os.path.join(absolute_path, 'models/NLU/roberta-base-cookdial.txt'))


    intent = None
    system_message = None

    dst.restart()

    system_message = dp.generate_response(intent)


    user_message = input()
    if "restart" == user_message.lower():
        break

    intents = nlu.predict(user_message)
    # print("intent ", intent)
    dst.update_dialog_history(
        system_message=system_message,
        user_message=user_message,
        intents=intents,
    )

    system_message = dp.generate_response(intents)



def show_conversation() -> None:
    if st.session_state.messages:
        st.session_state.messages.append({"role": "user", "content": st.session_state.user_text})
    else:
        ai_role = f"{st.session_state.locale.ai_role_prefix} {st.session_state.role}. {st.session_state.locale.ai_role_postfix}"  # NOQA: E501
        st.session_state.messages = [
            {"role": "system", "content": ai_role},
            {"role": "user", "content": st.session_state.user_text},
        ]

    ai_content = "Dummy respone from AI"
    # delete random before deploying with our model
    random_str = ''.join(choices(string.ascii_uppercase + string.digits, k=5))
    ai_content += random_str
    st.session_state.messages.append({"role": "assistant", "content": ai_content})
    if ai_content:
        show_chat(ai_content, st.session_state.user_text)
        st.divider()
        show_audio_player(ai_content)
