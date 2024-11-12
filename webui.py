import streamlit as st
from webui_pages.utils import *
from streamlit_option_menu import option_menu
from webui_pages.dialogue.dialogue import dialogue_page, chat_box
from webui_pages.knowledge_base.knowledge_base import knowledge_base_page
import os
import sys
from server.utils import api_address


api = ApiRequest(base_url=api_address())

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 默认用户
DEFAULT_USERNAME = "guanjia"
DEFAULT_PASSWORD = "guanjia"


# 登录页面
def login_page():
    with st.form("login_form"):
        st.title("登录")
        username = st.text_input("用户名", value="")
        password = st.text_input("密码", value="", type="password")
        submit = st.form_submit_button("登录")

        if submit:
            if username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD:
                st.success("登录成功！")
                # 更新会话状态为已登录
                st.session_state.logged_in = True
                st.experimental_rerun()  # 重新运行脚本以显示主页面
            else:
                st.error("用户名或密码错误，请重新输入。")


if __name__ == "__main__":
    print(st.session_state.logged_in)
    if not st.session_state.logged_in:
        login_page()
    else:
        is_lite = "lite" in sys.argv

        st.set_page_config(
            "知识库问答",
            os.path.join("img", "chatchat_icon_blue_square_v2.png"),
            initial_sidebar_state="expanded",
            # menu_items={
            #     'Get Help': 'https://github.com/chatchat-space/Langchain-Chatchat',
            #     'Report a bug': "https://github.com/chatchat-space/Langchain-Chatchat/issues",
            #     'About': f"""欢迎使用 Langchain-Chatchat WebUI {VERSION}！"""
            # }
        )

        pages = {
            "对话": {
                "icon": "chat",
                "func": dialogue_page,
            },
            "知识库管理": {
                "icon": "hdd-stack",
                "func": knowledge_base_page,
            },
        }

        with st.sidebar:
            # st.image(
            #     os.path.join(
            #         "img",
            #         "logo-long-chatchat-trans-v2.png"
            #     ),
            #     use_column_width=True
            # )
            # st.caption(
            #     f"""<p align="right">当前版本：{VERSION}</p>""",
            #     unsafe_allow_html=True,
            # )
            options = list(pages)
            icons = [x["icon"] for x in pages.values()]

            default_index = 0
            selected_page = option_menu(
                "",
                options=options,
                icons=icons,
                # menu_icon="chat-quote",
                default_index=default_index,
            )

        if selected_page in pages:
            pages[selected_page]["func"](api=api, is_lite=is_lite)
