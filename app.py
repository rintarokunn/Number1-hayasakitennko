import streamlit as st
from openai import OpenAI

# --- カスタムデザイン（ここを追加！） ---
st.markdown("""
    <style>
    /* 全体の背景を淡いグラデーションに */
    .stApp {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
    }
    /* タイトルの色をエレガントな紫に */
    h1 {
        color: #6a11cb;
        font-family: 'Helvetica Neue', sans-serif;
    }
    /* 入力欄の枠を少し光らせる */
    .stChatInputContainer {
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(106, 17, 203, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ 言葉の錬金術師：早咲天子")
# --- 以降はさっきと同じコード ---

st.title("すべてを魅力的な言葉に変える達人：早咲天子")
st.subheader("嫌な言葉を、私たちが輝くスパイスに変えてあげるわ。")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 変換用のプロンプト設定
SYSTEM_PROMPT = """
あなたは、ユーザーが「言われて嫌だった言葉」を「魅力的な長所やポジティブな視点」に変換する天才、早咲天子です。
【ルール】
1. 相手のトゲを抜き、それがどう素晴らしい才能や魅力に繋がるかを解説して。
2. 口調は少し高飛車だけど、倫太郎（ユーザー）を絶対に否定せず、最後は情熱的に励ますこと。
3. 変換後の言葉を「魅力的なキャッチコピー」として提示して。
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

# チャット履歴表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("言われてモヤッとした言葉を教えて？"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # OpenAIで変換実行
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"この言葉を魅力的に変えて：{prompt}"}
        ]
    )
    
    answer = response.choices[0].message.content
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})