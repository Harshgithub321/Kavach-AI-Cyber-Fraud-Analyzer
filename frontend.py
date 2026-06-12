import feedparser
from streamlit_autorefresh import st_autorefresh
import feedparser
import os
import random
import google.generativeai as genai
import streamlit as st
import pandas as pd
import re
import matplotlib.pyplot as plt
GEMINI_API_KEY = GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

gemini_model = genai.GenerativeModel("gemini-2.5-flash")

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="AI Fraud Threat Analyzer",
    page_icon="🛡️",
    layout="wide"
)

refresh_count = st_autorefresh(
    interval=60000,
    key="news_rotation"
)


# ================= CSS =================

st.markdown("""
<style>
.stApp {
    background:
        linear-gradient(rgba(2,6,23,0.86), rgba(2,6,23,0.94)),
        url("https://images.unsplash.com/photo-1510511459019-5dda7724fd87");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: white;
}

/* Main container spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Title */
.main-title {
    font-size: 56px;
    font-weight: 950;
    color: #38bdf8;
    text-align: center;
    letter-spacing: 1px;
    text-shadow:
        0 0 8px #38bdf8,
        0 0 20px rgba(56,189,248,0.9),
        0 0 45px rgba(56,189,248,0.6);
    margin-bottom: 8px;
}

.sub-title {
    text-align: center;
    color: #e2e8f0;
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 28px;
}

/* Glass card */
.card {
    background: rgba(15, 23, 42, 0.84);
    backdrop-filter: blur(14px);
    padding: 30px;
    border-radius: 24px;
    border: 1px solid rgba(56,189,248,0.32);
    box-shadow:
        0 0 25px rgba(56,189,248,0.14),
        inset 0 0 18px rgba(255,255,255,0.03);
    margin-bottom: 25px;
}

/* News card */
.news-box {
    background: rgba(15,23,42,0.86);
    padding: 12px;
    border-radius: 14px;
    border: 1px solid rgba(56,189,248,0.55);
    margin-bottom: 10px;
    color: #e0f2fe;
    font-size: 13px;
    font-weight: 600;
    box-shadow: 0 0 14px rgba(56,189,248,0.18);
}

/* Button */
.stButton button {
    background: linear-gradient(90deg, #0369a1, #38bdf8);
    color: white;
    font-weight: 900;
    height: 56px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.18);
    font-size: 18px;
    box-shadow: 0 0 18px rgba(56,189,248,0.35);
}

.stButton button:hover {
    background: linear-gradient(90deg, #38bdf8, #0ea5e9);
    transform: scale(1.01);
}

/* Metric boxes */
[data-testid="stMetric"] {
    background: rgba(15,23,42,0.82);
    border: 1px solid rgba(56,189,248,0.28);
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0 0 18px rgba(56,189,248,0.12);
}

[data-testid="stMetricLabel"] {
    color: #bae6fd;
    font-weight: 700;
}

[data-testid="stMetricValue"] {
    color: #ffffff;
    font-weight: 900;
}

/* Threat levels */
.high {
    color: #ef4444;
    font-size: 32px;
    font-weight: 950;
    text-shadow: 0 0 16px rgba(239,68,68,0.9);
}

.medium {
    color: #f59e0b;
    font-size: 32px;
    font-weight: 950;
    text-shadow: 0 0 14px rgba(245,158,11,0.8);
}

.low {
    color: #22c55e;
    font-size: 32px;
    font-weight: 950;
    text-shadow: 0 0 14px rgba(34,197,94,0.8);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(2, 6, 23, 0.97);
    border-right: 1px solid rgba(56,189,248,0.25);
}

section[data-testid="stSidebar"] * {
    color: #e2e8f0;
}

/* Text area */
textarea {
    background: rgba(15,23,42,0.92) !important;
    color: white !important;
    border-radius: 16px !important;
    border: 1px solid rgba(56,189,248,0.35) !important;
}

/* Inputs */
input {
    background: rgba(15,23,42,0.92) !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid rgba(56,189,248,0.35) !important;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background: rgba(15,23,42,0.92) !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid rgba(56,189,248,0.35) !important;
}

/* Animated safety ticker */
.safety-ticker {
    width: 100%;
    overflow: hidden;
    background: linear-gradient(90deg, rgba(239,68,68,0.18), rgba(245,158,11,0.16));
    border: 1px solid rgba(250,204,21,0.45);
    border-radius: 14px;
    padding: 13px;
    margin-bottom: 25px;
    box-shadow: 0 0 18px rgba(250,204,21,0.15);
}

.ticker-text {
    display: inline-block;
    white-space: nowrap;
    animation: scroll-left 20s linear infinite;
    color: #fde68a;
    font-weight: 900;
    font-size: 17px;
    letter-spacing: 0.4px;
}

@keyframes scroll-left {
    0% { transform: translateX(100%); }
    100% { transform: translateX(-100%); }
}
</style>
""", unsafe_allow_html=True)
def get_cyber_news():

    feeds = [
        "https://feeds.feedburner.com/TheHackersNews",
        "https://www.bleepingcomputer.com/feed/"
    ]

    news_list = []

    try:
        for url in feeds:

            feed = feedparser.parse(url)

            for entry in feed.entries[:4]:
                news_list.append(entry.title)

        return news_list[:8]

    except Exception:
        return [
            "Cyber news unavailable",
            "Check internet connection"
        ]
# ================= TOP SECTION =================

left_col, right_col = st.columns([3, 1])

with left_col:

    st.markdown("""
    <div class='main-title'>
    🔐 Kavach AI
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='sub-title'>
    Advanced Fraud Detection • Email Threat Analysis • URL Reputation Monitoring • Cyber Safety Intelligence
    </div>
    """, unsafe_allow_html=True)

with right_col:

    st.markdown("### 📰 Live Alerts")

    news_list = get_cyber_news()

    if news_list:

        current_news = news_list[
            refresh_count % len(news_list)
        ]

        st.markdown(
            f"""
            <div class="news-box">
            🚨 {current_news}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.warning("News unavailable")

# ================= LIVE CYBER NEWS TICKER =================

# ================= LIVE CYBER NEWS TICKER =================

news_list = get_cyber_news()

if news_list:
    current_news = news_list[refresh_count % len(news_list)]
else:
    current_news = "Cyber news currently unavailable"

st.markdown(
    f"""
    <div class="safety-ticker">
        <div class="ticker-text">
            📰 LIVE CYBER NEWS • {current_news}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ================= MOVING SAFETY TICKER =================

st.markdown("""
<div class="safety-ticker">
    <div class="ticker-text">
        🚨 Cyber Security Alert • Never Share OTP • Never Share PIN • Never Share CVV • Verify Sender Before Payment • Beware of Phishing Emails • Report Fraud at 1930 • Stay Safe Online • Protect Your Digital Identity •
    </div>
</div>
""", unsafe_allow_html=True)
# ================= DAILY TIP =================

tips = [
    "🚨 Never share OTP with anyone.",
    "🔒 Use strong passwords.",
    "⚠️ Verify URLs before clicking.",
    "💳 Never share CVV or PIN.",
    "📞 Call 1930 for financial cyber fraud."
]

st.info(random.choice(tips))
# ================= CYBER ANIMATION =================


# ================= SIDEBAR =================

# ================= SIDEBAR =================

st.sidebar.markdown("## 🛡️ Kavach AI Dashboard")

st.sidebar.markdown("---")

st.sidebar.metric("🤖 Model", "Naive Bayes")
st.sidebar.metric("🧠 NLP Engine", "TF-IDF + Bigrams")
st.sidebar.metric("🎯 Purpose", "Fraud Detection")

st.sidebar.markdown("---")

st.sidebar.markdown("### 🚀 Features")

st.sidebar.success("Spam Detection")
st.sidebar.success("Fraud Risk Score")
st.sidebar.success("URL Reputation Checker")
st.sidebar.success("Scammer Type Detection")
st.sidebar.success("Cyber Crime Reporting")
st.sidebar.success("PDF Security Reports")
st.sidebar.success("AI Safety Assistant")

st.sidebar.markdown("---")

st.sidebar.markdown("### 🚨 Emergency Response")

st.sidebar.error("☎️ Cyber Fraud Helpline: 1930")

st.sidebar.link_button(
    "🛡️ Cyber Crime Portal",
    "https://www.cybercrime.gov.in/Webform/Accept.aspx"
)

st.sidebar.link_button(
    "🏦 RBI Complaint Portal",
    "https://cms.rbi.org.in/"
)

st.sidebar.success(
    "Official Government Complaint Portals"
)

st.sidebar.markdown("---")

st.sidebar.markdown("### 💡 Daily Cyber Tip")

tips = [
    "🚨 Never share OTP with anyone.",
    "🔒 Use strong passwords and 2FA.",
    "⚠️ Verify URLs before clicking.",
    "💳 Never share CVV or PIN.",
    "📞 Call 1930 immediately for fraud."
]

import random
st.sidebar.info(random.choice(tips))

st.sidebar.markdown("---")

st.sidebar.markdown("### 🎙️ Audio Alerts")

import os

if os.path.exists("kavach_hindi.mp3"):
    with open("kavach_hindi.mp3", "rb") as audio:
        st.sidebar.audio(audio.read())

if os.path.exists("kavach_welcome.mp3"):
    with open("kavach_welcome.mp3", "rb") as audio:
        st.sidebar.audio(audio.read())

# ================= MODEL =================

@st.cache_resource
def train_model():
    df = pd.read_csv("email_spam_dataset.csv", encoding="latin-1")
    df = df[["v1", "v2"]].dropna()

    X = df["v2"]
    y = df["v1"].map({"ham": 0, "spam": 1})

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        min_df=2
    )

    X_train_vector = vectorizer.fit_transform(X_train)

    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    )

    model.fit(X_train_vector, y_train)

    return model, vectorizer, df


model, vectorizer, df = train_model()

# ================= FUNCTIONS =================

def detect_links(message):
    return re.findall(r"https?://\S+|www\.\S+", message)


def detect_phone_numbers(message):
    return re.findall(r"\b\d{10}\b", message)


def detect_emails(message):
    return re.findall(r"\S+@\S+", message)


def check_url_reputation(links):
    risky_keywords = [
        "login", "verify", "otp", "bank", "free",
        "claim", "update", "secure", "payment",
        "reward", "kyc", "password"
    ]

    results = []

    for link in links:
        risk_score = 0
        reasons = []
        lower_link = link.lower()

        for word in risky_keywords:
            if word in lower_link:
                risk_score += 15
                reasons.append(f"Contains risky keyword: {word}")

        if lower_link.startswith("http://"):
            risk_score += 20
            reasons.append("Uses insecure HTTP connection")

        if len(link) > 75:
            risk_score += 10
            reasons.append("URL is unusually long")

        risk_score = min(risk_score, 100)

        if risk_score >= 60:
            status = "High Risk"
        elif risk_score >= 30:
            status = "Suspicious"
        else:
            status = "Low Risk"

        results.append({
            "url": link,
            "status": status,
            "risk_score": risk_score,
            "reasons": reasons
        })

    return results


def psychological_analysis(message):
    tactics = []
    msg = message.lower()

    fear_words = [
        "blocked", "suspended", "warning", "risk",
        "danger", "expired", "fraud", "illegal", "suspension"
    ]

    greed_words = [
        "win", "winner", "prize", "reward",
        "cash", "free", "bonus", "lottery"
    ]

    urgency_words = [
        "urgent", "immediately", "now",
        "limited", "today", "hurry", "last chance"
    ]

    authority_words = [
        "bank", "government", "official",
        "verification", "account", "security", "credit card"
    ]

    personal_data_words = [
        "otp", "password", "pin", "login",
        "card", "cvv", "details"
    ]

    payment_words = [
        "fee", "registration", "pay", "payment",
        "deposit", "charges"
    ]

    if any(word in msg for word in payment_words):
        tactics.append("Payment Scam Attempt")

    if any(word in msg for word in fear_words):
        tactics.append("Fear Manipulation")

    if any(word in msg for word in greed_words):
        tactics.append("Reward Bait")

    if any(word in msg for word in urgency_words):
        tactics.append("Urgency Pressure")

    if any(word in msg for word in authority_words):
        tactics.append("Fake Authority")

    if any(word in msg for word in personal_data_words):
        tactics.append("Personal Data Theft Attempt")

    return tactics


def detect_scam_persona(message):
    msg = message.lower()

    if any(word in msg for word in [
        "otp", "bank", "account", "verify",
        "password", "login", "card", "cvv", "pin"
    ]):
        return "Bank Fraudster"

    elif any(word in msg for word in [
        "win", "winner", "lottery", "reward",
        "cash", "prize", "bonus"
    ]):
        return "Lottery Scam Bot"

    elif any(word in msg for word in [
        "job", "hiring", "salary",
        "interview", "resume", "vacancy"
    ]):
        return "Fake Job Recruiter"

    elif any(word in msg for word in [
        "bitcoin", "crypto",
        "investment", "trading", "profit"
    ]):
        return "Crypto Scam Promoter"

    elif any(word in msg for word in [
        "delivery", "parcel",
        "tracking", "shipment", "courier"
    ]):
        return "Fake Delivery Agent"

    elif any(word in msg for word in [
        "loan", "emi", "credit", "insurance"
    ]):
        return "Financial Scam Caller"

    return "Unknown / General Spam"


def analyze_message(message):
    suspicious_words = [
        "free", "win", "winner", "cash", "prize", "urgent",
        "click", "offer", "limited", "verify", "account",
        "password", "lottery", "discount", "claim",
        "congratulations", "bank", "otp", "login",
        "reward", "bonus", "blocked", "suspended",
        "crypto", "investment", "parcel", "delivery",
        "cvv", "pin", "card", "suspension",
        "fee", "registration", "pay", "payment",
        "selected", "work from home"
    ]

    message_vector = vectorizer.transform([message])
    ml_prediction = model.predict(message_vector)[0]
    probability = model.predict_proba(message_vector)[0]

    spam_risk = probability[1] * 100
    msg_lower = message.lower()

    found_words = [word for word in suspicious_words if word in msg_lower]
    links = detect_links(message)
    url_reputation = check_url_reputation(links)
    phone_numbers = detect_phone_numbers(message)
    emails = detect_emails(message)
    tactics = psychological_analysis(message)
    persona = detect_scam_persona(message)

    final_score = spam_risk
    final_score += len(found_words) * 5
    final_score += len(tactics) * 10

    if links:
        final_score += 20

    if phone_numbers:
        final_score += 10

    if emails:
        final_score += 10

    if persona != "Unknown / General Spam":
        final_score += 20

    final_score = min(final_score, 100)

    prediction = "Spam" if ml_prediction == 1 or final_score >= 40 else "Ham / Not Spam"

    if final_score >= 70 or persona == "Fake Job Recruiter" or "Payment Scam Attempt" in tactics:
        threat = "High"
    elif final_score >= 40:
        threat = "Medium"
    else:
        threat = "Low"

    return {
        "prediction": prediction,
        "ml_probability": round(spam_risk, 2),
        "fraud_score": round(final_score, 2),
        "threat": threat,
        "persona": persona,
        "tactics": tactics,
        "words": found_words,
        "links": links,
        "phones": phone_numbers,
        "emails": emails,
        "url_reputation": url_reputation
    }


def generate_pdf_report(result, message):
    pdf_file = "security_report.pdf"

    doc = SimpleDocTemplate(pdf_file)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("AI Fraud Threat Analysis Report", styles["Title"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"<b>Message:</b> {message}", styles["BodyText"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"<b>Prediction:</b> {result['prediction']}", styles["BodyText"]))
    content.append(Paragraph(f"<b>Threat Level:</b> {result['threat']}", styles["BodyText"]))
    content.append(Paragraph(f"<b>ML Spam Probability:</b> {result['ml_probability']}%", styles["BodyText"]))
    content.append(Paragraph(f"<b>Final Fraud Score:</b> {result['fraud_score']}%", styles["BodyText"]))
    content.append(Paragraph(f"<b>Scammer Type:</b> {result['persona']}", styles["BodyText"]))

    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>Psychological Tactics:</b>", styles["Heading3"]))

    if result["tactics"]:
        for tactic in result["tactics"]:
            content.append(Paragraph(f"- {tactic}", styles["BodyText"]))
    else:
        content.append(Paragraph("None", styles["BodyText"]))

    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>Suspicious Words:</b>", styles["Heading3"]))
    content.append(Paragraph(", ".join(result["words"]) if result["words"] else "None", styles["BodyText"]))

    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>Links Found:</b>", styles["Heading3"]))
    content.append(Paragraph(", ".join(result["links"]) if result["links"] else "None", styles["BodyText"]))

    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>URL Reputation:</b>", styles["Heading3"]))

    if result["url_reputation"]:
        for url_info in result["url_reputation"]:
            content.append(Paragraph(f"URL: {url_info['url']}", styles["BodyText"]))
            content.append(Paragraph(f"Status: {url_info['status']}", styles["BodyText"]))
            content.append(Paragraph(f"Risk Score: {url_info['risk_score']}%", styles["BodyText"]))
    else:
        content.append(Paragraph("No URL found.", styles["BodyText"]))

    content.append(Spacer(1, 10))

    content.append(Paragraph(
        "Safety Advice: Never share OTP, PIN, CVV, passwords, or bank details.",
        styles["BodyText"]
    ))

    doc.build(content)

    return pdf_file
def cyber_ai_chat(user_question):
    try:
        prompt = f"""
        You are CyberGuard AI.

        Answer questions related to:
        - Cyber Security
        - Fraud Prevention
        - Spam Detection
        - Scam Awareness
        - Banking Fraud
        - UPI Fraud
        - OTP Scams
        - Phishing
        - Cyber Crime Reporting
        - Government Cyber Safety Websites

        User Question:
        {user_question}
        """

        response = gemini_model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"AI chatbot error: {e}"
# ================= UI =================

message = st.text_area(
    "📩 Paste your SMS / Email / WhatsApp message",
    height=170,
    placeholder="Example: Verify your account now at http://fake-bank-login.com/verify"
)

analyze_btn = st.button("🔍 Analyze Threat", use_container_width=True)

if analyze_btn:
    if message.strip() == "":
        st.warning("Please enter a message first.")

    else:
        result = analyze_message(message)

        col1, col2, col3 = st.columns(3)

        col1.metric("Prediction", result["prediction"])
        col2.metric("ML Spam Probability", f"{result['ml_probability']}%")
        col3.metric("Final Fraud Score", f"{result['fraud_score']}%")

        st.progress(int(result["fraud_score"]))

        if result["threat"] == "High":
            st.markdown("<p class='high'>🚨 Threat Level: HIGH</p>", unsafe_allow_html=True)
        elif result["threat"] == "Medium":
            st.markdown("<p class='medium'>⚠️ Threat Level: MEDIUM</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p class='low'>✅ Threat Level: LOW</p>", unsafe_allow_html=True)

        left, right = st.columns(2)

        with left:
            st.subheader("👤 Scammer Type")
            st.info(result["persona"])

            st.subheader("🧠 Scam Psychology")

            if result["tactics"]:
                for tactic in result["tactics"]:
                    st.write("•", tactic)
            else:
                st.success("No manipulation tactics found.")

            st.subheader("🔎 Suspicious Indicators")
            st.write("**Words:**", result["words"] if result["words"] else "None")
            st.write("**Links:**", result["links"] if result["links"] else "None")
            st.write("**Phones:**", result["phones"] if result["phones"] else "None")
            st.write("**Emails:**", result["emails"] if result["emails"] else "None")

            st.subheader("🌐 URL Reputation Checker")

            if result["url_reputation"]:
                for url_info in result["url_reputation"]:
                    st.write("**URL:**", url_info["url"])
                    st.write("**Status:**", url_info["status"])
                    st.write("**Risk Score:**", f"{url_info['risk_score']}%")

                    if url_info["reasons"]:
                        st.write("**Reasons:**")
                        for reason in url_info["reasons"]:
                            st.write("-", reason)

                    st.divider()
            else:
                st.success("No URL found in this message.")

        with right:
            st.subheader("📊 Message Risk Chart")

            fig, ax = plt.subplots(figsize=(4, 4))
            ax.pie(
                [100 - result["fraud_score"], result["fraud_score"]],
                labels=["Safe", "Fraud Risk"],
                autopct="%1.1f%%",
                startangle=90
            )

            ax.set_title("Message Risk Analysis")
            st.pyplot(fig)

        st.subheader("🛡️ Safety Advice")

        if result["threat"] == "High":
            st.error("High risk. Do not click links or share OTP, PIN, CVV, passwords, or bank details.")

            st.subheader("🚨 Report Cyber Crime")

            st.write(
                "This message looks highly suspicious. "
                "You can report cyber fraud on the official National Cyber Crime Reporting Portal."
            )

            st.link_button(
                "🚨 Report on Cyber Crime Portal",
                "https://www.cybercrime.gov.in/"
            )

            st.info("For financial cyber fraud in India, call helpline number 1930 immediately.")

        elif result["threat"] == "Medium":
            st.warning("Be careful. Verify the sender before replying or sharing details.")

            st.subheader("⚠️ Need to Report?")

            st.write(
                "If money loss, OTP sharing, fake job payment, or bank fraud happened, "
                "report it on the official portal."
            )

            st.info("For financial fraud, call 1930.")

        else:
            st.success("Message looks mostly safe.")

        pdf_file = generate_pdf_report(result, message)

        with open(pdf_file, "rb") as file:
            st.download_button(
                label="📄 Download Security Report",
                data=file,
                file_name="AI_Fraud_Report.pdf",
                mime="application/pdf"
            )

# ================= CYBER SAFETY VIDEO =================

st.markdown("---")
st.subheader("🎥 Cyber Safety Awareness Center")

st.write("Learn about common cyber frauds and online safety.")

col1, col2, col3 = st.columns(3)

with col1:
    st.link_button(
        "🎣 Phishing Awareness",
        "https://www.youtube.com/results?search_query=phishing+awareness"
    )

with col2:
    st.link_button(
        "🔐 OTP Scam Prevention",
        "https://www.youtube.com/results?search_query=otp+fraud+awareness"
    )

with col3:
    st.link_button(
        "💳 UPI Fraud Safety",
        "https://www.youtube.com/results?search_query=upi+fraud+awareness"
    )

# ================= AI CHATBOT =================

st.markdown("---")
st.subheader("🤖 Kavach AI Assistant")

question = st.text_input(
    "Ask anything about fraud, spam, scams, cyber safety, phishing, UPI fraud, banking fraud, government portals..."
)

if st.button("Ask AI"):
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("🔍 Kavach AI is analyzing..."):
            answer = cyber_ai_chat(question)

        st.success(answer)