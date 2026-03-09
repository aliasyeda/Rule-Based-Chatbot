# 🤖 Rule-Based Chatbot

A conversational AI chatbot built using pattern matching and rule-based responses. This bot can handle multiple intents, maintain conversation history, and answer domain-specific questions.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Sample Conversations](#sample-conversations)
- [Future Enhancements](#future-enhancements)

## 🔍 Overview

This rule-based chatbot uses pattern matching and intent recognition to simulate human-like conversations. It maintains conversation history, has a knowledge base for FAQs, and provides an interactive console interface.

## ✨ Features

### Core Functionalities
- **Intent Recognition**: Identifies user intent (greeting, help, small talk, etc.)
- **Pattern Matching**: Uses regex patterns to understand user input
- **Knowledge Base**: Predefined responses for common questions
- **Conversation Logging**: Saves all interactions to JSON file
- **Extensible Design**: Easy to add new patterns and responses

### Supported Intents
| Intent | Description | Example |
|--------|-------------|---------|
| Greeting | Welcome messages | "Hello", "Hi" |
| Farewell | Exit conversations | "Bye", "Goodbye" |
| Help | Bot capabilities | "What can you do?" |
| Time | Current time queries | "What time is it?" |
| Date | Current date queries | "Today's date" |
| Weather | Weather information | "How's the weather?" |
| Small Talk | Casual conversation | "How are you?" |

## 🛠️ Technologies Used

- **Python 3.8+**: Core programming language
- **Regular Expressions (re)**: Pattern matching
- **JSON**: Conversation logging
- **datetime**: Time and date handling
- **pathlib**: File path management

## 📦 Installation

### Prerequisites
```bash
# Python 3.8 or higher required
python --version
