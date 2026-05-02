import sqlite3
import json
from datetime import datetime
import gradio as gr
from groq import Groq  



def get_db_connection():
    conn = sqlite3.connect('finance_tracker.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS salary (id INTEGER PRIMARY KEY AUTOINCREMENT, amount REAL, month TEXT, year INTEGER, created_at TEXT)')
        cursor.execute('CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, amount REAL, category TEXT, description TEXT, date TEXT, created_at TEXT)')
        conn.commit()

def set_salary(amount, month=None, year=None):
    try:
        num_amount = float(str(amount).replace('$', '').replace(',', ''))
        now = datetime.now()
        with get_db_connection() as conn:
            conn.execute('INSERT INTO salary (amount, month, year, created_at) VALUES (?, ?, ?, ?)', (num_amount, month or now.strftime("%B"), year or now.year, now.isoformat()))
            conn.commit()
        return f"Salary ${num_amount:,.2f} saved!"
    except: return "Error saving salary."

def log_expense(amount, category, description):
    try:
        num_amount = float(str(amount).replace('$', '').replace(',', ''))
        with get_db_connection() as conn:
            conn.execute('INSERT INTO expenses (amount, category, description, date, created_at) VALUES (?, ?, ?, ?, ?)', (num_amount, category, description, datetime.now().strftime("%Y-%m-%d"), datetime.now().isoformat()))
            conn.commit()
        return f"Logged ${num_amount:,.2f} for {category}."
    except: return "Error logging expense."

def get_balance():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT amount, month, year FROM salary ORDER BY id DESC LIMIT 1')
        row = cursor.fetchone()
        if not row: return {"salary": 0, "spent": 0, "remaining": 0, "month": "N/A"}
        cursor.execute('SELECT SUM(amount) as total FROM expenses')
        spent = cursor.fetchone()['total'] or 0
        return {"salary": row['amount'], "spent": spent, "remaining": row['amount'] - spent, "month": f"{row['month']} {row['year']}"}


client = Groq(api_key="")

def run_agent(user_input, history):
    
    system_prompt = """
    You are a Finance Assistant. 
    1. If user mentions salary: Output ONLY 'TOOL:SET_SALARY|amount|month|year'
    2. If user mentions expense: Output ONLY 'TOOL:LOG_EXPENSE|amount|category|description'
    3. Otherwise, reply naturally.
    """
    
    clean_messages = [{"role": "system", "content": system_prompt}]
    for msg in history:
        clean_messages.append({"role": msg["role"], "content": msg["content"]})
    clean_messages.append({"role": "user", "content": user_input})

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=clean_messages
        )
        ai_reply = completion.choices[0].message.content

        
        
        if "TOOL:SET_SALARY" in ai_reply:
            parts = ai_reply.split("|")
            
            set_salary(parts[1], parts[2], parts[3])
            bal = get_balance() 
            return f"✅ Salary saved! Your new balance is ${bal['remaining']:,.2f}."

        elif "TOOL:LOG_EXPENSE" in ai_reply:
            parts = ai_reply.split("|")
            
            log_expense(parts[1], parts[2], parts[3])
            bal = get_balance() 
            return f"💸 Expense logged. Remaining balance: ${bal['remaining']:,.2f}."

        
        return ai_reply

    except Exception as e:
        return f"⚠️ Error: {str(e)}"



CSS = """

body, .gradio-container { 
    font-family: 'Inter', sans-serif !important; 
    background-color: #000000 !important; 
}


#chatbot { 
    background-color: #000000 !important; 
    border: 3px solid #ffffff !important; 
}


#chatbot .message.user > div { 
    background-color: #008000 !important; 
    color: #ffffff !important; 
    font-size: 22px !important; 
    font-weight: bold !important;
    border-radius: 15px !important;
}


#chatbot .message.bot > div { 
    background-color: #1a1a1a !important; 
    color: #ffffff !important; 
    font-size: 22px !important; 
    font-weight: 500 !important;
    border: 1px solid #ffffff !important;
    border-radius: 15px !important;
}


#chatbot .bot p, #chatbot .user p, #chatbot .bot span, #chatbot .user span {
    color: #ffffff !important;
}


#msg-input textarea { 
    background-color: #ffffff !important; 
    color: #000000 !important; 
    font-size: 22px !important;
    font-weight: bold !important;
    border: 4px solid #ffcc00 !important;
}


.prose {
    color: #ffffff !important;
    font-size: 24px !important;
}

.prose code {
    color: #00ff00 !important; 
    background-color: #222222 !important;
    font-size: 24px !important;
}

/* Buttons */
.qa-btn { 
    background-color: #ffcc00 !important; 
    color: #000000 !important; 
    font-weight: bold !important;
    font-size: 18px !important;
}
"""

def build_ui():
    init_db()
    with gr.Blocks(title="FinanceAI") as demo:
        gr.Markdown("# 💰 FINANCE AI ASSISTANT")
        
        with gr.Row():
            salary_md = gr.Markdown("**Salary**\n\n`$0.00`")
            spent_md = gr.Markdown("**Spent**\n\n`$0.00`")
            remain_md = gr.Markdown("**Remaining**\n\n`$0.00`")

        chatbot = gr.Chatbot(
    value=[{"role": "assistant", "content": "HI! HOW CAN I HELP?"}], 
    elem_id="chatbot", 
    height=450
   
)
        
        msg = gr.Textbox(placeholder="Type here...", show_label=False, elem_id="msg-input")
        send = gr.Button("SEND →", variant="primary", elem_id="send-btn")

        
        def refresh():
            b = get_balance()
            return (
                f"**Salary**\n\n`${b['salary']:,.2f}`", 
                f"**Spent**\n\n`${b['spent']:,.2f}`", 
                f"**Remaining**\n\n`${b['remaining']:,.2f}`"
            )

        
        def chat_and_update(txt, h):
           
            reply = run_agent(txt, h)
            
           
            h.append({"role": "user", "content": txt})
            h.append({"role": "assistant", "content": reply})
            
            
            s, sp, r = refresh()
            
           
            return h, "", s, sp, r

       
        demo.load(refresh, None, [salary_md, spent_md, remain_md])

        
        send.click(
            chat_and_update, 
            inputs=[msg, chatbot], 
            outputs=[chatbot, msg, salary_md, spent_md, remain_md]
        )
        
       
        msg.submit(
            chat_and_update, 
            inputs=[msg, chatbot], 
            outputs=[chatbot, msg, salary_md, spent_md, remain_md]
        )

    return demo

if __name__ == "__main__":
    build_ui().launch(css=CSS)