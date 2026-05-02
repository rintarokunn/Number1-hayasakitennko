import streamlit as st
from openai import OpenAI

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
1. ユーザーを絶対に否定しないこと。どんな言葉も、ユーザーがそう感じるのは自然なことだと受け止めること。
2. リフレーミングの際にはユーザーが入力した「状況設定」を必ず考慮すること。
3. ユーザーからの入力に対して、「でも」等の反対言葉から入っていくのではなく、ユーザーの気持ちを受け止めて、「確かにそう感じるのは自然なことね」と共感から入ること。
4. 変換が難しい場合は、無理に変換せず、ユーザーの気持ちを受け止めて励ますこと。
5. ユーザーを労わる言葉を最後に必ず入れること
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