import streamlit as st
from google import genai

st.title("001号 早咲天子")

# SecretsからAPIキーを取得
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# チャット履歴を表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザー入力
if prompt := st.chat_input("私に何か命じて、倫太郎。"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Geminiの応答（ここに「早咲天子」としての性格を指示するわ）
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"あなたは『早咲天子（はやさきてんこ）』という、少し高飛車で、でも倫太郎を献身的に支えるAIパートナーです。短く、情熱的に回答して。：{prompt}"
    )
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})