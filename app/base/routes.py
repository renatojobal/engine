from crypt import methods
from email import header
import resource
from app.base import blueprint
from flask import render_template, Flask, request, Response
import spacy
import requests as request_maker
from re import search
import logging
import graphviz



@blueprint.route('/')
@blueprint.route('/index')
def index():
    return render_template('index.html')


@blueprint.route("/annotate", methods=["GET"])
def annotate():
    """
    Natural Language Proccesing
    This funciton will process a text and return entities including the reference inside dbpedia
    """
    
    args = request.args
    
    target_text = args.get("text")


    if(target_text[len(target_text)-1] == " "):
        target_text = target_text[:len(target_text)-1]

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

    if (len(nouns_list)):
        # Query each token against dbpedia


        print("Query each token against dbpedia")
        URL = "https://api.dbpedia-spotlight.org/en/annotate"
        PARAMS = {'text': nouns_as_text}
        print(f"\nNouns as text: {nouns_as_text}\n")
        original_prequest = request_maker.get(url=URL, params=PARAMS, headers={'accept': 'application/json'})
        print(f"\nOrignial Pre Request no jason: {original_prequest}\n")
        original_response = original_prequest.json()

        if original_response.get("Resources"):
            resources = original_response["Resources"]
            untagged_words = nouns_list.copy()
            for index, value in enumerate(resources):
                # Check if the key uri is corresponding to an annotated entity
                for noun in nouns_list:

                    if(search(noun, value['@surfaceForm'])):
                        # Add the as noun to the original response""
                        value["tag"] = 'noun'
                        original_response["Resources"][index] = value

                        untagged_words.remove(noun)

            
            # Add the other words that were not found in dbpedia
            for untagged in untagged_words:
                original_response["Resources"].append({"@surfaceForm" : untagged, "tag": "noun"})
                

    
        return original_response
    
    else:
        return Response("{}", status=404, mimetype='application/json')


@blueprint.route("/wake_up", methods=["GET"])
def wake_up():
    """
    This function is used to prevent the server to sleep
    """
   
    return "<p>Hi, I`m alive </p>"


@blueprint.route("/rdf", methods=["GET"])
def endpoint_rdf():
    """
    Convert a text into a rdf with fred
    """
    # Get params
    args = request.args
    
    target_text = args.get("text")
    target_prefix = args.get("prefix", default="fred:")
    target_namespace = args.get("namespace", default="http://www.ontologydesignpatterns.org/ont/fred/domain.owl#")
    target_format = args.get("format", default="json")


    # Obtain the rdf
    result_rdf = _get_rdf_from_text(target_text=target_text, prefix=target_prefix, namespace=target_namespace, format=target_format)

    # Obtain the image
    # Todo

    # Build response
    
    return Response(result_rdf.text, 
        status=200, 
        mimetype= f'application/{target_format}'
    )


def _get_rdf_from_text(target_text: str = None, prefix : str = "fred:", namespace: str = "http://www.ontologydesignpatterns.org/ont/fred/domain.owl#", format :str ="json"):
    """

    """
    if(target_text != None):
        
        fred_url = "http://wit.istc.cnr.it/stlab-tools/fred"
        params = {
            'text' : target_text,
            'prefix' : prefix,
            'namespace' : namespace
        }
        print(format)
        headers = {
            'Authorization' : 'Bearer 9c4fa397-188b-301f-90a3-4399c6bf3ccf',
            'Accept' : f'application/rdf+{format}'
        }
        response = request_maker.get(url=fred_url, params=params, headers=headers)

        return response

@blueprint.route("/image_rdf", methods=["GET"])
def endpoint_image_rdf():
    """
    """
    # Get params
    args = request.args
    
    target_rdf = args.get("rdf")


    # Obtain the rdf
    result_rdf = _get_image_from_rdf_from_web(target_rdf=target_rdf)

    # Obtain the image
    # Todo

    # Build response
    
    return Response(result_rdf.text, 
        status=200
    )

def _get_image_from_rdf_from_web(target_rdf: str, format : str ="json"):
    """
    Using an endpoint
    """
    if(target_rdf != None):
        url = "http://www.ldf.fi/service/rdf-grapher"
        params = {
            'from': format,
            'to': "png",
            'rdf': target_rdf
        }
    
        response = request_maker.get(url=url, params=params)
        return response


def _get_image_from_rdf(target_rdf: str):
    """
    Creating it from Graphviz library
    """
    if(target_rdf != None):
        dot = graphviz.Digraph(comment='The Round Table')
    

def get_nouns_list(target_text=""):
    """
    """
    nlp = spacy.load("en")
