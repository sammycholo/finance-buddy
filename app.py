from flask import Flask, render_template, request
from genai_chat import GenAiChat
from dotenv import load_dotenv
import os

def create_app():
    app = Flask(__name__)
    load_dotenv()

    chat_history = []

    @app.route("/", methods=["POST","GET"])
    def chat():
        prompt = ""
        if request.method == "POST":
            prompt = request.form["prompt"]
        else:
            prompt = "Who are you and what can you do?"
        
        genai_chat = GenAiChat()
        response, history = genai_chat.send_chat(os.getenv("CONTEXT"), prompt)

        chat_history.extend(history)

        model ={
            "bot_name": os.getenv("BOT_NAME"),
            "slogan": os.getenv("SLOGAN"),
            #"message": response.text,
            "prompt": prompt,
            "chat_history": chat_history,
        }
        return render_template("index.html", model=model)
    return app
if __name__ == "__main__":
    app = create_app()
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", int(os.getenv("PORT")))),
    )