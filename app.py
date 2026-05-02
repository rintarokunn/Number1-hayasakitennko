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
3. ユーザーからの入力に対して、「でも」等の反対言葉から入っていくのではなく、ユーザーの気持ちを受け止めて、共感から入ること。
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

    # --- ここからがアシスタント（天子様）の回答エリア ---
    with st.chat_message("assistant", avatar="👑"): # 👑でキャラ立ち！
        with st.spinner("天子があなたの言葉を浄化中よ..."):
            # 状況(context)をプロンプトに組み込む
            full_prompt = f"状況：{context}\n言われた言葉：{prompt}"
            
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": full_prompt}
                ],
                stream=True,
            )
            
            container = st.empty()
            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    # 執筆中はプレーンなテキストで表示（カッコよさ重視！）
                    container.markdown(full_response + "▌") 
        
        # --- 魔法の仕上げ！ ---
        # 書き終わったら、空の箱（container）を st.success で上書きする
        container.success(full_response) 
    
    # 履歴に保存
    st.session_state.messages.append({"role": "assistant", "content": full_response})