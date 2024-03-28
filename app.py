# Importing necessary modules

from flask import Flask, render_template, jsonify, redirect, url_for, request
import m as main1
import string 
import car_details as cd
from difflib import SequenceMatcher
import webbrowser

# Creating a Flask app instance
app = Flask(__name__)
first_time = True

def get_response(chatbot, user_input):
    
    """Returns the response from the chatbot based on the user's input."""
    user_input = user_input.lower().translate(str.maketrans('', '', string.punctuation))
    max_similarity = 0
    best_match = None
    for question in chatbot:
        similarity = SequenceMatcher(None, user_input, question).ratio()
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = question
    if max_similarity >= 0.7:
        return chatbot[best_match]
    else:
        return cd.others(user_input)

@app.route('/redirect_to_second')
def redirect_to_second():
    return redirect(url_for('second_page'))

# Route for the second page
@app.route('/second_page')
def second_page():
    res,history = cd.photos_get()
    if "None" in res:
        print("did'nt get the name of car")
        return render_template("next_page.html", res=f"{res}{history}")
    for i in res:
        webbrowser.open_new_tab(i)
    return render_template("next_page.html", res=res)

    

# Defining the route for the home page
@app.route("/")
def index():
    return render_template("index.html")


# Defining the route for getting bot response
@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    chatbot = main1.create_chatbot()
    if userText in chatbot:
        response = chatbot[userText]
        return response
    else:
        
        try:
            response = get_response(chatbot, userText)
            return response
        except Exception as e:
            try:
                response = get_response(chatbot, userText)
                return response
            except:
                try:
                    response = get_response(chatbot, userText)
                    return response
                except:
                    return f"An error occurred: {str(e)}  Trying again"
