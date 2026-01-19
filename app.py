import streamlit as st
import pandas as pd

st.set_page_config(page_title="残業時間集計", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;600;700&display=swap');
    
    :root {
        --primary: #0ea5e9;
        --primary-dark: #0284c7;
        --primary-light: #e0f2fe;
        --text-primary: #0f172a;
        --text-secondary: #64748b;
        --text-muted: #94a3b8;
        --bg-main: #f8fafc;
        --bg-card: #ffffff;
        --border: #e2e8f0;
        --danger: #ef4444;
        --danger-light: #fef2f2;
        --radius: 12px;
        --radius-sm: 8px;
    }
    
    * { font-family: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif; }
    
    .stApp { background-color: var(--bg-main); }
    .main .block-container { padding: 0; max-width: 100%; }
    header[data-testid="stHeader"] { display: none; }
    
    [data-testid="stSidebar"] {
        background-color: var(--bg-card);
        border-right: 1px solid var(--border);
        padding-top: 80px;
    }
    [data-testid="stSidebar"] > div:first-child { padding: 1.5rem; }
    
    [data-testid="collapsedControl"] {
        background: var(--primary) !important;
        color: white !important;
        border-radius: 8px !important;
        top: 70px !important;
        left: 10px !important;
    }
    [data-testid="collapsedControl"] svg {
        fill: white !important;
    }
    [data-testid="collapsedControl"]:hover {
        background: var(--primary-dark) !important;
    }
    
    .app-header {
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 60px;
        background: var(--bg-card);
        border-bottom: 1px solid var(--border);
        display: flex;
        align-items: center;
        padding: 0 24px;
        z-index: 1000;
    }
    
    .app-logo { display: flex; align-items: center; gap: 10px; }
    
    .logo-icon {
        width: 36px; height: 36px;
        background: linear-gradient(135deg, var(--primary) 0%, #06b6d4 100%);
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 18px;
    }
    
    .logo-text {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .content-area {
        padding-top: 80px;
        padding-left: 40px;
        padding-right: 40px;
        max-width: 900px;
        margin: 0 auto;
    }
    
    @media (max-width: 768px) {
        .content-area { padding-left: 16px; padding-right: 16px; }
        .hero h1 { font-size: 1.6rem !important; }
        .feature-grid { grid-template-columns: 1fr !important; }
    }
    
    .hero {
        text-align: center;
        padding: 40px 0 24px;
    }
    
    .hero h1 {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 8px;
    }
    
    .hero h1 span {
        background: linear-gradient(135deg, var(--primary) 0%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero p {
        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.6;
        max-width: 400px;
        margin: 0 auto;
    }
    
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        max-width: 480px;
        margin: 20px auto 0;
    }
    
    .feature-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-sm);
        padding: 14px 10px;
        text-align: center;
    }
    
    .feature-card h4 {
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 2px;
    }
    
    .feature-card p {
        font-size: 0.65rem;
        color: var(--text-muted);
    }
    
    .result-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 16px 0 12px;
    }
    
    .result-header h2 {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .badge {
        background: var(--primary-light);
        color: var(--primary-dark);
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    .data-table {
        width: 100%;
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        border-collapse: separate;
        border-spacing: 0;
        overflow: hidden;
    }
    
    .data-table th {
        background: #f8fafc;
        color: var(--text-muted);
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        padding: 12px 16px;
        text-align: left;
        border-bottom: 1px solid var(--border);
    }
    
    .data-table td {
        padding: 12px 16px;
        font-size: 0.85rem;
        color: var(--text-primary);
        border-bottom: 1px solid #f1f5f9;
    }
    
    .data-table tr:last-child td { border-bottom: none; }
    
    .data-table tr.warning {
        background: var(--danger-light);
    }
    
    .data-table tr.warning td {
        color: var(--danger);
        font-weight: 600;
    }
    
    .data-table tr.warning td:first-child {
        border-left: 4px solid var(--danger);
    }
    
    .table-scroll {
        max-height: 420px;
        overflow-y: auto;
        border-radius: var(--radius);
    }
    
    .sidebar-label {
        font-size: 0.65rem;
        font-weight: 600;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 8px;
    }
    
    .stat-box {
        background: var(--bg-main);
        border: 1px solid var(--border);
        border-radius: var(--radius-sm);
        padding: 12px;
        margin-bottom: 8px;
    }
    
    .stat-box .label {
        font-size: 0.65rem;
        color: var(--text-muted);
    }
    
    .stat-box .value {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text-primary);
    }
    
    .stat-box .value.red { color: var(--danger); }
    
    .filter-box {
        background: var(--bg-main);
        border: 1px solid var(--border);
        border-radius: var(--radius-sm);
        padding: 8px 12px;
    }
    
    .stCheckbox label { font-size: 0.8rem !important; color: var(--text-primary) !important; }
    
    .export-buttons { margin-top: 20px; }
    .export-buttons .stDownloadButton button {
        width: 100% !important;
        background: var(--primary) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 16px !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
    }
    .export-buttons .stDownloadButton button:hover {
        background: var(--primary-dark) !important;
    }
    
    .upload-container {
        max-width: 400px;
        margin: 24px auto;
    }
    
    .stFileUploader { margin: 0 !important; }
    .stFileUploader > div { background: transparent !important; padding: 0 !important; }
    .stFileUploader label { display: none !important; }
    .stFileUploader section { 
        padding: 0 !important; 
        background: transparent !important; 
        border: none !important; 
    }
    .stFileUploader [data-testid="stFileUploaderDropzone"] {
        background: var(--bg-card) !important;
        border: 2px dashed var(--border) !important;
        border-radius: var(--radius) !important;
        padding: 40px 24px !important;
        min-height: 160px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.2s ease !important;
    }
    .stFileUploader [data-testid="stFileUploaderDropzone"]:hover {
        border-color: var(--primary) !important;
        background: #f0f9ff !important;
    }
    .stFileUploader [data-testid="stFileUploaderDropzone"] span {
        color: var(--text-secondary) !important;
        font-size: 0.85rem !important;
    }
    .stFileUploader [data-testid="stFileUploaderDropzone"] button {
        background: var(--primary) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: 500 !important;
        margin-top: 8px !important;
    }
    .stFileUploader [data-testid="stFileUploaderDropzone"] button:hover {
        background: var(--primary-dark) !important;
    }
    .stFileUploader small {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="app-header">
    <div class="app-logo">
        <div class="logo-icon">📊</div>
        <span class="logo-text">残業時間集計</span>
    </div>
</div>
<div class="content-area">
""", unsafe_allow_html=True)

def decimal_to_hours_minutes(decimal_hours):
    if pd.isna(decimal_hours):
        return "0:00"
    hours = int(decimal_hours)
    minutes = int(round((decimal_hours - hours) * 60))
    return f"{hours}:{minutes:02d}"

st.markdown("""
<div class="hero">
    <h1>残業時間を<span>自動集計</span></h1>
    <p>CSVファイルをアップロードするだけで、スタッフごとの残業時間を自動集計。45時間以上の残業者を一目で確認できます。</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="upload-container">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("CSVファイルをドラッグ＆ドロップ、またはクリックして選択", type=['csv'], label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is None:
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card"><h4>自動集計</h4><p>スタッフごとに合計</p></div>
        <div class="feature-card"><h4>時間変換</h4><p>時間:分で表示</p></div>
        <div class="feature-card"><h4>警告表示</h4><p>45h超を強調</p></div>
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
        
        staff_col = name_col = site_col = overtime_col = late_overtime_col = None
        for col in df.columns:
            if "ｽﾀｯﾌ番号" in col or "スタッフ番号" in col: staff_col = col
            if "氏名" in col and "漢字" in col: name_col = col
            if "現場名" in col: site_col = col
            if "支払残業時間" in col: overtime_col = col
            if "支払深残時間" in col: late_overtime_col = col
        
        if all([staff_col, name_col, overtime_col, late_overtime_col]):
            agg_dict = {overtime_col: 'sum', late_overtime_col: 'sum'}
            group_cols = [staff_col, name_col]
            
            if site_col:
                agg_dict[site_col] = lambda x: ', '.join(x.dropna().unique())
            
            grouped = df.groupby(group_cols).agg(agg_dict).reset_index()
            
            grouped['total'] = grouped[overtime_col] + grouped[late_overtime_col]
            grouped['time_str'] = grouped['total'].apply(decimal_to_hours_minutes)
            
            if site_col:
                result = grouped[[staff_col, name_col, site_col, 'total', 'time_str']].copy()
                result.columns = ['staff_no', 'name', 'site', 'total', 'time_str']
            else:
                result = grouped[[staff_col, name_col, 'total', 'time_str']].copy()
                result.columns = ['staff_no', 'name', 'total', 'time_str']
                result['site'] = ''
            
            result = result.sort_values('staff_no', ascending=True)
            
            total_staff = len(result)
            over_45 = len(result[result['total'] >= 45])
            
            st.sidebar.markdown('<p class="sidebar-label">統計</p>', unsafe_allow_html=True)
            st.sidebar.markdown(f'''
            <div class="stat-box"><p class="label">総スタッフ数</p><p class="value">{total_staff}名</p></div>
            <div class="stat-box"><p class="label">45時間以上</p><p class="value red">{over_45}名</p></div>
            ''', unsafe_allow_html=True)
            
            st.sidebar.markdown('<p class="sidebar-label">フィルター</p>', unsafe_allow_html=True)
            st.sidebar.markdown('<div class="filter-box">', unsafe_allow_html=True)
            show_45 = st.sidebar.checkbox("45時間以上のみ表示", value=False)
            st.sidebar.markdown('</div>', unsafe_allow_html=True)
            
            if show_45:
                display = result[result['total'] >= 45].copy()
                title, badge_text = "45時間以上の残業者", f"{len(display)}名"
            else:
                display = result.copy()
                title, badge_text = "スタッフ残業時間一覧", f"{len(display)}名"
            
            st.markdown(f'''
            <div class="result-header">
                <h2>{title}</h2>
                <span class="badge">{badge_text}</span>
            </div>
            ''', unsafe_allow_html=True)
            
            rows_html = ""
            for _, row in display.iterrows():
                cls = "warning" if row['total'] >= 45 else ""
                rows_html += f'<tr class="{cls}"><td>{row["staff_no"]}</td><td>{row["name"]}</td><td>{row["site"]}</td><td>{row["time_str"]}</td></tr>'
            
            st.markdown(f'''
            <div class="table-scroll">
                <table class="data-table">
                    <thead><tr><th>スタッフ番号</th><th>氏名</th><th>現場名</th><th>合計残業時間</th></tr></thead>
                    <tbody>{rows_html}</tbody>
                </table>
            </div>
            ''', unsafe_allow_html=True)
            
            def create_csv(data):
                export_df = data[['staff_no', 'name', 'site', 'time_str']].copy()
                export_df.columns = ['スタッフ番号', '氏名', '現場名', '合計残業時間']
                return export_df.to_csv(index=False).encode('utf-8-sig')
            
            st.markdown('<div class="export-buttons">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                over_45_data = result[result['total'] >= 45]
                st.download_button(
                    label=f"45時間以上をCSV出力 ({len(over_45_data)}名)",
                    data=create_csv(over_45_data),
                    file_name="overtime_45plus.csv",
                    mime="text/csv"
                )
            with col2:
                st.download_button(
                    label=f"全員をCSV出力 ({len(result)}名)",
                    data=create_csv(result),
                    file_name="overtime_all.csv",
                    mime="text/csv"
                )
            st.markdown('</div>', unsafe_allow_html=True)
            
        else:
            st.error("必要な列が見つかりませんでした。")
            
    except Exception as e:
        st.error(f"読み込みエラー: {e}")

st.markdown('</div>', unsafe_allow_html=True)
