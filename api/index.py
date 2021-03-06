from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Conversation, ConversationalPipeline
from flask import Flask
from flask import request, jsonify

tokenizer = AutoTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/blenderbot-400M-distill")
nlp = ConversationalPipeline(model=model, tokenizer=tokenizer)

app = Flask(__name__)

conversation = Conversation()

@app.route('/add_input', methods = ['GET'])
def add_input():
     text = request.args.get('text')
     conversation.add_user_input(text)
     result = nlp([conversation], do_sample=False, max_length=1000)
     messages = []
     for is_user, text in result.iter_texts():
          messages.append({
               'is_user': is_user,
               'text': text
          })
     return jsonify({
          'uuid': result.uuid,
          'messages': messages
     })

app.run()