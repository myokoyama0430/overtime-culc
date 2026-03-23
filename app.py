import streamlit as st
import pandas as pd

st.set_page_config(page_title="残業時間集計", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Sans+JP:wght@300;400;500;600;700&display=swap');

    :root {
        /* ── Backgrounds ── */
        --bg:              #f6f8fc;
        --bg-surface:      #ffffff;
        --bg-surface-hover:#f0f4ff;
        --bg-muted:        #f1f5f9;

        /* ── Borders ── */
        --border:          rgba(15,23,42,0.08);
        --border-bright:   rgba(15,23,42,0.15);
        --border-accent:   rgba(99,102,241,0.35);

        /* ── Brand / Accent ── */
        --accent:          #6366f1;
        --accent-dark:     #4f46e5;
        --gradient:        linear-gradient(135deg, #6366f1 0%, #2563eb 50%, #0891b2 100%);
        --gradient-subtle: linear-gradient(135deg, rgba(99,102,241,0.06) 0%, rgba(37,99,235,0.04) 100%);

        /* ── Text Hierarchy ── */
        --text:            #0f172a;
        --text-body:       #374151;
        --text-secondary:  #6b7280;
        --text-muted:      #9ca3af;

        /* ── Semantic: Danger ── */
        --danger:          #dc2626;
        --danger-light:    #ef4444;
        --danger-bg:       rgba(239,68,68,0.06);
        --danger-border:   rgba(220,38,38,0.20);

        /* ── Semantic: Success ── */
        --success:         #16a34a;
        --success-bg:      rgba(22,163,74,0.06);

        /* ── Shape / Shadow ── */
        --radius:          14px;
        --radius-sm:       8px;
        --shadow-sm:       0 1px 3px rgba(15,23,42,0.06), 0 1px 2px rgba(15,23,42,0.04);
        --shadow-md:       0 4px 12px rgba(15,23,42,0.08), 0 2px 4px rgba(15,23,42,0.04);
        --shadow-accent:   0 4px 15px rgba(99,102,241,0.25);
    }

    * { font-family: 'Inter', 'Noto Sans JP', -apple-system, sans-serif; box-sizing: border-box; }

    html, body, .stApp {
        background-color: var(--bg) !important;
        color: var(--text-body) !important;
    }

    /* Subtle grid */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image:
            linear-gradient(rgba(99,102,241,0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(99,102,241,0.05) 1px, transparent 1px);
        background-size: 64px 64px;
        pointer-events: none;
        z-index: 0;
    }

    /* Glow orb — top-right, very subtle on light */
    .stApp::after {
        content: '';
        position: fixed;
        top: -150px; right: -150px;
        width: 500px; height: 500px;
        background: radial-gradient(circle, rgba(99,102,241,0.07) 0%, transparent 65%);
        pointer-events: none;
        z-index: 0;
    }

    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
        position: relative;
        z-index: 1;
    }

    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }
    .stDeployButton { display: none !important; }
    #MainMenu { display: none !important; }
    footer { display: none !important; }

    /* ===== HEADER ===== */
    .app-header {
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 60px;
        background: rgba(246,248,252,0.85);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-bottom: 1px solid var(--border);
        box-shadow: 0 1px 0 rgba(15,23,42,0.06);
        display: flex;
        align-items: center;
        padding: 0 32px;
        z-index: 1000;
        gap: 12px;
    }

    .logo-mark {
        width: 32px; height: 32px;
        background: var(--gradient);
        border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-size: 15px;
        box-shadow: 0 0 16px rgba(99,102,241,0.30);
        flex-shrink: 0;
    }

    .logo-name {
        font-size: 0.95rem;
        font-weight: 600;
        color: var(--text);
        letter-spacing: -0.01em;
    }

    .header-dot {
        width: 4px; height: 4px;
        background: var(--border-bright);
        border-radius: 50%;
        margin: 0 4px;
    }

    .header-sub {
        font-size: 0.82rem;
        color: var(--text-secondary);
        font-weight: 400;
    }

    /* ===== LAYOUT ===== */
    .content-area {
        padding-top: 80px;
        padding-bottom: 60px;
        padding-left: 40px;
        padding-right: 40px;
        max-width: 960px;
        margin: 0 auto;
    }

    @media (max-width: 768px) {
        .content-area { padding-left: 16px; padding-right: 16px; }
    }

    /* ===== HERO ===== */
    .hero {
        padding: 56px 0 40px;
        text-align: center;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(99,102,241,0.08);
        border: 1px solid rgba(99,102,241,0.25);
        border-radius: 100px;
        padding: 5px 14px;
        font-size: 0.76rem;
        font-weight: 600;
        color: #4f46e5;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 20px;
    }

    .hero-badge::before {
        content: '';
        width: 6px; height: 6px;
        background: var(--accent);
        border-radius: 50%;
        box-shadow: 0 0 6px rgba(99,102,241,0.5);
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }

    .hero h1 {
        font-size: 2.4rem;
        font-weight: 700;
        line-height: 1.2;
        letter-spacing: -0.03em;
        color: var(--text);
        margin-bottom: 14px;
    }

    .hero h1 .grad {
        background: var(--gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero p {
        font-size: 0.92rem;
        color: var(--text-secondary);
        line-height: 1.7;
        max-width: 380px;
        margin: 0 auto;
        font-weight: 400;
    }

    /* ===== UPLOAD ===== */
    .upload-wrap {
        max-width: 440px;
        margin: 32px auto 0;
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
        background: var(--bg-surface) !important;
        border: 1.5px dashed var(--border-bright) !important;
        border-radius: var(--radius) !important;
        padding: 44px 24px !important;
        min-height: 170px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: var(--shadow-sm) !important;
        transition: all 0.25s ease !important;
    }
    .stFileUploader [data-testid="stFileUploaderDropzone"]:hover {
        border-color: var(--border-accent) !important;
        background: rgba(99,102,241,0.03) !important;
        box-shadow: 0 0 0 4px rgba(99,102,241,0.08), var(--shadow-md) !important;
    }
    .stFileUploader [data-testid="stFileUploaderDropzone"] span {
        color: var(--text-secondary) !important;
        font-size: 0.87rem !important;
    }
    .stFileUploader [data-testid="stFileUploaderDropzone"] button {
        background: var(--gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 22px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        margin-top: 10px !important;
        box-shadow: var(--shadow-accent) !important;
        transition: all 0.2s !important;
    }
    .stFileUploader [data-testid="stFileUploaderDropzone"] button:hover {
        box-shadow: 0 6px 20px rgba(99,102,241,0.40) !important;
        transform: translateY(-1px) !important;
    }
    .stFileUploader small { display: none !important; }

    /* ===== FEATURE CARDS ===== */
    .features {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        max-width: 440px;
        margin: 28px auto 0;
    }

    .feat-card {
        background: var(--bg-surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-sm);
        box-shadow: var(--shadow-sm);
        padding: 16px 12px;
        text-align: center;
        transition: all 0.2s;
    }

    .feat-card:hover {
        background: var(--bg-surface-hover);
        border-color: var(--border-accent);
        box-shadow: var(--shadow-md);
        transform: translateY(-1px);
    }

    .feat-icon {
        font-size: 1.3rem;
        margin-bottom: 6px;
    }

    .feat-card h4 {
        font-size: 0.82rem;
        font-weight: 600;
        color: var(--text);
        margin-bottom: 3px;
    }

    .feat-card p {
        font-size: 0.76rem;
        color: var(--text-secondary);
        margin: 0;
    }

    /* ===== DIVIDER ===== */
    .section-divider {
        height: 1px;
        background: var(--border);
        margin: 28px 0;
    }

    /* ===== STATS ===== */
    .stats-row {
        display: flex;
        gap: 14px;
        margin-bottom: 24px;
        flex-wrap: wrap;
    }

    .stat-card {
        flex: 1;
        min-width: 160px;
        background: var(--bg-surface);
        border: 1px solid var(--border);
        border-top: none;
        border-radius: var(--radius);
        box-shadow: var(--shadow-sm);
        padding: 18px 20px;
        position: relative;
        overflow: hidden;
        transition: all 0.2s;
    }

    .stat-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: var(--gradient);
    }

    .stat-card.danger {
        border-color: var(--danger-border);
    }

    .stat-card.danger::before {
        background: linear-gradient(90deg, #dc2626, #f97316);
    }

    .stat-card:hover {
        box-shadow: var(--shadow-md);
        border-color: var(--border-bright);
    }

    .stat-label {
        font-size: 0.76rem;
        font-weight: 600;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-bottom: 8px;
    }

    .stat-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text);
        letter-spacing: -0.03em;
        line-height: 1;
        font-family: 'Inter', sans-serif;
    }

    .stat-card.danger .stat-value {
        color: var(--danger);
    }

    .stat-unit {
        font-size: 0.9rem;
        font-weight: 400;
        color: var(--text-secondary);
        margin-left: 2px;
    }

    /* ===== RESULT HEADER ===== */
    .result-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 14px;
    }

    .result-title {
        font-size: 0.92rem;
        font-weight: 600;
        color: var(--text);
        letter-spacing: -0.01em;
    }

    .pill {
        background: rgba(99,102,241,0.08);
        border: 1px solid rgba(99,102,241,0.20);
        color: #4f46e5;
        padding: 4px 12px;
        border-radius: 100px;
        font-size: 0.76rem;
        font-weight: 600;
    }

    .pill.danger {
        background: var(--danger-bg);
        border-color: var(--danger-border);
        color: var(--danger);
    }

    /* ===== TABLE ===== */
    .table-wrap {
        background: var(--bg-surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        box-shadow: var(--shadow-sm);
        overflow: hidden;
    }

    .table-scroll {
        max-height: 440px;
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: var(--border-bright) transparent;
    }

    .table-scroll::-webkit-scrollbar { width: 4px; }
    .table-scroll::-webkit-scrollbar-track { background: transparent; }
    .table-scroll::-webkit-scrollbar-thumb { background: var(--border-bright); border-radius: 4px; }

    .data-table {
        width: 100%;
        border-collapse: collapse;
    }

    .data-table thead {
        position: sticky;
        top: 0;
        z-index: 2;
    }

    .data-table th {
        background: var(--bg-muted);
        color: var(--text-secondary);
        font-size: 0.74rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        padding: 12px 18px;
        text-align: left;
        border-bottom: 1px solid var(--border-bright);
        white-space: nowrap;
    }

    .data-table td {
        padding: 13px 18px;
        font-size: 0.87rem;
        color: var(--text-body);
        border-bottom: 1px solid var(--border);
        transition: background 0.12s;
    }

    .data-table tr:last-child td { border-bottom: none; }

    .data-table tbody tr:hover td {
        background: var(--bg-muted);
    }

    .data-table td.num {
        font-family: 'Inter', monospace;
        font-variant-numeric: tabular-nums;
        font-weight: 500;
    }

    /* Warning rows */
    .data-table tr.warn td {
        background: var(--danger-bg);
    }

    .data-table tr.warn td:first-child {
        border-left: 3px solid var(--danger);
        padding-left: 15px;
    }

    .data-table tbody tr:hover.warn td {
        background: rgba(239,68,68,0.10);
    }

    .data-table tr.warn .time-badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: rgba(220,38,38,0.08);
        border: 1px solid var(--danger-border);
        color: var(--danger);
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.84rem;
        font-weight: 600;
        font-family: 'Inter', monospace;
    }

    .data-table tr.warn .time-badge::before {
        content: '⚠';
        font-size: 0.7rem;
    }

    .data-table tr:not(.warn) .time-badge {
        display: inline-block;
        font-family: 'Inter', monospace;
        font-weight: 500;
        color: var(--success);
        font-size: 0.87rem;
    }

    /* ===== CHECKBOX ===== */
    .stCheckbox label {
        font-size: 0.87rem !important;
        color: var(--text-body) !important;
        font-weight: 400 !important;
    }

    /* ===== BUTTONS ===== */
    .stDownloadButton button {
        background: var(--bg-surface) !important;
        border: 1px solid var(--border-bright) !important;
        color: var(--text-body) !important;
        border-radius: 8px !important;
        padding: 9px 18px !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        box-shadow: var(--shadow-sm) !important;
        transition: all 0.2s !important;
        width: 100% !important;
    }

    .stDownloadButton button:hover {
        background: var(--bg-muted) !important;
        border-color: var(--border-accent) !important;
        color: var(--text) !important;
        box-shadow: var(--shadow-md) !important;
    }

    .primary-btn .stDownloadButton button {
        background: var(--gradient) !important;
        border-color: transparent !important;
        color: white !important;
        box-shadow: var(--shadow-accent) !important;
    }

    .primary-btn .stDownloadButton button:hover {
        box-shadow: 0 6px 20px rgba(99,102,241,0.40) !important;
        transform: translateY(-1px) !important;
    }

    /* ===== EXPORT LABEL ===== */
    .export-label {
        font-size: 0.76rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-bottom: 10px;
        margin-top: 22px;
    }

    /* ===== ERROR ===== */
    .stAlert {
        background: var(--danger-bg) !important;
        border: 1px solid var(--danger-border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--danger) !important;
    }

    [data-testid="column"] { gap: 10px !important; }
</style>
""", unsafe_allow_html=True)


def decimal_to_hours_minutes(decimal_hours):
    if pd.isna(decimal_hours):
        return "0:00"
    hours = int(decimal_hours)
    minutes = int(round((decimal_hours - hours) * 60))
    return f"{hours}:{minutes:02d}"


# Header
st.markdown("""
<div class="app-header">
    <div class="logo-mark">⏱</div>
    <span class="logo-name">OvertimeAI</span>
    <div class="header-dot"></div>
    <span class="header-sub">残業時間集計システム</span>
</div>
<div class="content-area">
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <div class="hero-badge">AI-Powered Analytics</div>
    <h1>残業時間を<br><span class="grad">自動で可視化</span></h1>
    <p>CSVをアップロードするだけで、スタッフごとの残業時間を即時集計。45時間超の労働者をリアルタイムで検出します。</p>
</div>
""", unsafe_allow_html=True)

# Upload
st.markdown('<div class="upload-wrap">', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "CSV",
    type=["csv"],
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is None:
    st.markdown("""
    <div class="features">
        <div class="feat-card">
            <div class="feat-icon">⚡</div>
            <h4>自動集計</h4>
            <p>スタッフ別に即時合計</p>
        </div>
        <div class="feat-card">
            <div class="feat-icon">🕐</div>
            <h4>時間変換</h4>
            <p>時間:分で表示</p>
        </div>
        <div class="feat-card">
            <div class="feat-icon">🔴</div>
            <h4>超過検知</h4>
            <p>45h超を自動強調</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    try:
        try:
            df = pd.read_csv(uploaded_file, encoding="cp932")
        except Exception:
            uploaded_file.seek(0)
            try:
                df = pd.read_csv(uploaded_file, encoding="shift_jis")
            except Exception:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding="utf-8")

        df.columns = df.columns.str.strip()

        staff_col = name_col = site_col = overtime_col = late_overtime_col = None
        for col in df.columns:
            if "ｽﾀｯﾌ番号" in col or "スタッフ番号" in col:
                staff_col = col
            if "氏名" in col and "漢字" in col:
                name_col = col
            if "現場名" in col:
                site_col = col
            if "支払残業時間" in col:
                overtime_col = col
            if "支払深残時間" in col:
                late_overtime_col = col

        if all([staff_col, name_col, overtime_col, late_overtime_col]):
            agg_dict = {overtime_col: "sum", late_overtime_col: "sum"}
            group_cols = [staff_col, name_col]

            if site_col:
                agg_dict[site_col] = lambda x: ", ".join(x.dropna().unique())

            grouped = df.groupby(group_cols).agg(agg_dict).reset_index()
            grouped["total"] = grouped[overtime_col] + grouped[late_overtime_col]
            grouped["time_str"] = grouped["total"].apply(decimal_to_hours_minutes)

            if site_col:
                result = grouped[[staff_col, name_col, site_col, "total", "time_str"]].copy()
                result.columns = ["staff_no", "name", "site", "total", "time_str"]
            else:
                result = grouped[[staff_col, name_col, "total", "time_str"]].copy()
                result.columns = ["staff_no", "name", "total", "time_str"]
                result["site"] = ""

            result = result.sort_values("staff_no", ascending=True)

            total_staff = len(result)
            over_45 = len(result[result["total"] >= 45])
            rate = int(over_45 / total_staff * 100) if total_staff > 0 else 0

            # Stats
            st.markdown(f"""
            <div class="section-divider"></div>
            <div class="stats-row">
                <div class="stat-card">
                    <div class="stat-label">総スタッフ数</div>
                    <div class="stat-value">{total_staff}<span class="stat-unit">名</span></div>
                </div>
                <div class="stat-card danger">
                    <div class="stat-label">45時間超過</div>
                    <div class="stat-value">{over_45}<span class="stat-unit">名</span></div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">超過率</div>
                    <div class="stat-value">{rate}<span class="stat-unit">%</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Filter
            col_chk, _ = st.columns([2, 3])
            with col_chk:
                show_45 = st.checkbox("45時間以上のみ表示", value=False)

            display = result[result["total"] >= 45].copy() if show_45 else result.copy()
            title = "45時間以上の残業者" if show_45 else "スタッフ残業時間一覧"
            pill_class = "danger" if show_45 else ""

            st.markdown(f"""
            <div class="result-header">
                <span class="result-title">{title}</span>
                <span class="pill {pill_class}">{len(display)} 名</span>
            </div>
            """, unsafe_allow_html=True)

            # Table
            rows_html = ""
            for _, row in display.iterrows():
                cls = "warn" if row["total"] >= 45 else ""
                time_cell = f'<span class="time-badge">{row["time_str"]}</span>'
                rows_html += f'<tr class="{cls}"><td>{row["staff_no"]}</td><td>{row["name"]}</td><td style="color:var(--text-secondary)">{row["site"]}</td><td class="num">{time_cell}</td></tr>'

            st.markdown(f"""
            <div class="table-wrap">
                <div class="table-scroll">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>スタッフ番号</th>
                                <th>氏名</th>
                                <th>現場名</th>
                                <th>合計残業時間</th>
                            </tr>
                        </thead>
                        <tbody>{rows_html}</tbody>
                    </table>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Export
            def create_csv(data):
                export_df = data[["staff_no", "name", "site", "time_str"]].copy()
                export_df.columns = ["スタッフ番号", "氏名", "現場名", "合計残業時間"]
                return export_df.to_csv(index=False).encode("utf-8-sig")

            st.markdown('<div class="export-label">エクスポート</div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            over_45_data = result[result["total"] >= 45]
            with col1:
                st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
                st.download_button(
                    label=f"⬇  45時間以上を出力  ({len(over_45_data)}名)",
                    data=create_csv(over_45_data),
                    file_name="overtime_45plus.csv",
                    mime="text/csv",
                )
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.download_button(
                    label=f"⬇  全員を出力  ({len(result)}名)",
                    data=create_csv(result),
                    file_name="overtime_all.csv",
                    mime="text/csv",
                )

        else:
            st.error("必要な列が見つかりませんでした。CSVの形式を確認してください。")

    except Exception as e:
        st.error(f"読み込みエラー: {e}")

st.markdown('</div>', unsafe_allow_html=True)
