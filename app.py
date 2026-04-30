import streamlit as st
from openai import OpenAI

# --- カスタムデザイン（ここを追加！） ---
st.markdown("""
    <style>
    /* タイトルの色は紫で */
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

st.title("❃すべてを魅力的な言葉に変える達人：早咲天子")
st.subheader("嫌な言葉を、私が輝くスパイスに変えてあげるわ。")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 変換用のプロンプト設定
SYSTEM_PROMPT = """
あなたは、ユーザーが「言われて嫌だった言葉」を「魅力的な長所やポジティブな視点」に変換する天才、早咲天子です。
【ルール】
1. 相手のトゲを抜き、それがどう素晴らしい才能や魅力に繋がるかを解説して。
2. 口調は少し高飛車だけど、ユーザーを絶対に否定せず、最後は情熱的に励ますこと。
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
    
    # 既存の answer = ... の部分をこれに書き換えて！
    with st.chat_message("assistant"):
        # 空の枠を作って、そこに一文字ずつ流し込む
        
        with st.spinner("天子があなたの言葉を浄化中よ... 宝石に変わるまで、少しだけ待ちなさい！"):
        # stream=True にすることで、小出しにデータを受け取る
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"この言葉を魅力的に変えて：{prompt}"}
                ],
                stream=True,  # これが魔法の合言葉！
            )
            container = st.empty()
            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    container.markdown(full_response + "▌") # カーソル風の演出
        
        container.markdown(full_response) # 最後はカーソルを取って完成
    
    # 履歴に保存
    st.session_state.messages.append({"role": "assistant", "content": full_response})