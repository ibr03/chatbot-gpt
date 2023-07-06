from flask import Flask, render_template, request
from gpt import get_chat_response, load_chat_log, save_chat_log

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_chatbot_response', methods=['POST'])
def get_chatbot_response():
    user_message = request.form['user_message']
    bot_response = get_chat_response(user_message)
    return {'response': bot_response}

if __name__ == '__main__':
    app.run(port=8000)
