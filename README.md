# ClipTrans - Multilingual Input Assistant for Real-Time Communication

<div align="center">

![Version](https://img.shields.io/badge/version-1.20-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Mac-lightgrey.svg)
![License](https://img.shields.io/badge/license-Custom-orange.svg)

**Type in your language. Send in theirs. Instantly.**

*The world's simplest input-focused translation tool — designed for real-time communication.*

ClipTrans introduces a new category: **input-focused translation for real-time communication.**
It is not designed for reading translations, but for sending messages instantly.

[Why ClipTrans?](#why-cliptrans) | [Key Features](#key-features) | [Quick Start](#quick-start) | [AI Tutor Mode](#ai-tutor-mode) | [Settings](#settings)

</div>

---

## Why ClipTrans?

Most translation apps are designed for **reading** translated text.

ClipTrans is designed for something different:

**Sending messages to people who speak another language - without changing how you type.**

Whether you are chatting on Slack, Discord, Teams, in online games, or on social platforms,
ClipTrans turns translation into an **input operation**, not an output destination.

| Traditional Translation Apps | ClipTrans |
|------------------------------|-----------|
| Read translated text | Type in your native language |
| Copy & paste manually | Press a hotkey |
| Switch windows | Paste and send immediately |
| Break conversation flow | Stay in the conversation |

**Translation is not the goal. Communication is.**

---

## Designed for Real-Time Conversations

ClipTrans is optimized for situations where speed matters:

- Chatting with overseas teammates
- Responding to international customers
- Talking with players in global game servers
- Participating in foreign-language communities

The translated text is automatically placed in your clipboard, ready to paste and send instantly.

- No extra windows.
- No thinking in a foreign language.
- No disruption to your workflow.

---

## Supported Languages

ClipTrans supports multilingual input and UI localization, enabling conversations across regions.

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

You can type in any supported language and communicate instantly with users of another.

---

## Key Features

### Multilingual Input Translation

- **One hotkey** to translate your input text (default: `Ctrl+Alt+D`)
- Translation optimized for **sending**, not reading
- **Clipboard is automatically replaced** with translated text
- Paste and send immediately in any app

### Background Operation

- Works **system-wide** with global hotkeys
- No need to switch windows
- **Visual confirmation** near the cursor when translation completes
- **Smart caching** - Previously translated text is retrieved instantly without API calls

### AI Dictionary & Learning Support

- **Context-aware word explanations** powered by Claude AI
- Etymology, prefixes, suffixes, synonyms, and antonyms
- Designed to improve future input quality

### Text-to-Speech

- **One-touch pronunciation** check with native speakers
- Perfect for language learning and listening practice

### AI Tutor Mode (Optional)

- **Personalized learning assistant**
- Remembers your past translations
- Uses **BM25 + recency weighting** to recall relevant history
- Helps you communicate better over time, not just translate

---

## Philosophy

ClipTrans was created from environments where there was no time to "use a translation app."
It is built for real-time communication, where sending a response matters more than reading one.

ClipTrans treats translation as an **invisible infrastructure**, not a destination.

You should not need to:
- Think about grammar while chatting
- Switch tools mid-conversation
- Copy text back and forth

You should only need to:

**Type -> Translate -> Paste -> Send**

That is the core design principle of ClipTrans.

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
| Font Size | `Ctrl+Wheel` | Adjust text size in the window |

### Workflow

```
1. Type your message in your native language
2. Select the text and press Ctrl+C
3. Press Ctrl+Alt+D to translate!
   -> Translation is automatically copied to clipboard
4. Press Ctrl+V to paste and send!
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
