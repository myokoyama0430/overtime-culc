import streamlit as st
import pandas as pd

st.set_page_config(page_title="残業時間集計", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #f5f9fc;
    }
    .main .block-container {
        padding: 1rem 2rem;
        max-width: 1000px;
    }
    header[data-testid="stHeader"] {
        background-color: #ffffff;
        border-bottom: 1px solid #e8eef3;
    }
    .header-container {
        background-color: #ffffff;
        padding: 1rem 2rem;
        border-bottom: 1px solid #e8eef3;
        margin: -1rem -2rem 2rem -2rem;
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }
    .header-icon {
        background: linear-gradient(135deg, #3b9ddd 0%, #2ecc71 100%);
        width: 36px;
        height: 36px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 18px;
    }
    .header-title {
        color: #2c3e50;
        font-size: 1.2rem;
        font-weight: 600;
        margin: 0;
    }
    .hero-section {
        text-align: center;
        padding: 3rem 1rem;
    }
    .hero-title {
        font-size: 2.2rem;
        color: #2c3e50;
        font-weight: 700;
        margin-bottom: 0.8rem;
    }
    .hero-title span {
        color: #3b9ddd;
    }
    .hero-subtitle {
        color: #7f8c8d;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 2rem;
    }
    .upload-box {
        background: #ffffff;
        border: 2px dashed #d0e3f0;
        border-radius: 16px;
        padding: 2.5rem;
        text-align: center;
        max-width: 500px;
        margin: 0 auto 2rem auto;
    }
    .upload-icon {
        width: 60px;
        height: 60px;
        background-color: #e8f4fc;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem auto;
        color: #3b9ddd;
        font-size: 24px;
    }
    .upload-text {
        color: #2c3e50;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    .upload-subtext {
        color: #95a5a6;
        font-size: 0.85rem;
    }
    .result-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding: 0 0.5rem;
    }
    .result-title {
        color: #2c3e50;
        font-size: 1.1rem;
        font-weight: 600;
    }
    .result-count {
        color: #7f8c8d;
        font-size: 0.9rem;
    }
    .data-table {
        background: #ffffff;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .stDataFrame {
        border: none !important;
    }
    .stDataFrame > div {
        border-radius: 12px;
        overflow: hidden;
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e8eef3;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdown"] h2 {
        color: #2c3e50;
        font-size: 1rem;
        font-weight: 600;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #e8eef3;
    }
    [data-testid="stMetric"] {
        background-color: #f8fbfd;
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid #e8eef3;
    }
    [data-testid="stMetric"] label {
        color: #7f8c8d;
        font-size: 0.85rem;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #2c3e50;
        font-size: 1.5rem;
        font-weight: 600;
    }
    .stCheckbox label {
        color: #2c3e50;
    }
    .stFileUploader > div > div {
        background-color: transparent !important;
    }
    .stFileUploader label {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-container">
    <div class="header-icon">📊</div>
    <p class="header-title">残業時間集計</p>
</div>
""", unsafe_allow_html=True)

def decimal_to_hours_minutes(decimal_hours):
    """10進法の時間を時間:分形式に変換"""
    if pd.isna(decimal_hours):
        return "0:00"
    hours = int(decimal_hours)
    minutes = int(round((decimal_hours - hours) * 60))
    return f"{hours}:{minutes:02d}"

uploaded_file = st.file_uploader("CSVファイル", type=['csv'], label_visibility="collapsed")

if uploaded_file is None:
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">残業時間を<span>自動集計</span></h1>
        <p class="hero-subtitle">
            CSVファイルをアップロードするだけで、スタッフごとの残業時間を自動集計。<br>
            45時間以上の残業者を一目で確認できます。
        </p>
        <div class="upload-box">
            <div class="upload-icon">↑</div>
            <p class="upload-text">CSVファイルをアップロード</p>
            <p class="upload-subtext">ドラッグ＆ドロップ、またはクリックして選択</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    try:
        try:
            df = pd.read_csv(uploaded_file, encoding="cp932")
        except:
            uploaded_file.seek(0)
            try:
                df = pd.read_csv(uploaded_file, encoding="shift_jis")
            except:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding="utf-8")
        
        df.columns = df.columns.str.strip()
        
        staff_col = None
        name_col = None
        overtime_col = None
        late_overtime_col = None
        
        for col in df.columns:
            if "ｽﾀｯﾌ番号" in col or "スタッフ番号" in col:
                staff_col = col
            if "氏名" in col and "漢字" in col:
                name_col = col
            if "支払残業時間" in col:
                overtime_col = col
            if "支払深残時間" in col:
                late_overtime_col = col
        
        if all([staff_col, name_col, overtime_col, late_overtime_col]):
            grouped = df.groupby([staff_col, name_col]).agg({
                overtime_col: 'sum',
                late_overtime_col: 'sum'
            }).reset_index()
            
            grouped['合計残業時間（10進法）'] = grouped[overtime_col] + grouped[late_overtime_col]
            grouped['合計残業時間（時間:分）'] = grouped['合計残業時間（10進法）'].apply(decimal_to_hours_minutes)
            
            result = grouped[[staff_col, name_col, '合計残業時間（10進法）', '合計残業時間（時間:分）']].copy()
            result.columns = ['スタッフ番号', '氏名', '合計残業時間（10進法）', '合計残業時間（時間:分）']
            
            result = result.sort_values('スタッフ番号', ascending=True)
            
            st.sidebar.markdown("## フィルター")
            show_only_over_45 = st.sidebar.checkbox("45時間以上のみ表示", value=False)
            
            st.sidebar.markdown("---")
            st.sidebar.metric("総スタッフ数", f"{len(result)}名")
            st.sidebar.metric("45時間以上", f"{len(result[result['合計残業時間（10進法）'] >= 45])}名")
            
            if show_only_over_45:
                display_df = result[result['合計残業時間（10進法）'] >= 45].copy()
                count_text = f"{len(display_df)}名"
                title_text = "45時間以上の残業者"
            else:
                display_df = result.copy()
                over_45_count = len(result[result['合計残業時間（10進法）'] >= 45])
                count_text = f"{len(display_df)}名（45時間以上: {over_45_count}名）"
                title_text = "スタッフ残業時間一覧"
            
            st.markdown(f"""
            <div class="result-header">
                <span class="result-title">{title_text}</span>
                <span class="result-count">{count_text}</span>
            </div>
            """, unsafe_allow_html=True)
            
            display_df = display_df.reset_index(drop=True)
            output_df = display_df[['スタッフ番号', '氏名', '合計残業時間（時間:分）']].copy()
            
            over_45_mask = display_df['合計残業時間（10進法）'] >= 45
            
            def highlight_over_45(row):
                idx = row.name
                if idx < len(over_45_mask) and over_45_mask.iloc[idx]:
                    return ['background-color: #fff5f5; color: #e74c3c; font-weight: 600'] * len(row)
                return ['background-color: #ffffff'] * len(row)
            
            styled_df = output_df.style.apply(highlight_over_45, axis=1)
            styled_df = styled_df.set_properties(**{
                'font-size': '14px',
                'padding': '12px 16px',
                'border-bottom': '1px solid #f0f3f5'
            })
            styled_df = styled_df.set_table_styles([
                {'selector': 'th', 'props': [
                    ('background-color', '#f8fbfd'),
                    ('color', '#7f8c8d'),
                    ('font-weight', '500'),
                    ('font-size', '13px'),
                    ('padding', '12px 16px'),
                    ('text-align', 'left'),
                    ('border-bottom', '1px solid #e8eef3')
                ]}
            ])
            
            st.markdown('<div class="data-table">', unsafe_allow_html=True)
            st.dataframe(styled_df, use_container_width=True, height=500, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        else:
            st.error("必要な列が見つかりませんでした。")
            st.write("検出された列:", df.columns.tolist())
            st.info("CSVファイルには「スタッフ番号」「氏名(漢字)」「支払残業時間」「支払深残時間」の列が必要です。")
            
    except Exception as e:
        st.error(f"ファイルの読み込みに失敗しました: {e}")
