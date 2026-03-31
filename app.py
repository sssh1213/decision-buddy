import streamlit as st

# 1. 頁面基本設定 (置中排版、簡約圖示)
st.set_page_config(page_title="Decisions.", page_icon="⚪", layout="centered")

# 2. 注入 CSS 來隱藏預設的標頭、頁尾，並美化字體與留白
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {max-width: 600px; margin: 0 auto;} /* 限制最大寬度，讓手機與電腦看都簡約 */
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# 3. 簡約風格的標題
st.markdown("<h2 style='text-align: center; color: #2c3e50; font-weight: 600; margin-bottom: 0;'>Decisions.</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d; font-size: 14px;'>理性分析，優雅選擇</p>", unsafe_allow_html=True)
st.markdown("---")

# 4. 選項輸入 (並排顯示)
col1, col2 = st.columns(2)
with col1:
    option_a = st.text_input("選項 A", placeholder="例如：買筆電", label_visibility="collapsed")
with col2:
    option_b = st.text_input("選項 B", placeholder="例如：組裝桌機", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# 5. 初始化 Session State (用來記住有幾個評分項目)
if 'criteria' not in st.session_state:
    st.session_state.criteria = [
        {"name": "價格與預算", "weight": 4, "score_a": 3, "score_b": 3},
        {"name": "外觀與質感", "weight": 3, "score_a": 3, "score_b": 3}
    ]

# 新增項目的函數
def add_criterion():
    st.session_state.criteria.append({"name": "新考量因素", "weight": 3, "score_a": 3, "score_b": 3})

# 6. 渲染滑桿區塊 (直列排版，適合手機單手滑動)
st.markdown("<h5 style='color: #34495e;'>評估維度</h5>", unsafe_allow_html=True)

for i, c in enumerate(st.session_state.criteria):
    with st.container():
        # 因素名稱輸入框
        c["name"] = st.text_input("因素名稱", c["name"], key=f"name_{i}", label_visibility="collapsed")
        
        # 重要性滑桿
        c["weight"] = st.slider("⚖️ 此因素的重要性", 1, 5, c["weight"], key=f"w_{i}")
        
        # 兩個選項的表現滑桿 (左右並排)
        col_a, col_b = st.columns(2)
        with col_a:
            c["score_a"] = st.slider(f"🔵 {option_a if option_a else 'A'} 的表現", 1, 5, c["score_a"], key=f"a_{i}")
        with col_b:
            c["score_b"] = st.slider(f"🟢 {option_b if option_b else 'B'} 的表現", 1, 5, c["score_b"], key=f"b_{i}")
        
        st.markdown("<hr style='margin: 1.5em 0; border-top: 1px dashed #e0e0e0;'>", unsafe_allow_html=True)

# 新增按鈕
st.button("＋ 新增考量因素", on_click=add_criterion, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# 7. 計算與結果呈現
if st.button("生成分析結果", type="primary", use_container_width=True):
    # 計算加權總分
    score_a = sum(c["weight"] * c["score_a"] for c in st.session_state.criteria)
    score_b = sum(c["weight"] * c["score_b"] for c in st.session_state.criteria)
    
    # 計算滿分會是多少 (用於進度條呈現)
    max_possible = sum(c["weight"] * 5 for c in st.session_state.criteria)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #2c3e50;'>分析結論</h4>", unsafe_allow_html=True)
    
    # 顯示分數與進度條 (增加視覺設計感)
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.metric(label=f"🔵 {option_a if option_a else 'A'}", value=score_a)
        st.progress(score_a / max_possible if max_possible > 0 else 0)
    with res_col2:
        st.metric(label=f"🟢 {option_b if option_b else 'B'}", value=score_b)
        st.progress(score_b / max_possible if max_possible > 0 else 0)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 結論文字
    if score_a > score_b:
        st.success(f"✨ 數據顯示，**{option_a if option_a else '選項 A'}** 目前更符合你的綜合需求。")
    elif score_b > score_a:
        st.success(f"✨ 數據顯示，**{option_b if option_b else '選項 B'}** 目前更符合你的綜合需求。")
    else:
        st.info("⚖️ 兩者平分秋色！建議沉澱一下，或者再新增一個絕對關鍵的因素來打破僵局。")
