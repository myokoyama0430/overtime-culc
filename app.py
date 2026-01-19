import streamlit as st
import pandas as pd

st.set_page_config(page_title="残業時間集計", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #e8f4fc 0%, #d0e8f7 100%);
    }
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1200px;
    }
    h1 {
        color: #1a5f8a;
        font-size: 2.2rem;
        font-weight: 700;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #4da6d9;
        margin-bottom: 1.5rem;
    }
    h2, h3 {
        color: #2980b9;
        font-weight: 600;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #d6eaf8 0%, #aed6f1 100%);
        padding: 1rem;
    }
    [data-testid="stSidebar"] h2 {
        color: #1a5f8a;
        font-size: 1.2rem;
        border-bottom: 2px solid #5dade2;
        padding-bottom: 0.5rem;
    }
    .stFileUploader > div {
        background-color: #ffffff;
        border: 2px dashed #5dade2;
        border-radius: 12px;
        padding: 1.5rem;
    }
    .stDataFrame {
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        padding: 0.5rem;
    }
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
        margin-bottom: 0.8rem;
    }
    [data-testid="stMetric"] label {
        color: #2980b9;
        font-weight: 600;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #1a5f8a;
        font-size: 1.8rem;
    }
    .stRadio > label {
        color: #1a5f8a;
        font-weight: 500;
    }
    .stCheckbox > label {
        color: #1a5f8a;
        font-weight: 500;
    }
    div[data-testid="stAlert"] {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("残業時間集計アプリ")

def decimal_to_hours_minutes(decimal_hours):
    """10進法の時間を時間:分形式に変換"""
    if pd.isna(decimal_hours):
        return "0:00"
    hours = int(decimal_hours)
    minutes = int(round((decimal_hours - hours) * 60))
    return f"{hours}:{minutes:02d}"

uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=['csv'])

if uploaded_file is not None:
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
            
            st.sidebar.header("設定")
            
            sort_option = st.sidebar.radio(
                "並び順",
                ["合計残業時間（多い順）", "合計残業時間（少ない順）", "スタッフ番号（昇順）", "スタッフ番号（降順）"]
            )
            
            if sort_option == "合計残業時間（多い順）":
                result = result.sort_values('合計残業時間（10進法）', ascending=False)
            elif sort_option == "合計残業時間（少ない順）":
                result = result.sort_values('合計残業時間（10進法）', ascending=True)
            elif sort_option == "スタッフ番号（昇順）":
                result = result.sort_values('スタッフ番号', ascending=True)
            else:
                result = result.sort_values('スタッフ番号', ascending=False)
            
            st.sidebar.markdown("---")
            show_only_over_45 = st.sidebar.checkbox("45時間以上のみ表示", value=False)
            
            if show_only_over_45:
                display_df = result[result['合計残業時間（10進法）'] >= 45].copy()
                st.subheader(f"45時間以上の残業者一覧（{len(display_df)}名）")
            else:
                display_df = result.copy()
                over_45_count = len(result[result['合計残業時間（10進法）'] >= 45])
                st.subheader(f"全スタッフの残業時間一覧（{len(display_df)}名中、45時間以上: {over_45_count}名）")
            
            display_df = display_df.reset_index(drop=True)
            display_df.index = display_df.index + 1
            
            output_df = display_df[['スタッフ番号', '氏名', '合計残業時間（時間:分）']].copy()
            
            over_45_staff = set(display_df[display_df['合計残業時間（10進法）'] >= 45].index)
            
            def highlight_over_45(row):
                if row.name in over_45_staff:
                    return ['background-color: #ffe6e6; color: #c0392b; font-weight: 600'] * len(row)
                return ['background-color: #ffffff'] * len(row)
            
            styled_df = output_df.style.apply(highlight_over_45, axis=1)
            styled_df = styled_df.set_properties(**{
                'font-size': '14px',
                'padding': '8px 12px',
                'border-bottom': '1px solid #e0e0e0'
            })
            styled_df = styled_df.set_table_styles([
                {'selector': 'th', 'props': [
                    ('background-color', '#3498db'),
                    ('color', 'white'),
                    ('font-weight', '600'),
                    ('font-size', '14px'),
                    ('padding', '10px 12px'),
                    ('text-align', 'left')
                ]}
            ])
            
            st.dataframe(styled_df, use_container_width=True, height=550)
            
            st.sidebar.markdown("---")
            st.sidebar.metric("総スタッフ数", f"{len(result)}名")
            st.sidebar.metric("45時間以上", f"{len(result[result['合計残業時間（10進法）'] >= 45])}名")
            
        else:
            st.error("必要な列が見つかりませんでした。")
            st.write("検出された列:", df.columns.tolist())
            st.info("CSVファイルには「スタッフ番号」「氏名(漢字)」「支払残業時間」「支払深残時間」の列が必要です。")
            
    except Exception as e:
        st.error(f"ファイルの読み込みに失敗しました: {e}")
else:
    st.markdown("""
    <div style="background-color: #ffffff; border-radius: 12px; padding: 2rem; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.08); margin-top: 2rem;">
        <h3 style="color: #2980b9; margin-bottom: 1rem;">CSVファイルをアップロードしてください</h3>
        <p style="color: #5d6d7e; font-size: 1rem;">残業時間データを集計し、45時間以上のスタッフを強調表示します</p>
    </div>
    """, unsafe_allow_html=True)
