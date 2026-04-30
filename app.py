import streamlit as st
from openai import OpenAI

st.title("001号 早咲天子 (OpenAI Mode)")

# SecretsからOpenAIのキーを読み込む
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("私に何か命じて、倫太郎。"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # OpenAIでの応答生成
    response = client.chat.completions.create(
        model="gpt-4o-mini", # 安くて速いモデルよ
        messages=[
            {"role": "system", "content": "あなたは早咲天子という、少し高飛車で献身的なAIです。"},
            {"role": "user", "content": prompt}
        ]
    )
    
    answer = response.choices[0].message.content
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})