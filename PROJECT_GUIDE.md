# Friday AI - Core Project Guide

**Friday AI** is a private, 100% offline voice assistant. It runs entirely on your local machine, providing secure and private natural language interaction without needing a web interface or cloud connection.

---

## 🚀 Quick Start

### Running Friday
To start the voice assistant, run:
```powershell
python main.py
```

**How it works:**
1.  **Wait**: Say the wake word: **"Friday"**.
2.  **Listen**: Wait for the "Yes?" acknowledgement.
3.  **Speak**: State your command or question.
4.  **Process**: Friday processes locally using Ollama and Whisper.
5.  **Respond**: Friday speaks the answer back to you.

---

## 📋 Features

### 🧠 Private Intelligence Stack
- **Brain**: Ollama (Llama 3 / Mistral running locally)
- **Ears**: OpenAI Whisper (offline speech-to-text)
- **Mouth**: pyttsx3 (offline text-to-speech)
- **NLP**: spaCy for intent classification and routing

### 💬 Voice Commands
- **Greeting**: "Hello", "Hi", "Hey"
- **Time/Date**: "What time is it?", "What's the date?"
- **Weather**: "What's the weather?" (Requires OpenWeatherMap API key)
- **Identity**: "Who are you?"
- **General Queries**: Any complex question is handled by your local LLM (llama3).

---

## ⚙️ Installation & Setup

### Prerequisites
1.  **Python 3.8+**
2.  **Ollama**: Download from [ollama.com](https://ollama.com)

### Setup
1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Ollama Setup (Crucial)**:
    - **Step A**: Download/Install Ollama from [ollama.com](https://ollama.com).
    - **Step B**: Run the Ollama app (you'll see a tray icon).
    - **Step C**: Open a terminal and run: `ollama pull llama3`.
    - **Note**: If `ollama` is not recognized, restart your computer or add Ollama to your Path.

3.  **Download AI Model**:
    ```bash
    ollama pull llama3
    ```

---

## 🛠️ Configuration
Configure Friday via `.env` or `config.py`.

**Example `.env`:**
```bash
WAKE_WORD=friday
LLM_MODEL=llama3
SPEECH_ENGINE=whisper
TTS_ENGINE=pyttsx3
```

---

## 🔐 Privacy Guarantee
- ✅ **No Internet Required**: Works fully offline.
- ✅ **No Data Collection**: Your voice and thoughts never leave your machine.
- ✅ **Open Source**: Full visibility into the code.

---

**Friday AI: Intelligence in your control.**
