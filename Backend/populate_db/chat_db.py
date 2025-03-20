# this will store the previous conversations of the chatbot

import sqlite3

connection = sqlite3.connect("chat_history.db")
cursor = connection.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS chat_history (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_input TEXT,
                   bot_response TEXT,
                   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
               )
               """)

connection.commit()

def insert_chat(user_input,bot_response):
    """Inserts a new chat message into the database."""
    cursor.execute("INSERT INTO chat_history (user_input,bot_response) VALUES (?,?)",(user_input,bot_response))
    connection.commit()
    
    
def get_recent_chats(limit=5):
    """Retrieves the last `limit` messages for context."""
    cursor.execute("SELECT user_input, bot_response FROM chat_history ORDER BY timestamp DESC LIMIT ?",(limit,))
    return cursor.fetchall()


