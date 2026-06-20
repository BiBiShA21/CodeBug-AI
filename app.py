import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="CodeBug AI",
    page_icon="🐛",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============ THEMES - GRADIENTS + NOISE ============
THEMES = {
    "Cyberpunk": {
        "primary": "#FF006E",
        "secondary": "#00D9FF",
        "gradient": "linear-gradient(135deg, #0A0E27 0%, #1a0a1a 50%, #0a1a1a 100%)",
    },
    "Coding": {
        "primary": "#1E90FF",
        "secondary": "#00CED1",
        "gradient": "linear-gradient(135deg, #0D1117 0%, #0a1a2e 50%, #081a2a 100%)",
    },
    "Gaming": {
        "primary": "#FF00FF",
        "secondary": "#00FFFF",
        "gradient": "linear-gradient(135deg, #0A0F1F 0%, #1a0a2e 50%, #0a1a3e 100%)",
    },
    "Space": {
        "primary": "#6A0DAD",
        "secondary": "#00D4FF",
        "gradient": "linear-gradient(135deg, #0B0014 0%, #1a0a2e 50%, #0a1a3a 100%)",
    },
    "Anime": {
        "primary": "#FF1493",
        "secondary": "#FFD700",
        "gradient": "linear-gradient(135deg, #1A1A2E 0%, #2a1a1a 50%, #1a2a2a 100%)",
    },
    "Hacker": {
        "primary": "#00FF00",
        "secondary": "#00FF00",
        "gradient": "linear-gradient(135deg, #000000 0%, #0a1a0a 50%, #000a00 100%)",
    },
    "Minimal": {
        "primary": "#FFFFFF",
        "secondary": "#FF00FF",
        "gradient": "linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 50%, #1a2a2a 100%)",
    },
    "Light": {
        "primary": "#3498DB",
        "secondary": "#2ECC71",
        "gradient": "linear-gradient(135deg, #0D1a2E 0%, #0a2a2e 50%, #0a1a3a 100%)",
    },
    "Barbie": {
        "primary": "#FF1493",
        "secondary": "#FF69B4",
        "gradient": "linear-gradient(135deg, #2a0a1a 0%, #3a1a2a 50%, #2a1a2a 100%)",
    },
    "Cars": {
        "primary": "#DC143C",
        "secondary": "#FFD700",
        "gradient": "linear-gradient(135deg, #1C1C1C 0%, #2a1a0a 50%, #1a2a0a 100%)",
    }
}

# ============ CUSTOM CSS - PREMIUM NOISE + GRADIENTS ============
def get_theme_css(theme_name):
    theme = THEMES[theme_name]
    
    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@700&family=Inter:wght@400;500;600;700&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
        }}
        
        html, body {{
            height: 100vh;
            width: 100vw;
            overflow: hidden !important;
            -ms-overflow-style: none;
            scrollbar-width: none;
        }}
        
        html::-webkit-scrollbar, body::-webkit-scrollbar {{
            display: none;
        }}
        
        /* PREMIUM GRADIENT + NOISE BACKGROUND */
        .stApp {{
            background: {theme['gradient']};
            background-attachment: fixed;
            overflow: hidden !important;
            height: 100vh;
            position: relative;
        }}
        
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' result='noise' seed='2' /%3E%3C/filter%3E%3Crect width='400' height='400' fill='%23ffffff' filter='url(%23noiseFilter)' opacity='0.03'/%3E%3C/svg%3E");
            background-size: 400px 400px;
            background-repeat: repeat;
            pointer-events: none;
            z-index: 0;
        }}
        
        [data-testid="stAppViewContainer"] {{
            background: {theme['gradient']};
            overflow: hidden !important;
            height: 100vh;
            padding: 0 !important;
            margin: 0 !important;
            position: relative;
            z-index: 1;
        }}
        
        [data-testid="stMainBlockContainer"] {{
            overflow: hidden !important;
            height: 100vh;
            padding: 12px !important;
            display: flex;
            flex-direction: column;
            position: relative;
            z-index: 2;
        }}
        
        /* HIDE DEPLOY AND OTHER UI */
        [data-testid="stToolbar"] {{
            display: none !important;
        }}
        
        [data-testid="viewerBadge"] {{
            display: none !important;
        }}
        
        header {{
            display: none !important;
        }}
        
        footer {{
            display: none !important;
        }}
        
        /* HEADING - IBM PLEX SANS */
        h1 {{
            font-family: 'IBM Plex Sans', sans-serif !important;
            font-weight: 700 !important;
            color: #FFFFFF !important;
            font-size: 2.2rem !important;
            text-shadow: 0 2px 10px rgba(0,0,0,0.8);
            margin: 0 !important;
            padding: 0 !important;
        }}
        
        h2, h3 {{
            font-family: 'IBM Plex Sans', sans-serif !important;
            font-weight: 700 !important;
            color: #FFFFFF !important;
            text-shadow: 0 1px 5px rgba(0,0,0,0.5);
            margin: 0 !important;
            padding: 0 !important;
        }}
        
        /* TEXT - WHITE */
        .stMarkdown, .stCaption, p, label {{
            color: #FFFFFF !important;
        }}
        
        /* CODE BOX - TRANSPARENT */
        .stTextArea {{
            background-color: transparent !important;
        }}
        
        .stTextArea textarea {{
            font-family: 'Courier New', monospace !important;
            font-size: 13px !important;
            line-height: 1.6 !important;
            border: 2px solid {theme['primary']} !important;
            border-radius: 8px !important;
            background-color: rgba(0, 0, 0, 0.15) !important;
            color: #FFFFFF !important;
            scrollbar-width: none;
            padding: 12px !important;
            resize: none !important;
            caret-color: {theme['secondary']};
        }}
        
        .stTextArea textarea::-webkit-scrollbar {{
            display: none;
        }}
        
        .stTextArea textarea:focus {{
            background-color: rgba(0, 0, 0, 0.2) !important;
            border-color: {theme['secondary']} !important;
            box-shadow: 0 0 15px {theme['primary']} !important;
            outline: none;
        }}
        
        .stTextArea textarea::placeholder {{
            color: rgba(255, 255, 255, 0.4) !important;
        }}
        
        /* FEEDBACK BOX - TRANSPARENT - FIXED HEIGHT */
        .feedback-box {{
            border: 2px solid {theme['primary']};
            border-radius: 8px;
            padding: 12px;
            height: 380px;
            overflow-y: auto;
            overflow-x: hidden;
            background-color: rgba(0, 0, 0, 0.15);
            color: #FFFFFF;
            scrollbar-width: none;
        }}

        .feedback-box::-webkit-scrollbar {{
            display: none;
        }}
        
        .feedback-content {{
            font-family: 'Inter', sans-serif !important;
            font-size: 13px !important;
            line-height: 1.6 !important;
            color: #FFFFFF !important;
        }}
        
        /* BUTTONS - GRADIENT */
        .stButton > button {{
            border: none !important;
            background: linear-gradient(135deg, {theme['primary']}, {theme['secondary']}) !important;
            color: #000 !important;
            font-weight: bold !important;
            border-radius: 8px !important;
            font-family: 'IBM Plex Sans', sans-serif !important;
            height: 40px !important;
            transition: all 0.3s ease !important;
        }}
        
        .stButton > button:hover {{
            box-shadow: 0 0 20px {theme['primary']} !important;
            transform: translateY(-2px) !important;
        }}
        
        /* SELECTBOX - GRADIENT BUTTONS - SMOOTH CORNERS */
        .stSelectbox {{
            color: #FFFFFF !important;
        }}
        
        .stSelectbox > div > div {{
            background: linear-gradient(135deg, {theme['primary']}, {theme['secondary']}) !important;
            border-radius: 8px !important;
        }}
        
        .stSelectbox [data-baseweb="select"] {{
            background: linear-gradient(135deg, {theme['primary']}, {theme['secondary']}) !important;
            border-radius: 8px !important;
        }}
        
        .stSelectbox button {{
            background: linear-gradient(135deg, {theme['primary']}, {theme['secondary']}) !important;
            color: #000 !important;
            font-weight: bold !important;
            border: none !important;
            border-radius: 8px !important;
        }}
        
        .stSelectbox button > div {{
            border-radius: 8px !important;
        }}
        
        .stSelectbox button:hover {{
            box-shadow: 0 0 15px {theme['primary']} !important;
        }}
        
        [data-baseweb="select"] button {{
            background: linear-gradient(135deg, {theme['primary']}, {theme['secondary']}) !important;
            color: #000 !important;
            font-weight: bold !important;
        }}
        
        div[role="listbox"] {{
            background-color: rgba(0, 0, 0, 0.9) !important;
            color: #FFFFFF !important;
            border: 2px solid {theme['primary']} !important;
        }}
        
        div[role="option"] {{
            background-color: rgba(0, 0, 0, 0.6) !important;
            color: #FFFFFF !important;
        }}
        
        div[role="option"]:hover {{
            background-color: {theme['primary']} !important;
        }}
        
        /* DIVIDERS */
        hr {{
            border-color: {theme['primary']} !important;
            opacity: 0.5;
            margin: 8px 0 !important;
        }}
        
        /* REMOVE SIDEBAR */
        [data-testid="stSidebar"] {{
            display: none !important;
        }}
        
        /* SMOOTH CONTAINERS */
        .element-container {{
            margin: 0 !important;
            padding: 0 !important;
        }}
        
        .stColumn {{
            gap: 0 !important;
        }}
    </style>
    """

# ============ SESSION STATE ============
if "theme" not in st.session_state:
    st.session_state.theme = "Cyberpunk"
if "code" not in st.session_state:
    st.session_state.code = ""
if "feedback" not in st.session_state:
    st.session_state.feedback = ""

# Apply CSS
st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

# ============ HEADER WITH THEME AT TOP RIGHT ============
header_col1, header_col2, header_col3 = st.columns([0.8, 2, 1], gap="small")

with header_col2:
    st.markdown(
        f"""
        <div style='text-align: center; padding: 8px 0;'>
            <h1 style='margin: 0; padding: 0;'>🐛 CodeBug <span style='color: {THEMES[st.session_state.theme]["secondary"]};'>AI</span></h1>
            <p style='color: #CCC; font-size: 13px; margin: 3px 0; padding: 0;'>AI Code Reviewer • Smart • Fast • Friendly</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with header_col3:
    st.markdown("<div style='padding-top: 8px; padding-bottom: 0;'><b style='font-size: 13px;'>Theme</b></div>", unsafe_allow_html=True)
    theme_options = list(THEMES.keys())
    current_idx = theme_options.index(st.session_state.theme)
    
    selected_theme = st.selectbox(
        "Select Theme",
        theme_options,
        index=current_idx,
        label_visibility="collapsed",
        key="theme_selector"
    )
    
    if selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
        st.rerun()

st.divider()

# ============ CONTROLS BAR ============
control_col1, control_col2, control_col3, control_col4 = st.columns([1, 1, 0.9, 1.1], gap="small")

with control_col1:
    language = st.selectbox(
        "Language",
        ["Python", "JavaScript", "Java", "C++", "C#", "Go", "Ruby", "PHP", "TypeScript", "Swift"],
        label_visibility="collapsed",
        key="lang"
    )

with control_col2:
    feedback_style = st.selectbox(
        "Feedback Style",
        ["Gen-Z", "Professional", "Friendly", "Mentor"],
        label_visibility="collapsed",
        key="style"
    )

with control_col3:
    if st.button("📝 Sample", use_container_width=True, key="sample_btn"):
        st.session_state.code = """def greet(name):
    return f"Hello {name}"
    
print(greet("World"))"""
        st.rerun()

with control_col4:
    btn_col1, btn_col2 = st.columns(2, gap="small")
    with btn_col1:
        analyze_btn = st.button("🚀 Analyze", use_container_width=True)
    with btn_col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.code = ""
            st.session_state.feedback = ""
            st.rerun()

st.divider()

# ============ MAIN PANELS - FULL HEIGHT ============
code_col, feedback_col = st.columns(2, gap="small")

theme_color = THEMES[st.session_state.theme]

with code_col:
    st.markdown("### 💻 User Code", unsafe_allow_html=True)
    code_input = st.text_area(
        "Paste code here:",
        value=st.session_state.code,
        height=380,
        label_visibility="collapsed"
    )
    st.session_state.code = code_input

with feedback_col:
    st.markdown("### 🤖 AI Feedback", unsafe_allow_html=True)
    
    if st.session_state.feedback:
        feedback_html = f"""
        <div class='feedback-box'>
            <div class='feedback-content'>
                {st.session_state.feedback}
            </div>
        </div>
        """
        st.markdown(feedback_html, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='
            border: 2px dashed {theme_color["secondary"]};
            border-radius: 8px;
            padding: 12px;
            height: 380px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            color: #CCC;
            background-color: rgba(0, 0, 0, 0.15);
        '>
        <p>👈 Paste code & click <strong>Analyze</strong> 🚀</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ============ STATUS BAR ============
status_col1, status_col2, status_col3, status_col4 = st.columns(4, gap="small")

with status_col1:
    lines = len(st.session_state.code.split('\n')) if st.session_state.code else 0
    st.caption(f"📝 Lines: `{lines}`")

with status_col2:
    chars = len(st.session_state.code) if st.session_state.code else 0
    st.caption(f"✍️ Chars: `{chars}`")

with status_col3:
    st.caption(f"🎨 Theme: `{st.session_state.theme}`")

with status_col4:
    st.caption("✅ Ready")

# ============ ANALYZE CODE ============
if analyze_btn:
    if not code_input.strip():
        st.error("❌ Paste some code first!")
    else:
        with st.spinner("🔍 Analyzing..."):
            try:
                style_prompts = {
                    "Gen-Z": """Analyze this {language} code and respond with this EXACT format:

🚨 **ISSUE:**
[Brief 1-2 line issue description]

✅ **CORRECTED CODE:**
```{language}
[Write the COMPLETE fixed code here]
```

💡 **WHY IT WORKS:**
[1-2 line explanation in Gen-Z style with emojis]""",
                    
                    "Professional": """Analyze this {language} code and respond with this EXACT format:

⚠️ **ISSUE IDENTIFIED:**
[Brief 1-2 line issue description]

✅ **CORRECTED CODE:**
```{language}
[Write the COMPLETE fixed code here]
```

💡 **EXPLANATION:**
[1-2 line professional explanation]""",
                    
                    "Friendly": """Analyze this {language} code and respond with this EXACT format:

🔴 **WHAT'S WRONG:**
[Brief 1-2 line issue description]

🟢 **HERE'S THE FIX:**
```{language}
[Write the COMPLETE fixed code here]
```

🌟 **WHY THIS WORKS:**
[1-2 line friendly explanation with encouraging tone]""",
                    
                    "Mentor": """Analyze this {language} code and respond with this EXACT format:

📌 **THE ISSUE:**
[Brief 1-2 line issue description]

🎯 **THE CORRECTED CODE:**
```{language}
[Write the COMPLETE fixed code here]
```

🚀 **KEY LEARNING:**
[1-2 line explanation about what the developer should learn]"""
                }
                
                prompt = style_prompts[feedback_style].format(language=language) + f"\n\nUser's Code:\n```{language}\n{code_input}\n```"
                
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(prompt)
                
                st.session_state.feedback = response.text
                st.success("✅ Analysis Complete!")
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

st.markdown(f"<div style='text-align: center; color: #888; font-size: 11px; margin-top: 8px;'>Made with ❤️ for developers • CodeBug AI v2.3</div>", unsafe_allow_html=True)