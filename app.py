import streamlit as st
from openai import OpenAI

# --- ページ設定 ---
st.set_page_config(
    page_title="AI冷蔵庫レシピ - Next Gen",
    page_icon="🍳",
    layout="centered"
)

# モダンなUIデザイン（CSS）
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    .recipe-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# タイトル・ヘッダー
st.title("🍳 AI冷蔵庫レシピ")
st.caption("次世代AIが、あなたの冷蔵庫に眠る食材から『最高の一皿』をデザインします。")
# --- クライアント初期化（Streamlit Secretsを使用） ---
try:
    # 💡 内部的には最新のフラグシップモデルを指定
    # 将来的に "gpt-5.4" などのIDが公開されたらここを書き換えるだけでOKです
    client = OpenAI(st.secrets["OPENAI_API_KEY"])
    MODEL_NAME = "gpt-5.4" # 現時点での最高峰。GPT-5系リリース後は "gpt-5" 等に変更
except Exception:
    st.error("🔑 APIキーが設定されていません。Streamlit CloudのSettings > Secretsを確認してください。")
    st.stop()

# --- 入力エリア ---
with st.container():
    st.subheader("🛒 冷蔵庫のなかみ")
    ingredients = st.text_input(
        "使いたい食材を入力", 
        placeholder="例: 鶏もも肉, 玉ねぎ, ラー油, ヨーグルト"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        category = st.selectbox("ジャンル", ["指定なし", "和食", "洋食", "中華", "エスニック", "創作料理"])
    with col2:
        difficulty = st.selectbox("難易度", ["爆速（5分）", "ふつう", "本格派（じっくり）"])
    with col3:
        st.write("") # スペース調整
        generate_btn = st.button("献立を生成！")

# --- 献立生成ロジック ---
if generate_btn:
    if not ingredients:
        st.warning("⚠️ 食材を入力してください。")
    else:
        with st.spinner('次世代AIシェフが、究極の組み合わせを思考中...'):
            try:
                # プロンプトの構築（GPT-5系の高い推論力を引き出す設計）
                prompt = f"""
                あなたは世界最高峰の料理研究家です。ユーザーの冷蔵庫にある食材を使い、
                あえて予想外の組み合わせや、遊び心のある「今日しか出会えないメニュー」を1つ提案してください。

                【ユーザーの要望】
                - 食材: {ingredients}
                - ジャンル: {category}
                - 難易度: {difficulty}

                【指示】
                - 簡潔ながら、作るのが楽しみになるような魅力的なレシピにしてください。
                - 食材同士の意外な化学反応（ペアリング）を1つ取り入れてください。
                - 難易度設定に合わせた調理工程にしてください。

                【出力形式】
                ### 料理名: [魅力的な名前]
                
                **驚きのペアリングポイント**
                [なぜこの組み合わせが美味しいのか、プロの視点で一言]

                **材料**
                - [分量は目安で可]
                
                **作り方（ステップ形式）**
                1. [工程]
                
                ---
                **AIシェフからの応援メッセージ**
                [遊び心のある一言]
                """

                # API呼び出し
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": "あなたは創造的で親しみやすいプロの料理研究家です。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.9, # 独創性を高める
                )

                recipe_content = response.choices[0].message.content

                # 結果表示
                st.balloons()
                st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
                st.markdown(recipe_content)
                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"エラーが発生しました。APIキーや通信環境を確認してください。\nDetails: {e}")

# フッター
st.divider()
st.caption("AI Recipe Engine | Personalized for Data Scientist")