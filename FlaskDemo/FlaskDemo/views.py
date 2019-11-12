from FlaskDemo import app
from flask import render_template,escape, url_for,request
from chatterbot.trainers import ListTrainer,ChatterBotCorpusTrainer
from chatterbot import ChatBot
import datetime
import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["test_mydatabase"]
mycol = mydb["test_colletions"]
data_output = list()
data_input = list()
english_bot = ChatBot("chatterbot")

def datetime():
    current_datetime = datetime.datetime.now()
    return (current_datetime)
def start_bot():
    trainer1 = ChatterBotCorpusTrainer(english_bot)
    trainer1.train("chatterbot.corpus.english")
    return english_bot
def process_input(data):
    while True:
        try:
            bot_response = english_bot.get_response(data)
            return bot_response
        except(KeyboardInterrupt, EOFError, SystemExit):
            break
    else:
        return "No response is registered"



@app.route('/',methods = ['POST','GET'])
def hello():
    if request.method == 'GET':
        return render_template("Chatbot.html")

    if request.method == 'POST':
        user_input = request.form
        for key,values in user_input.items():
           data_input.append(values)
        processed_output = process_input(data_input[-1])
        data_output.append(processed_output)
        details_db = {"User":"Test_demo","input":values,"Output":processed_output}
        mycol.insert_one(details_db)
        return render_template("Chatbot.html",data_output = data_output,data_input = data_input,length = len(data_output) )

start_bot()
app.run(port=5000)


