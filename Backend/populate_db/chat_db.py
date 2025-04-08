# this will store the previous conversations of the chatbot

import sqlite3

connection = sqlite3.connect("chat_history.db",check_same_thread=False)
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

#this all is working fine 
# # to see the data in the chat history table
# if __name__ == "__main__":
#     # Insert a test conversation (optional)
#     insert_chat("Who won the last F1 race?", "Max Verstappen won the last race.")
    
#     # Retrieve and print recent conversations
#     chats = get_recent_chats(5)
#     for user_msg,bot_msg in chats:
#         print(f"User: {user_msg}\nBot: {bot_msg}\n")
        

