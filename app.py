import streamlit as st
from openai import OpenAI  # 1. クラスをインポート
import os

# ページの設定
st.set_page_config(
    page_title="AI冷蔵庫レシピ - 今日の献立",
    page_icon="🍳",
    layout="centered"
)

# スタイル（カード風デザイン）
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
    }
    .recipe-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🍳 AI冷蔵庫レシピ")
st.caption("冷蔵庫にあるもので、プロの料理家が「意外な一皿」を提案します。")

# --- 2. クライアントの初期化 ---
try:
    # Streamlit CloudのSecretsから取得
    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"],
        organization=st.secrets.get("org-7GrkeEBEcYJYYsBLsQuKi7aP") # 任意
    )
except Exception as e:
    st.error("🔑 APIキーが設定されていません。Streamlit CloudのSettings > Secretsを確認してください。")
    st.stop()

# --- 入力エリア ---
with st.container():
    st.subheader("🛒 冷蔵庫のなかみ")
    ingredients = st.text_input("使いたい食材を入力（例: 鶏肉, キャベツ, 納豆）", placeholder="カンマ区切りで入力してください")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        category = st.selectbox("料理のジャンル", ["指定なし（お任せ）", "和食", "洋食", "中華", "エスニック"])
    with col2:
        difficulty = st.selectbox("難易度", ["簡単（時短）", "ふつう", "本格的（じっくり）"])
    with col3:
        st.write("")
        generate_btn = st.button("提案してもらう！")

# --- ロジック実行 ---
if generate_btn:
    if not ingredients:
        st.warning("⚠️ 食材を何か入力してください。")
    else:
        with st.spinner('AIシェフが独創的なメニューを考案中...'):
            try:
                # プロンプトの構築
                prompt = f"""
                あなたはプロの料理研究家です。ユーザーの要望を汲み取りつつ、あえて予想外の組み合わせや、遊び心のあるメニューを1つ提案してください。
                
                【条件】
                - 使用食材: {ingredients}
                - カテゴリ: {category}
                - 難易度: {difficulty}
                - レシピは簡潔に。
                - 同じ食材でも毎回異なるメニューになるよう、独創的な視点で考えてください。

                【出力形式】
                以下の形式で出力してください（Markdown形式）:
                ### 料理名: [料理名]
                
                **材料**
                - [材料1]
                - [材料2]...
                
                **作り方**
                1. [手順1]
                2. [手順2]...
                
                ---
                **AIからの今日の一言**
                [ユーザーへの応援メッセージ]
                """

                # --- 3. 最新のAPI呼び出し形式 ---
                response = client.chat.completions.create(
                    model="gpt-4o", 
                    messages=[
                        {"role": "system", "content": "あなたは遊び心溢れるプロの料理研究家です。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.9,
                )

                recipe_content = response.choices[0].message.content

                # 結果表示
                st.balloons()
                st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
                st.markdown(recipe_content)
                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"通信エラーが発生しました: {e}")

st.divider()
st.caption("Produced by AI Recipe Assistant")