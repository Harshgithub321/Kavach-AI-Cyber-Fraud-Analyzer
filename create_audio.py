from gtts import gTTS

text = """
Welcome to Kavach AI.
Your intelligent cyber safety assistant.
Stay alert. Stay secure.
"""

tts = gTTS(text=text, lang="en")
tts.save("kavach_welcome.mp3")

print("Audio Created Successfully")