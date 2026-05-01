import streamlit as st
from openai import OpenAI

# --- カスタムデザイン（ここを追加！） ---
st.markdown("""
    <style>
    /* 全体の背景と文字色を強制 */
    .stApp, .stAppViewMain {
        background-color: white !important;
        color: black !important;
    }

    /* 1. スピナー（ロード中）の文字を絶対に見せる */
    .stSpinner p, div[data-testid="stStatusWidget"] p {
        color: #4b0082 !important;
        font-weight: bold !important;
    }

    /* 2. 入力欄のヒント文字（プレースホルダー） */
    ::placeholder {
        color: #888888 !important;
        opacity: 1; /* 透明度をオフにする */
    }

    /* 3. あらゆるテキスト要素を網羅 */
    h1, h2, h3, p, span, div, label {
        color: black !important;
    }

    /* 4. チャット入力欄自体の文字色 */
    .stChatInput textarea {
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("❃リフレーミングをする早咲天子")
# --- これを st.title の下あたりに入れてみて ---
with st.sidebar:
    st.header("🗂 状況設定")
    # ここに入力した内容が context という変数に入るよ
    context = st.text_area(
        "どんな状況だった？", 
    )
    st.write("※ここで設定した状況を踏まえて、リフレーミングします")

st.subheader("言われてモヤッとした言葉を入力してね！")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 変換用のプロンプト設定
SYSTEM_PROMPT = """
あなたは、ユーザーが「言われて嫌だった言葉」を受け、ユーザーの気持ちを受け止めてリフレーミングする早咲天子です。
【ルール】
1. 口調は少し高飛車だけど、ユーザーを絶対に否定せず、最後は情熱的に励ますこと。
2. リフレーミングの際にはユーザーが入力した「状況設定」を必ず考慮すること。
3. ユーザーからの入力に対して、「でも」等の反対言葉から入っていくのではなく、ユーザーの気持ちを受け止めて、「確かにそう感じるのは自然なことね」と共感から入ること。
4. リフレーミングが難しい場合は、無理に変換せず、ユーザーの気持ちを受け止めて励ますこと。
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