from crypt import methods
import resource
from app.base import blueprint
from flask import render_template, Flask, request
import spacy
import requests as prequest


@blueprint.route('/')
@blueprint.route('/index')
def index():
    return render_template('index.html')


@blueprint.route("/nlp", methods=["GET"])
def nlp():
    """
    Natural Language Proccesing
    This funciton will process a text and return entities including the reference inside dbpedia
    """
    
    args = request.args
    
    target_text = args.get("text")

    # Get tokens of the text
    nlp = spacy.load("es_core_news_sm")
    doc = nlp(target_text)
    nouns_list = []
    nouns_as_text = ""
    for token in doc:
        if token.pos_ == 'NOUN' or token.pos_ == 'PROPN':
            nouns_list.append(token.text)
            nouns_as_text += f"{token.text} "
    

    print(nouns_list)

    # Query each token against dbpedia
    URL = "https://api.dbpedia-spotlight.org/en/annotate"
    PARAMS = {'text': nouns_as_text}

    response = prequest.get(url=URL, params=PARAMS, headers={'accept': 'application/json'})
    
    resources = response.json()["Resources"]

    for key in resources:
        print(key)
    
  

   
    return "<p>Hello world </p>"


@blueprint.route("/wake_up", methods=["GET"])
def wake_up():
    """
    This function is used to prevent the server to sleep
    """
   
    return "<p>Hi, I`m alive </p>"



def get_nouns_list(target_text=""):
    """
    """
    nlp = spacy.load("en")
