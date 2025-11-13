import streamlit as st
import requests
import json

# -------------------- Page Config --------------------
st.set_page_config(
    page_title="🪄 النظام التحريري الذكي (Streamlit + n8n + AI)",
    page_icon="🪄",
    layout="wide"
)

# -------------------- Headline --------------------
st.markdown("""
<h1 style='text-align:center; color:#F9F9F9;'>🪄 نظام التحرير الذكي</h1>
<p style='text-align:center; color:#A8A8A8;'>
اكتب نصك بالعربية واختر السياسة التحريرية ليُعاد صياغته بأسلوب احترافي وفق السياسة المختارة 🎯
</p>
""", unsafe_allow_html=True)

# -------------------- Policy Cards --------------------
st.markdown("""
<style>
.policy-container {
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    margin-top: 25px;
}

/* القاعدة العامة */
.policy-card {
    flex: 1;
    min-width: 250px;
    background: #1E1E1E;
    border-radius: 15px;
    padding: 20px;
    margin: 10px;
    text-align: center;
    transition: all 0.4s ease;
    position: relative;
    overflow: hidden;
}

/* حافة مضيئة متحركة */
.policy-card::before {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 15px;
    padding: 2px;
    background: linear-gradient(90deg, #FFD700, #00BFFF, #ADFF2F, #FFD700);
    background-size: 300% 300%;
    -webkit-mask: 
        linear-gradient(#fff 0 0) content-box, 
        linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    animation: borderFlow 5s linear infinite;
    opacity: 0;
    transition: opacity 0.3s ease;
}

@keyframes borderFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* نبضة الألوان */
@keyframes pulse-gold {
    0% { box-shadow: 0 0 10px #FFD70055; }
    50% { box-shadow: 0 0 25px #FFD700AA; }
    100% { box-shadow: 0 0 10px #FFD70055; }
}
@keyframes pulse-blue {
    0% { box-shadow: 0 0 10px #00BFFF55; }
    50% { box-shadow: 0 0 25px #00BFFFAA; }
    100% { box-shadow: 0 0 10px #00BFFF55; }
}
@keyframes pulse-green {
    0% { box-shadow: 0 0 10px #ADFF2F55; }
    50% { box-shadow: 0 0 25px #ADFF2FAA; }
    100% { box-shadow: 0 0 10px #ADFF2F55; }
}

/* نجاح ميديا */
.policy-card.media:hover {
    transform: translateY(-6px);
    background-color: rgba(255, 215, 0, 0.1);
    animation: pulse-gold 1.5s infinite;
}
.policy-card.media:hover::before {
    opacity: 1;
}

/* غزة TV */
.policy-card.gaza:hover {
    transform: translateY(-6px);
    background-color: rgba(0, 191, 255, 0.1);
    animation: pulse-blue 1.5s infinite;
}
.policy-card.gaza:hover::before {
    opacity: 1;
}

/* نجاح نيوز */
.policy-card.news:hover {
    transform: translateY(-6px);
    background-color: rgba(173, 255, 47, 0.1);
    animation: pulse-green 1.5s infinite;
}
.policy-card.news:hover::before {
    opacity: 1;
}

.policy-card h4 {
    margin-bottom: 10px;
    position: relative;
    z-index: 2;
}
.policy-card p {
    position: relative;
    z-index: 2;
}
</style>

<hr>
<h3 style='text-align:center; color:#F9F9F9;'>🧭 ما هي السياسات التحريرية؟</h3>
<p style='color:#BEBEBE; text-align:center;'>
اختر الطريقة التي تود أن يُعاد بها تحرير النص — كل سياسة تعبّر عن أسلوب مختلف في الكتابة ✍️
</p>

<div class='policy-container'>

  <div class='policy-card media' style='border-top:3px solid #FFD700;'>
    <h4 style='color:#FFD700;'>🎓 نجاح ميديا</h4>
    <p style='color:#CCCCCC;'>
    أسلوب أكاديمي موضوعي يستخدم لغة رسمية دقيقة،
    يركّز على التحليل والوضوح دون عاطفة.
    </p>
  </div>

  <div class='policy-card gaza' style='border-top:3px solid #00BFFF;'>
    <h4 style='color:#00BFFF;'>🇵🇸 غزة TV</h4>
    <p style='color:#CCCCCC;'>
    أسلوب وطني وإنساني يعكس روح الصمود والانتماء،
    ويركّز على الجانب الإنساني في الأحداث.
    </p>
  </div>

  <div class='policy-card news' style='border-top:3px solid #ADFF2F;'>
    <h4 style='color:#ADFF2F;'>🗞️ نجاح نيوز</h4>
    <p style='color:#CCCCCC;'>
    أسلوب صحفي مباشر يعرض الخبر كما حدث فعليًا،
    بلغة بسيطة وواضحة دون مبالغة.
    </p>
  </div>

</div>

<p style='text-align:center; color:#A8A8A8; margin-top:25px; font-size:16px;'>
🪄 اختر السياسة التي ترغب بها من الأزرار التالية 👇
</p>
<hr>
""", unsafe_allow_html=True)

# -------------------- Text Input --------------------
user_text = st.text_area("✍️ أدخل النص هنا:", height=200, placeholder="اكتب أو الصق نص الخبر هنا...")

# -------------------- URLs --------------------
EDIT_URL = "http://localhost:5678/webhook/edit-article"
TRANSLATE_URL = "http://localhost:5678/webhook/translate"

# -------------------- State --------------------
for key, value in {
    "edited_news": None,
    "original_text": "",
    "translation_result": None,
    "last_language": None
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -------------------- Helpers --------------------
def _coerce_to_dict(payload):
    """Simple  
    Try to make sure the n8n response is a dictionary.
    - If the payload is already a dict, return it.
    - If it's a JSON string, parse it and return the dict.
    - Otherwise return a dict with key 'text' and the string form of the payload.
    This makes later code easier because we always work with a dict.
    """
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        try:
            return json.loads(payload)
        except Exception:
            return {"النص": payload}
    return {"النص": str(payload)}

def _extract_json(result):
    """ 
    Try to find the real data object inside an n8n response.
    n8n can return different shapes, like {'output': {...}} or {'text': '...'}.
    We check some common keys (output, text, data, result) and use the first one found.
    If none match, we fall back to the whole result.
    Finally, convert that candidate to a dict with _coerce_to_dict.
    """
    if isinstance(result, dict):
        cand = None
        for k in ("output", "text", "data", "result"):
            if k in result:
                cand = result[k]
                break
        return _coerce_to_dict(cand if cand is not None else result)
    return _coerce_to_dict(result)

def _normalize_keys(d):
    """ 
    Normalize keys from English to Arabic so the UI stays consistent.
    We map many possible input keys (like 'title', 'intro', 'body', 'tags')
    into fixed Arabic keys used by the app:
      - 'التصنيف' (category)
      - 'العنوان' (title)
      - 'المقدمة' (introduction)
      - 'التفاصيل' (details/body)
      - 'الخاتمة' (conclusion)
      - 'الكلمات_المفتاحية' (keywords)
    For keywords we accept a list or a comma string and always return a list of strings.
    """
    mapping = {
        "التصنيف": ["التصنيف", "category"],
        "العنوان": ["العنوان", "title"],
        "المقدمة": ["المقدمة", "introduction", "intro"],
        "التفاصيل": ["التفاصيل", "details", "body"],
        "الخاتمة": ["الخاتمة", "conclusion"],
        "الكلمات_المفتاحية": ["الكلمات_المفتاحية", "keywords", "tags"]
    }
    norm = {}
    for ar_key, aliases in mapping.items():
        val = ""
        for k in aliases:
            if k in d:
                val = d.get(k, "")
                break
        # Normalize keywords into a list of strings
        if ar_key == "الكلمات_المفتاحية":
            if isinstance(val, list):
                norm[ar_key] = [str(x) for x in val]
            elif isinstance(val, str):
                norm[ar_key] = [x.strip() for x in val.split(",") if x.strip()]
            else:
                norm[ar_key] = []
        else:
            norm[ar_key] = val
    return norm

def _styled_box(content_dict):
    """ 
    Return an HTML string that shows the article parts in the app theme.
    The function expects a dict with the normalized Arabic keys and
    builds a styled block of HTML that Streamlit will render.
    """
    return f"""
    <div style='background-color:#202020; padding:20px; border-radius:15px;'>
        <h4 style='color:#FFD700;'>📌 التصنيف</h4><p style='color:#EAEAEA;'>{content_dict.get('التصنيف','')}</p>
        <h4 style='color:#00BFFF;'>🗞️ العنوان</h4><p style='color:#EAEAEA;'>{content_dict.get('العنوان','')}</p>
        <h4 style='color:#FF69B4;'>✏️ المقدمة</h4><p style='color:#EAEAEA;'>{content_dict.get('المقدمة','')}</p>
        <h4 style='color:#ADFF2F;'>📖 التفاصيل</h4><p style='color:#EAEAEA;'>{content_dict.get('التفاصيل','')}</p>
        <h4 style='color:#FFB6C1;'>🧩 الخاتمة</h4><p style='color:#EAEAEA;'>{content_dict.get('الخاتمة','')}</p>
        <h4 style='color:#87CEEB;'>🏷️ الكلمات المفتاحية</h4><p style='color:#EAEAEA;'>{', '.join(content_dict.get('الكلمات_المفتاحية',[]))}</p>
    </div>
    """

def send_to_n8n(policy_id):
    """ 
    Send the user's original text and the chosen policy id to the edit webhook.
    - If there is no input text, show a warning and stop.
    - On success (HTTP 200) parse the response, normalize keys and save to session_state.
    - On failure, show an error message with the status or exception.
    """
    if not user_text.strip():
        st.warning("⚠️ الرجاء إدخال نص أولًا.")
        return
    payload = {"input_text": user_text, "policy_id": policy_id}
    try:
        with st.spinner("⏳ جاري المعالجة عبر النظام التحريري..."):
            response = requests.post(EDIT_URL, json=payload)
        if response.status_code == 200:
            result = response.json()
            parsed = _extract_json(result)
            normalized = _normalize_keys(parsed)
            st.session_state.original_text = user_text
            st.session_state.edited_news = normalized
            st.success("✅ تمت إعادة الصياغة بنجاح!")
        else:
            st.error(f"❌ خطأ من الخادم: {response.status_code}")
            st.code(response.text, language="json")
    except Exception as e:
        st.error(f"⚠️ فشل الاتصال بالنظام التحريري: {e}")

def translate_news(lang_code):
    """ 
    Translate the already-edited news into the given language code.
    - If there is no edited news yet, show a warning.
    - Send the edited content and target language to the translate webhook.
    - On success save the normalized translation in session_state and record language.
    - On failure show an error message.
    """
    if not st.session_state.edited_news:
        st.warning("⚠️ لا يوجد نص مُحرر بعد. الرجاء تنفيذ التحرير أولاً.")
        return
    payload = {"input_text": st.session_state.edited_news, "target_language": lang_code}
    try:
        with st.spinner(f"🔄 جاري الترجمة إلى {'الإنجليزية' if lang_code=='en' else 'العبرية'}..."):
            response = requests.post(TRANSLATE_URL, json=payload)
        if response.status_code == 200:
            result = response.json()
            parsed = _extract_json(result)         
            normalized = _normalize_keys(parsed)    
            st.session_state.translation_result = normalized
            st.session_state.last_language = lang_code
            st.success(f"✅ تمت الترجمة ({lang_code.upper()}) بنجاح!")
        else:
            st.error(f"❌ خطأ في الترجمة: {response.status_code}")
            st.code(response.text, language="json")
    except Exception as e:
        st.error(f"⚠️ فشل الاتصال بخدمة الترجمة: {e}")

# -------------------- Tabs --------------------
tab1, tab2, tab3 = st.tabs(["📰 التحرير", "🌍 الترجمة", "📊 المقارنة"])

# === Tab 1: Editing ===
with tab1:
    st.markdown("### 🎯 اختر السياسة التحريرية")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🎓 سياسة نجاح ميديا"):
            send_to_n8n("policy1")
    with c2:
        if st.button("🇵🇸 سياسة غزة TV"):
            send_to_n8n("policy2")
    with c3:
        if st.button("🗞️ سياسة نجاح نيوز"):
            send_to_n8n("policy3")

    if st.session_state.edited_news:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📝 النص الأصلي")
            st.info(st.session_state.original_text)
        with col2:
            st.markdown("### 🧾 النص المُعاد صياغته")
            st.markdown(_styled_box(st.session_state.edited_news), unsafe_allow_html=True)

# === Tab 2: Translation ===
with tab2:
    st.markdown("### 🌍 ترجمة النص إلى لغات أخرى")
    if st.session_state.edited_news:
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            if st.button("🇬🇧 ترجمة إلى الإنجليزية"):
                translate_news("en")
        with col_t2:
            if st.button("🇮🇱 ترجمة إلى العبرية"):
                translate_news("he")
        if st.session_state.translation_result:
            lang = st.session_state.last_language
            st.markdown(f"#### 💬 النتيجة ({'الإنجليزية' if lang=='en' else 'العبرية'})")
            st.markdown(_styled_box(st.session_state.translation_result), unsafe_allow_html=True)
    else:
        st.info("✏️ يرجى تحرير نص أولاً في تبويب التحرير قبل الترجمة.")

# === Tab 3: Comparison ===
with tab3:
    if st.session_state.edited_news and st.session_state.translation_result:
        st.markdown("### 📊 مقارنة النصوص (العربي ↔ المترجم)")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🧾 النص العربي")
            st.markdown(_styled_box(st.session_state.edited_news), unsafe_allow_html=True)
        with col2:
            st.markdown("#### 🌍 النص المترجم")
            st.markdown(_styled_box(st.session_state.translation_result), unsafe_allow_html=True)
    else:
        st.info("⚙️ قم بالتحرير والترجمة أولاً لرؤية المقارنة.")
