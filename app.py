import streamlit as st
import pandas as pd

st.set_page_config(page_title="残業時間集計", layout="wide")

st.title("残業時間集計アプリ")

def decimal_to_hours_minutes(decimal_hours):
    """10進法の時間を時間:分形式に変換"""
    if pd.isna(decimal_hours):
        return "0:00"
    hours = int(decimal_hours)
    minutes = int(round((decimal_hours - hours) * 60))
    return f"{hours}:{minutes:02d}"

def load_data():
    """CSVファイルを読み込む"""
    try:
        df = pd.read_csv(
            "attached_assets/過剰残業_1768802890577.csv",
            encoding="cp932"
        )
        return df
    except Exception as e:
        st.error(f"ファイルの読み込みに失敗しました: {e}")
        return None

df = load_data()

if df is not None:
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
        
        grouped['支払残業時間（時間:分）'] = grouped[overtime_col].apply(decimal_to_hours_minutes)
        grouped['支払深残時間（時間:分）'] = grouped[late_overtime_col].apply(decimal_to_hours_minutes)
        grouped['合計残業時間（時間:分）'] = grouped['合計残業時間（10進法）'].apply(decimal_to_hours_minutes)
        
        result = grouped[[staff_col, name_col, overtime_col, '支払残業時間（時間:分）', 
                          late_overtime_col, '支払深残時間（時間:分）', 
                          '合計残業時間（10進法）', '合計残業時間（時間:分）']].copy()
        
        result.columns = ['スタッフ番号', '氏名', '支払残業時間（10進法）', '支払残業時間（時間:分）',
                          '支払深残時間（10進法）', '支払深残時間（時間:分）',
                          '合計残業時間（10進法）', '合計残業時間（時間:分）']
        
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
        
        def highlight_over_45(row):
            if row['合計残業時間（10進法）'] >= 45:
                return ['background-color: #ffcccc; color: #cc0000; font-weight: bold'] * len(row)
            return [''] * len(row)
        
        styled_df = display_df.style.apply(highlight_over_45, axis=1)
        styled_df = styled_df.format({
            '支払残業時間（10進法）': '{:.2f}',
            '支払深残時間（10進法）': '{:.2f}',
            '合計残業時間（10進法）': '{:.2f}'
        })
        
        st.dataframe(styled_df, use_container_width=True, height=600)
        
        st.sidebar.markdown("---")
        st.sidebar.subheader("統計情報")
        st.sidebar.metric("総スタッフ数", f"{len(result)}名")
        st.sidebar.metric("45時間以上", f"{len(result[result['合計残業時間（10進法）'] >= 45])}名")
        st.sidebar.metric("平均残業時間", f"{result['合計残業時間（10進法）'].mean():.2f}時間")
        st.sidebar.metric("最大残業時間", f"{result['合計残業時間（10進法）'].max():.2f}時間")
        
    else:
        st.error("必要な列が見つかりませんでした。")
        st.write("検出された列:", df.columns.tolist())
