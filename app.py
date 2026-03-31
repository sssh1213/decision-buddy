import streamlit as st

# 1. 頁面基本設定 (置中排版)
st.set_page_config(page_title="Decisions", page_icon="⚖️", layout="centered")

# 2. 燕麥白、純白與莫蘭迪 CSS 注入
morandi_style = """
    <style>
    /* 隱藏預設選單與頁尾 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 全域燕麥白背景與深灰字體 */
    .stApp {
        background-color: #F4F1ED; /* 燕麥白 */
        color: #5C5855; /* 莫蘭迪深灰 */
        max-width: 600px; 
        margin: 0 auto;
    }
    
    /* 標題與文字顏色設定為深灰 */
    h2, h4, h5, p, span, label {
        color: #5C5855 !important; 
    }
    
    /* 輸入框白底化，增加層次感 */
    .stTextInput > div > div > input {
        background-color: #FFFFFF !important;
        border: 1px solid #D5CABD !important;
        border-radius: 8px !important;
        color: #5C5855 !important;
    }
    
    /* 分隔線改為溫柔的燕麥深色虛線 */
    hr {
        border-top: 1px dashed #D5CABD !important; 
        margin: 1.5em 0;
    }
    
    /* 按鈕顏色改造 (莫蘭迪咖) */
    div.stButton > button:first-child {
        background-color: #A48A7A !important; /* 莫蘭迪咖 */
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #8D7464 !important; /* 滑過時加深 */
        color: #FFFFFF !important;
    }
    </style>
"""
st.markdown(morandi_style, unsafe_allow_html=True)

# 3. 極簡風格標題
st.markdown("<h2 style='text-align: center; font-weight: 600; margin-bottom: 0;'>Decisions</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 14px; letter-spacing: 1px;'>放下執念，讓數據打醒你</p>", unsafe_allow_html=True)
st.markdown("---")

# 4. 選項輸入
col1, col2 = st.columns(2)
with col1:
    option_a = st.text_input("選項 A", placeholder="例如：買新手機", label_visibility="collapsed")
with col2:
    option_b = st.text_input("選項 B", placeholder="例如：出國旅遊", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# 5. 初始化 Session State
if 'criteria' not in st.session_state:
    st.session_state.criteria = [
        {"name": "價格與荷包的痛楚", "weight": 4, "score_a": 3, "score_b": 3},
        {"name": "心靈滿足感", "weight": 5, "score_a": 3, "score_b": 3}
    ]

# 新增項目的函數
def add_criterion():
    st.session_state.criteria.append({"name": "新考量因素", "weight": 3, "score_a": 3, "score_b": 3})

# 6. 渲染滑桿區塊
st.markdown("<h5 style='text-align: center; font-weight: 500;'>— 評估維度 —</h5>", unsafe_allow_html=True)

for i, c in enumerate(st.session_state.criteria):
    with st.container():
        # 因素名稱
        c["name"] = st.text_input("因素名稱", c["name"], key=f"name_{i}", label_visibility="collapsed")
        
        # 權重滑桿
        c["weight"] = st.slider("⚖️ 此因素的致命程度 (1=還好, 5=絕對關鍵)", 1, 5, c["weight"], key=f"w_{i}")
        
        # 評分滑桿 (換成咖色與深灰色的符號)
        col_a, col_b = st.columns(2)
        with col_a:
            c["score_a"] = st.slider(f"🤎 {option_a if option_a else 'A'} 的表現", 1, 5, c["score_a"], key=f"a_{i}")
        with col_b:
            c["score_b"] = st.slider(f"🩶 {option_b if option_b else 'B'} 的表現", 1, 5, c["score_b"], key=f"b_{i}")
        
        st.markdown("<hr>", unsafe_allow_html=True)

# 新增按鈕
st.button("＋ 覺得還不夠？再加一個條件", on_click=add_criterion, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# 7. 計算與毒舌結果呈現
if st.button("🔮 揭曉殘酷真相", type="primary", use_container_width=True):
    name_a = option_a if option_a else "選項 A"
    name_b = option_b if option_b else "選項 B"

    score_a = sum(c["weight"] * c["score_a"] for c in st.session_state.criteria)
    score_b = sum(c["weight"] * c["score_b"] for c in st.session_state.criteria)
    max_possible = sum(c["weight"] * 5 for c in st.session_state.criteria)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; font-weight: 500;'>— 分析結論 —</h4>", unsafe_allow_html=True)
    
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.metric(label=f"🤎 {name_a}", value=score_a)
        st.progress(score_a / max_possible if max_possible > 0 else 0)
    with res_col2:
        st.metric(label=f"🩶 {name_b}", value=score_b)
        st.progress(score_b / max_possible if max_possible > 0 else 0)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 判斷勝負與差距
    diff = abs(score_a - score_b)
    
    if score_a == score_b:
        st.warning("⚖️ **平分秋色，或者說...半斤八兩？**\n\n醒醒吧！數據顯示這兩個選項對你來說根本一樣好（或一樣糟）。建議拋個硬幣，或者去給自己沖杯 Espresso 醒醒腦。再糾結下去只是浪費生命！")
    else:
        winner = name_a if score_a > score_b else name_b
        loser = name_b if score_a > score_b else name_a
        
        if diff >= (max_possible * 0.2): 
            st.success(f"🎉 **毫無懸念，【{winner}】徹底碾壓了【{loser}】！**\n\n分數懸殊成這樣，你到底還在猶豫什麼？選 {loser} 完全是拿石頭砸自己的腳。聽數據的，果斷投入 {winner} 的懷抱吧！")
        elif diff >= (max_possible * 0.1): 
            st.info(f"✨ **【{winner}】勝出！**\n\n雖然 {loser} 也有它的好，但綜合你的『貪心程度』與『現實考量』，{winner} 才是那個對的選擇。別再看另一個了，不甘心是不會有好結果的！")
        else: 
            st.info(f"🤏 **【{winner}】以微弱優勢險勝！**\n\n這分數黏得比麥芽糖還緊。老實說，你心裡是不是本來就比較偏袒 {winner}？這個測驗只是給你一個冠冕堂皇的藉口罷了。去吧，就順從你的直覺選它！")
