import streamlit as st
import pandas as pd

st.set_page_config(page_title="残業時間集計", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #e6f3ff;
    }
    .stMainBlockContainer {
        background-color: #e6f3ff;
    }
    h1, h2, h3 {
        color: #0066cc;
    }
    .stSidebar {
        background-color: #cce6ff;
    }
    [data-testid="stSidebar"] {
        background-color: #cce6ff;
    }
    .stFileUploader {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
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
            result = result.sort_values('合計残業時間（10進法）', ascending=False)
            
            st.sidebar.header("フィルター設定")
            show_only_over_45 = st.sidebar.checkbox("45時間以上のみ表示", value=False)
            
            if show_only_over_45:
                display_df = result[result['合計残業時間（10進法）'] >= 45].copy()
                st.subheader(f"45時間以上の残業者一覧 （{len(display_df)}名）")
            else:
                display_df = result.copy()
                over_45_count = len(result[result['合計残業時間（10進法）'] >= 45])
                st.subheader(f"全スタッフの残業時間一覧 （{len(display_df)}名中、45時間以上: {over_45_count}名）")
            
            output_df = display_df[['スタッフ番号', '氏名', '合計残業時間（時間:分）']].copy()
            
            def highlight_over_45(row):
                original_row = display_df[display_df['スタッフ番号'] == row['スタッフ番号']]
                if not original_row.empty and original_row['合計残業時間（10進法）'].values[0] >= 45:
                    return ['background-color: #ffcccc; color: #cc0000; font-weight: bold'] * len(row)
                return [''] * len(row)
            
            styled_df = output_df.style.apply(highlight_over_45, axis=1)
            
            st.dataframe(styled_df, use_container_width=True, height=600)
            
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
    st.info("CSVファイルをアップロードして、残業時間を集計してください。")
