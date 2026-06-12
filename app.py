import pandas as pd
import matplotlib.pyplot as plt
import re

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
from sklearn.naive_bayes import MultinomialNB
# ================= LOAD DATASET =================

df = pd.read_csv("email_spam_dataset.csv", encoding="latin-1")
df = df[["v1", "v2"]].dropna()

# ================= HAM VS SPAM PIE CHART =================

label_counts = df["v1"].value_counts()

plt.figure(figsize=(6, 6))
plt.pie(
    label_counts,
    labels=label_counts.index,
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Ham vs Spam Message Distribution")
plt.savefig("ham_spam_pie_chart.png")
plt.close()

print("Pie chart saved as ham_spam_pie_chart.png")
print("Ham count:", label_counts["ham"])
print("Spam count:", label_counts["spam"])

# ================= FEATURES AND LABELS =================

X = df["v2"]
y = df["v1"].map({"ham": 0, "spam": 1})

# ================= SPLIT DATA =================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ================= TF-IDF WITH BIGRAMS =================

vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
    min_df=2
)

X_train_vector = vectorizer.fit_transform(X_train)
X_test_vector = vectorizer.transform(X_test)

# ================= MODEL TRAINING =================

model = MultinomialNB()

model.fit(X_train_vector, y_train)
# ================= MODEL EVALUATION =================

y_pred = model.predict(X_test_vector)

print("\n===== MODEL PERFORMANCE =====")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["Ham", "Spam"]))

# ================= CONFUSION MATRIX =================

cm = confusion_matrix(y_test, y_pred)

display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["Ham", "Spam"]
)

display.plot()
plt.title("Confusion Matrix - AI Fraud Persona & Email Threat Analyzer")
plt.savefig("confusion_matrix.png")
plt.close()

print("Confusion matrix saved as confusion_matrix.png")

# ================= BASIC DETECTION FEATURES =================

def detect_links(message):
    return re.findall(r"https?://\S+|www\.\S+", message)

def detect_phone_numbers(message):
    return re.findall(r"\b\d{10}\b", message)

def detect_emails(message):
    return re.findall(r"\S+@\S+", message)

# ================= SCAM PSYCHOLOGY ANALYZER =================

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

# ================= FRAUD PERSONA DETECTION =================

def detect_scam_persona(message):
    msg = message.lower()

    if any(word in msg for word in [
        "otp", "bank", "account", "verify",
        "password", "login", "card", "cvv", "pin"
    ]):
        return "Bank Fraudster"

    elif any(word in msg for word in [
        "win", "winner", "lottery",
        "reward", "cash", "prize", "bonus"
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

# ================= MAIN ANALYSIS FUNCTION =================
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
            "risk_score": risk_score,
            "status": status,
            "reasons": reasons
        })

    return results
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
    person = detect_scam_persona(message)

    final_score = spam_risk
    final_score += len(found_words) * 5
    final_score += len(tactics) * 10

    if links:
        final_score += 20

    if phone_numbers:
        final_score += 10

    if emails:
        final_score += 10

    if person != "Unknown / General Spam":
        final_score += 20

    final_score = min(final_score, 100)

    # ================= MESSAGE RISK PIE CHART =================

    safe_score = 100 - final_score

    plt.figure(figsize=(6, 6))
    plt.pie(
        [safe_score, final_score],
        labels=["Safe", "Fraud Risk"],
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title("Message Fraud Risk Analysis")
    plt.savefig("message_risk_pie_chart.png")
    plt.close()

    print("Message risk pie chart saved as message_risk_pie_chart.png")

    if ml_prediction == 1 or final_score >= 40:
        final_prediction = "Spam"
    else:
        final_prediction = "Ham / Not Spam"

    if (
        final_score >= 70
        or person == "Fake Job Recruiter"
        or "Payment Scam Attempt" in tactics
    ):
        threat_level = "High"
    elif final_score >= 40:
        threat_level = "Medium"
    else:
        threat_level = "Low"
        return {
    "prediction": final_prediction,
    "ml_probability": round(spam_risk, 2),
    "fraud_score": round(final_score, 2),
    "threat": threat_level,
    "persona": person,
    "tactics": tactics,
    "words": found_words,
    "links": links,
    "phones": phone_numbers,
    "emails": emails,
    "url_reputation": url_reputation
}

    print("\n===== AI FRAUD PERSON & EMAIL THREAT ANALYSIS =====")
    print("Message:", message)
    print("Prediction:", final_prediction)
    print("ML Spam Probability:", round(spam_risk, 2), "%")
    print("Final Fraud Risk Score:", round(final_score, 2), "%")
    print("Threat Level:", threat_level)

    print("Suspicious Words:", found_words if found_words else "None")
    print("Links Found:", links if links else "None")
    print("Phone Numbers Found:", phone_numbers if phone_numbers else "None")
    print("Email Addresses Found:", emails if emails else "None")
    print("Psychological Tactics Detected:", tactics if tactics else "None")
    print("Possible Scammer Type:", person)

    if threat_level == "High":
        print("Safety Advice: High risk. Do not click links or share OTP, PIN, CVV, password, or bank details.")
    elif threat_level == "Medium":
        print("Safety Advice: Be careful. Verify sender before replying or sharing details.")
    else:
        print("Safety Advice: Message looks mostly safe.")

# ================= USER INPUT =================

user_message = input("\nEnter email/message to analyze: ")
analyze_message(user_message)