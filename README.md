# 🛡️ Kavach AI — Cyber Fraud & Spam Detection Platform

Kavach AI is an AI-powered cyber-safety web application that helps users detect suspicious SMS, emails, WhatsApp messages, and phishing links.

It classifies messages as **Spam** or **Ham (safe message)**, calculates a fraud-risk score, identifies suspicious indicators, and provides cyber-safety guidance.

## 🚀 Live Demo

**Deployed App: https://kavach-ai-cyber-fraud-analyzer-gf9tbe7ij3bgmbww3tmrme.streamlit.app/

## 📌 Problem Statement

Cyber fraud messages are increasing rapidly. Users often receive fake bank, KYC, OTP, lottery, job, delivery, UPI, and phishing messages.

Many users cannot easily identify whether a message is genuine or fraudulent. Kavach AI helps users analyze suspicious messages before clicking links, sharing OTPs, or making payments.

## 🎯 Project Objective

The objective of Kavach AI is to:

* Detect spam and suspicious messages using Machine Learning.
* Identify phishing and fraud-related keywords.
* Extract suspicious URLs, phone numbers, and email addresses.
* Calculate a fraud-risk score and threat level.
* Provide safety advice and official cybercrime reporting guidance.
* Improve cyber-security awareness among users.

## ✨ Features

* 📩 Spam or Ham message classification
* 🧠 Multinomial Naive Bayes machine-learning model
* 🔢 TF-IDF text vectorization
* 📊 Fraud-risk score and threat level
* 🔗 Suspicious URL detection
* 📞 Phone number and email extraction
* 🚨 Scam psychology detection such as urgency, fear, greed, and fake authority
* 👤 Possible scammer persona detection
* 📈 Fraud-risk pie chart
* 📄 Downloadable PDF security report
* 📰 Live cyber-security news alerts
* 🔊 Hindi and English cyber-awareness audio
* 🤖 AI cyber-safety chatbot
* 🇮🇳 Cybercrime reporting guidance for Indian users

## 🧠 Machine Learning Model

The main machine-learning algorithm used in this project is:

### Multinomial Naive Bayes

Multinomial Naive Bayes is used for text classification. It is suitable for spam detection because it works efficiently with word-frequency and TF-IDF features.

The model predicts whether a message is:

* **Ham** — genuine or normal message
* **Spam** — unwanted, suspicious, or fraudulent message

## ⚙️ Working Flow

```text
User enters SMS / Email / WhatsApp message
                ↓
Text preprocessing
                ↓
TF-IDF Vectorization
                ↓
Multinomial Naive Bayes Prediction
                ↓
Spam / Ham Classification
                ↓
Fraud Score Calculation
                ↓
Threat Level Detection
                ↓
URL, Phone, Email and Keyword Analysis
                ↓
Safety Advice and PDF Report
```

## 🛠️ Technologies Used

| Technology                | Purpose                                        |
| ------------------------- | ---------------------------------------------- |
| Python                    | Main programming language                      |
| Streamlit                 | Web application interface                      |
| Pandas                    | Dataset loading and preprocessing              |
| Scikit-learn              | Machine-learning model training and evaluation |
| TF-IDF Vectorizer         | Converts text into numerical features          |
| Multinomial Naive Bayes   | Spam and ham classification                    |
| Matplotlib                | Fraud-risk chart visualization                 |
| ReportLab                 | PDF report generation                          |
| Feedparser                | Live cyber-security RSS news                   |
| gTTS                      | Hindi and English awareness audio              |
| Gemini API                | AI cyber-safety chatbot                        |
| GitHub                    | Version control and source code hosting        |
| Streamlit Community Cloud | Project deployment                             |

## 📂 Project Structure

```text
Kavach-AI-Cyber-Fraud-Analyzer/
│
├── frontend.py
├── app.py
├── email_spam_dataset.csv
├── requirements.txt
├── .gitignore
├── README.md
├── create_audio.py
├── create_hindi_audio.py
├── confusion_matrix.png
├── ham_spam_pie_chart.png
├── message_risk_pie_chart.png
└── security_report.pdf
```

## 📊 Dataset

The project uses an email/SMS spam dataset containing messages labelled as:

| Label | Meaning                        |
| ----- | ------------------------------ |
| Ham   | Genuine or safe message        |
| Spam  | Suspicious or unwanted message |

Example:

```text
Ham: Are we meeting at 5 PM today?

Spam: Congratulations! You won ₹50,000. Click this link now.
```

## 🔍 Fraud Indicators Checked

Kavach AI checks for suspicious indicators such as:

* OTP-related words
* PIN and CVV-related words
* Urgency words such as “urgent”, “immediately”, and “act now”
* Fake bank or KYC messages
* Lottery and reward scams
* Fake job offers
* Investment scams
* Suspicious URLs
* Phone numbers
* Email addresses
* Fear and pressure tactics

## 🚨 Threat Levels

| Threat Level | Meaning                                   |
| ------------ | ----------------------------------------- |
| Low          | Message looks mostly safe                 |
| Medium       | User should verify the sender and details |
| High         | Possible phishing, spam, or fraud attempt |

## 📄 PDF Security Report

After analysis, the user can download a PDF report containing:

* Original message
* Spam or Ham prediction
* Fraud score
* Threat level
* Suspicious keywords
* URLs, phone numbers, and emails found
* Scam persona
* Scam psychology tactics
* Cyber-safety advice

## 🇮🇳 Cybercrime Reporting Support

For high-risk messages, Kavach AI provides cybercrime reporting guidance.

* National Cyber Crime Reporting Portal: https://www.cybercrime.gov.in/
* Financial Cyber Fraud Helpline: **1930**

## 💻 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Harshgithub321/Kavach-AI-Cyber-Fraud-Analyzer.git
```

### 2. Open the project folder

```bash
cd Kavach-AI-Cyber-Fraud-Analyzer
```

### 3. Install required libraries

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

Create a file named `.env` in the project folder:

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

Do not upload the `.env` file to GitHub.

### 5. Run the application

```bash
streamlit run frontend.py
```

The application will open in your browser at:

```text
http://localhost:8501
```

## 🔐 API Key Security

API keys are stored using environment variables or Streamlit Secrets.

The `.env` file is added to `.gitignore` so secret keys are not uploaded to GitHub.

Example:

```text
GEMINI_API_KEY=your_secret_key
```

## ⚠️ Limitations

* The prediction depends on the quality of the training dataset.
* New fraud patterns may not always be detected.
* The URL checker is rule-based and does not replace a full malware scanner.
* The Gemini chatbot can face free API quota limits.
* The application is an awareness and decision-support tool, not a replacement for cybercrime investigation.

## 🔮 Future Improvements

* Add Hindi and Hinglish spam-message detection.
* Add more Indian regional languages.
* Integrate Google Safe Browsing API.
* Integrate VirusTotal API for stronger URL analysis.
* Add screenshot-based phishing website detection.
* Add user login and message history.
* Store reports in a database.
* Add WhatsApp and SMS integration.
* Add real-time cyber-fraud notifications.
* Train the model using a larger Indian fraud-message dataset.

## 👨‍💻 Author

**Harsh Srivastava**

GitHub: https://github.com/Harshgithub321

## 📜 License

This project is created for educational and cyber-security awareness purposes.
