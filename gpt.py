import openai
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()  # take environment variables from .env.

# Replace the connection string and database name with your own MongoDB configuration
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client['chatbot_db']
collection = db['chat_log']

openai.api_key = os.getenv('OPENKEY')  # Replace with your OpenAI API key
model_name = 'gpt-3.5-turbo'

def get_chat_response(user_message):
    chat_log = load_chat_log()  # Load existing conversation history
    
    # Append the new user message to the conversation
    chat_log.append({'role': 'system', 'content': user_message})
    user_messages = [log['content'] for log in chat_log if log['role'] == 'system']
    
    # Generate a response from ChatGPT
    response = openai.Completion.create(
        engine=model_name,
        prompt=user_messages,
        temperature=0.7,
        max_tokens=50,
        n=1,
        stop=None,
        log_level='info'
    )
    
    # Extract the generated response
    bot_response = response.choices[0].text.strip()
    
    # Append the bot's response to the conversation
    chat_log.append({'role': 'system', 'content': bot_response})
    
    save_chat_log(chat_log)  # Save the updated conversation history
    
    return bot_response

def load_chat_log():
    # Implement your own logic to load and return the chat log
    # This can be stored in a file, database, or any other storage mechanism
    # For demonstration purposes, we'll simply return an empty list
    chat_log = list(collection.find())
    return chat_log

def save_chat_log(chat_log):
    # Implement your own logic to save the chat log
    collection.drop()  # Remove existing chat log documents
    collection.insert_many(chat_log)  # Insert the updated chat log
