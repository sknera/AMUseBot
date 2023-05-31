from pathlib import Path
from random import randrange

from AMUseBotBackend.src.DP.dp import DP
from AMUseBotBackend.src.DST.dst import DST
from AMUseBotBackend.src.NLU.nlu import NLU

import graphviz
import streamlit as st
from PIL import Image
from src.utils.conversation import get_user_input, show_chat_buttons, show_conversation
from src.utils.lang import en


if __name__ == '__main__':

    # --- PATH SETTINGS ---
    current_dir: Path = Path(__file__).parent if "__file__" in locals() else Path.cwd()
    css_file: Path = current_dir / "src/styles/.css"
    assets_dir: Path = current_dir / "assets"
    icons_dir: Path = assets_dir / "icons"
    img_dir: Path = assets_dir / "img"
    tg_svg: Path = icons_dir / "tg.svg"
    favicon: Path = icons_dir / "favicons/0.png"
    # --- GENERAL SETTINGS ---
    LANG_PL: str = "Pl"
    AI_MODEL_OPTIONS: list[str] = [
        "gpt-3.5-turbo",
        "gpt-4",
        "gpt-4-32k",
    ]

    CONFIG = {"page_title": "AMUsebot", "page_icon": Image.open(favicon)}

    st.set_page_config(**CONFIG)

    # --- LOAD CSS ---
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Storing The Context
    if "locale" not in st.session_state:
        st.session_state.locale = en
    if "generated" not in st.session_state:
        st.session_state.generated = []
    if "past" not in st.session_state:
        st.session_state.past = []
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "user_text" not in st.session_state:
        st.session_state.user_text = ""
    if "input_kind" not in st.session_state:
        st.session_state.input_kind = st.session_state.locale.input_kind_1
    if "seed" not in st.session_state:
        st.session_state.seed = randrange(10 ** 3)  # noqa: S311
    if "costs" not in st.session_state:
        st.session_state.costs = []
    if "total_tokens" not in st.session_state:
        st.session_state.total_tokens = []
    if "dst" not in st.session_state:
        st.session_state.dst = DST(recipe_path="AMUseBotFront/ai_talks/AMUseBotBackend/recipe/", dialog_path="AMUseBotFront/ai_talks/AMUseBotBackend/dialog/")
    if "dp" not in st.session_state:
        st.session_state.dp = DP(dst=st.session_state.dst)
    if "nlu" not in st.session_state:
        st.session_state.nlu = NLU(intent_dict_path='AMUseBotFront/ai_talks/AMUseBotBackend/utils/intent_dict.json',
                                model_identifier_path='AMUseBotFront/ai_talks/AMUseBotBackend/models/NLU/roberta-base-cookdial.txt')

def show_graph():
    # Create a graphlib graph object
    if st.session_state.generated:
        user, chatbot = [], []
        graph = graphviz.Digraph()
        for i in range(len(st.session_state.generated)):
            user.append(st.session_state.past[i])
            chatbot.append(st.session_state.generated[i])
        for x in range(len(user)):
            graph.edge(st.session_state.past[x], st.session_state.generated[x])
            try:
                graph.edge(st.session_state.generated[x], st.session_state.past[x+1])
            except:
                pass
            st.graphviz_chart(graph)


def main() -> None:
    c1, c2 = st.columns(2)
    with c1, c2:
        st.session_state.input_kind = c2.radio(
            label=st.session_state.locale.input_kind,
            options=(st.session_state.locale.input_kind_1, st.session_state.locale.input_kind_2),
            horizontal=True,
        )
        role_kind = c1.radio(
            label=st.session_state.locale.radio_placeholder,
            options=(st.session_state.locale.radio_text1, st.session_state.locale.radio_text2),
            horizontal=True,
        )
        if role_kind == st.session_state.locale.radio_text1:
            c2.selectbox(label=st.session_state.locale.select_placeholder2, key="role",
                             options=st.session_state.locale.ai_role_options)
        elif role_kind == st.session_state.locale.radio_text2: 
            c2.text_input(label=st.session_state.locale.select_placeholder3, key="role")
        
    if st.session_state.user_text:
        show_graph()
        show_conversation()

    get_user_input()
    show_chat_buttons()


if __name__ == "__main__":
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.locale.title}</h1>", unsafe_allow_html=True)
    main()
