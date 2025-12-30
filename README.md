# ClipTrans - AI-Powered Clipboard Translation Assistant

<div align="center">

![Version](https://img.shields.io/badge/version-1.20-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Mac-lightgrey.svg)
![License](https://img.shields.io/badge/license-Custom-orange.svg)

**Instant translation, dictionary lookup, and pronunciation - all with a single hotkey**

[Features](#-features) | [Quick Start](#-quick-start) | [Usage](#-usage) | [AI Tutor Mode](#-ai-tutor-mode) | [Settings](#%EF%B8%8F-settings)

</div>

---

## Multilingual UI Support

ClipTrans now supports **9 languages** for the user interface:

| Language | Code |
|----------|------|
| English | EN |
| Japanese (日本語) | JA |
| Chinese (中文) | ZH |
| Korean (한국어) | KO |
| Spanish (Espanol) | ES |
| French (Francais) | FR |
| German (Deutsch) | DE |
| Portuguese (Portugues) | PT-BR |
| Russian (Русский) | RU |

All menus, dialogs, status messages, and default prompts automatically switch to your selected language.

---

## Common Challenges

- Reading **English documents or papers** and constantly switching to translation sites for unknown words...
- Using **foreign software or games** and tediously copy-pasting for translations...
- **Studying languages** and wanting to know not just meanings but also etymology and usage...
- Wanting to **check pronunciation** but opening another site is too much hassle...

### ClipTrans solves all of these!

Select text, press `Ctrl+C` to copy, then hit the hotkey. **Translation in just 2 seconds**.

---

## Features

### Instant Translation
- **One hotkey** for immediate translation (default: `Ctrl+Alt+D`)
- **High-accuracy translation** powered by DeepL API
- **Seamless clipboard replacement** - Translation results automatically replace clipboard content, ready to paste immediately with `Ctrl+V`
- **Works in the background** - No need to switch to ClipTrans window. Hotkeys work system-wide from any application

> **What makes ClipTrans different?**
> Unlike browser-based translators that require switching windows and manual copy-paste, ClipTrans runs quietly in the background and responds to global hotkeys. While you're working in Word, browsing the web, or playing a game - just copy text and press the hotkey. Your clipboard is instantly replaced with the translation, ready to paste. No window switching, no extra steps.

### AI Dictionary
- **Detailed word explanations** powered by Claude AI
- **Memorable learning** through etymology, prefix, and suffix breakdown
- Learn synonyms and antonyms together

### Text-to-Speech
- **One-touch pronunciation** check with native speakers
- Perfect for language learning and listening practice

### AI Tutor Mode
- Your personal **AI learning partner**
- **Personalized guidance** based on your learning history
- **High-precision context understanding** using BM25 algorithm

### Learning History Management
- **Automatic saving** of all translation history
- **Instant review** of past learning through keyword search

---

## Quick Start

### Requirements
- Python 3.8 or higher
- DeepL API key (free plan available)
- Claude API key (for AI Tutor mode)

### Installation

```bash
# Clone the repository
git clone https://github.com/unhaya/ClipboardTranslator.git
cd ClipboardTranslator

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

### Initial Setup
1. Open settings after launching the app
2. Enter your DeepL API key
3. (Optional) Enter your Claude API key
4. Save settings and you're done!

---

## Usage

### Basic Operations

| Function | Hotkey | Description |
|----------|--------|-------------|
| Translate | `Ctrl+Alt+D` | Translate clipboard text |
| Dictionary | `Ctrl+Alt+J` | Show detailed word explanation |
| Speech | `Ctrl+Alt+T` | Read text aloud |

### Workflow

```
1. Select text you want to translate
2. Press Ctrl+C to copy
3. Press Ctrl+Alt+D to translate!
   -> Results appear in the window
   -> Translation is automatically copied to clipboard
4. Press Ctrl+V to paste the translation anywhere!
```

**The key advantage**: Your clipboard now contains the translated text, not the original. You can immediately paste it into any application - chat, documents, emails - without any extra steps.

### Dictionary Example

Looking up "alleviate":

```
[Meaning]
To reduce or relieve (pain, problems, etc.)

[Etymology Breakdown]
al- (intensifier) + levi- (light) + -ate (verb suffix)
-> "to make lighter" = to alleviate

[Synonyms]
relieve, ease, mitigate

[Antonyms]
aggravate, worsen
```

---

## AI Tutor Mode

### Your Personal AI Learning Partner

AI Tutor mode is not just an AI chatbot. It's a **dedicated tutor that remembers your learning history** and provides guidance based on what you've learned before.

### Features

- **Learning History Utilization**: Remembers words you've translated and looked up
- **Personalization**: Provides advice based on your weak points
- **High-Precision Search**: Auto-detects related history using BM25 + morphological analysis
- **Temporal Weighting**: Prioritizes recently learned content

### How AI Tutor Remembers Your History

AI Tutor uses a **two-layer memory system**:

| Layer | Purpose | Storage |
|-------|---------|---------|
| **Conversation History** | Recent chat context | In-memory (configurable) |
| **Translation Database** | All past lookups | SQLite (permanent) |

**BM25 Search Algorithm:**
- When you ask a question, the tutor searches your entire translation history using BM25
- BM25 ranks results by relevance (word frequency, document frequency, text length)
- Recent entries are weighted higher (exponential decay over 30 days)
- Japanese text is analyzed with morphological analysis (Janome) for accurate matching

This means even if your conversation history is short, the tutor can recall any word you've ever looked up.

### Example

```
You: "Do you remember 'alleviate' that I looked up before?"

AI Tutor: "Of course I remember! That's the word you looked up on 12/27.
al- (intensifier) + levi- (light) + -ate (verb suffix) = 'to alleviate', right?
It's effective to memorize it together with the synonym 'relieve'!"
```

### Available Models

| Model | Characteristics | Recommended For |
|-------|----------------|-----------------|
| Claude Sonnet 4.5 | Balanced | Daily use |
| Claude Haiku 4.5 | Fast, Low cost | Quick queries |
| Claude Opus 4.5 | Highest performance | Deep learning |

---

## Settings

### Configuration Options

| Category | Item | Description |
|----------|------|-------------|
| Translation | DeepL Enable/Disable | Use DeepL API |
| Translation | Character Limit | Max characters for translation |
| API | DeepL API Key | DeepL authentication key |
| API | Claude API Key | Claude AI authentication key |
| Speech | Speech Enable/Disable | Use TTS feature |
| Speech | Volume | Playback volume (0.0-1.0) |
| Tutor | Model Selection | Claude model to use |
| Tutor | History Retention | Number of conversation history to reference |
| Shortcuts | Hotkeys for each function | Customizable |

### Config File Location

- Windows: `%APPDATA%\ClipboardTranslator\config.ini`

---

## Technical Specifications

### Architecture

```
ClipTrans/
├── main.py                 # Entry point
├── config/                 # Configuration management
├── core/                   # Core features
│   ├── translation.py      # DeepL/Claude translation
│   ├── dictionary.py       # Dictionary feature
│   ├── text_to_speech.py   # Text-to-speech
│   ├── history.py          # History management
│   └── tutor/              # AI Tutor mode
│       ├── chat_handler.py # Chat processing
│       └── search.py       # BM25 search
├── ui/                     # User interface
│   ├── main_window.py      # Main window
│   ├── settings_dialog.py  # Settings screen
│   └── history_dialog.py   # History screen
└── data/                   # Data storage
    └── dictionary.db       # SQLite database
```

### Technologies Used

- **GUI**: tkinter
- **Translation API**: DeepL API
- **AI**: Claude API (Anthropic)
- **Text-to-Speech**: pygame + gTTS
- **Database**: SQLite
- **Search**: BM25 algorithm + morphological analysis

---

## Requirements

### Required
- Python 3.8 or higher
- Internet connection

### Dependencies

```
requests
pynput
pyperclip
pygame
googletrans==4.0.0-rc1
```

### Optional (Recommended)

```
janome  # Improves morphological analysis accuracy
```

---

## Contributing

Bug reports and feature requests are welcome on [Issues](https://github.com/unhaya/ClipboardTranslator/issues).

---

## License

**Copyright (c) 2025 unhaya. All rights reserved.**

This software is open source but copyright is not waived.

| Usage | Permission |
|-------|------------|
| Personal use | Allowed freely |
| Educational use | Allowed freely |
| Modification/Fork | Allowed (maintain copyright notice) |
| Commercial use | Contact required |

For commercial use, please contact us via [Issues](https://github.com/unhaya/ClipboardTranslator/issues).

---

## Acknowledgments

- [DeepL](https://www.deepl.com/) - High-accuracy translation API
- [Anthropic](https://www.anthropic.com/) - Claude AI

---

<div align="center">

**If this project helped you, please give it a Star!**

Made with love for language learners

</div>
