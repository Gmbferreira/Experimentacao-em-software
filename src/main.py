import streamlit as st
from presentation.pages.lab01 import index as lab01
from presentation.pages.lab02 import index as lab02

# st.title("Medição e Experimentação em Software")

pages = [
    st.Page(lab01.render,title=lab01.metadata["title"],icon=lab01.metadata["icon"],url_path="lab01"),
    st.Page(lab02.render,title=lab02.metadata["title"],icon=lab02.metadata["icon"],url_path="lab02")
]

pg = st.navigation(pages)

pg.run()