# 💰 Finance AI Assistant

An intelligent, conversational personal finance tracker that leverages Large Language Models (LLMs) to help users manage their income and expenses through natural language.

## ✨ Key Features

*   **Natural Language Processing:** Built with **Llama 3.3-70B (via Groq API)** to understand financial intent from casual conversations.
*   **Real-time Dashboard:** Instantly updates Salary, Spent, and Remaining balances as you chat.
*   **High-Contrast UI:** Specially designed with a dark theme and large fonts for superior readability and accessibility.
*   **Persistent Storage:** Uses **SQLite** to ensure your financial data is safely stored and retrieved across sessions.
*   **Ultra-low Latency:** Powered by Groq's LPU technology for near-instant AI responses.

## 🛠️ Tech Stack

*   **Language:** Python 3.x
*   **AI Model:** Llama 3.3-70B-Versatile (Groq Cloud)
*   **Frontend:** Gradio (Custom CSS styling)
*   **Database:** SQLite3

## 🚀 Getting Started

### Prerequisites
* Python installed on your system.
* A Groq API Key (Get it from [Groq Console](https://console.groq.com/)).

### Installation

1. Clone the repository:
   
```bash
   git clone [https://github.com/YOUR_USERNAME/FinanceAI-Assistant.git](https://github.com/YOUR_USERNAME/FinanceAI-Assistant.git)
   cd FinanceAI-Assistant

Install required dependencies:

Bash
pip install gradio groq
Set up your API Key:
Replace the api_key in app.py with your Groq API key:

Python
client = Groq(api_key="YOUR_GROQ_API_KEY")
Run the application:

Bash
python app.py
📸 UI Preview
Dark Mode: Pure black background with high-contrast text.

Chatbot Interface: Intuitive message bubbles for User and AI.

Stats Cards: Big, bold numbers for quick financial overview.

📝 Example Commands
"I received my salary of $5000 for May."

"I spent $150 on groceries and $40 for taxi today."

"How much money is left in my account?"

🛡️ License
Distributed under the MIT License. See LICENSE for more information.

Developed by Charitha 🚀
