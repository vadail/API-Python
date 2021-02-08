import os
import json

from todos import decimalencoder
import boto3

dynamodb = boto3.resource('dynamodb')
comprehend = boto3.client(service_name='comprehend')
translator = boto3.client(service_name='translate')

def translate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    # Obtengo el idioma a traducir de la peticion HTTP
    language = event['pathParameters']['language']
    
    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    
    # Traduzco el texto al lenguage solicitado
    translatedText = translateText(result['Item']['text'],language)
    
    # Grabo el texto traducido en el campo text del Item
    result['Item']['text'] = translatedText
    
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response

# Funcion encargada de traducir el texto introducido (text) al lenguaje deseado (languageToTranslate) haciendo uso de los servicios comprehend y translate
def translateText (text, languageToTranslate) :
    dominantLanguage = "unknow"
    
    # Detectamos el lenguage del texto introducido
    dominantsLanguages = comprehend.detect_dominant_language(Text = text)
    
    # Si no hemos conseguido detectar ningun lenguaje introducimos en el texto devuelto un mensaje de error.
    if not dominantsLanguages:
        print("Error detecting dominants language\n")
        translatedText = "No ha sido posible traducir el texto original"
    else:
        dominantLanguage = dominantsLanguages["Languages"][0]["LanguageCode"]
        result = translator.translate_text(Text=text, SourceLanguageCode=dominantLanguage, TargetLanguageCode=languageToTranslate)
        translatedText = result.get('TranslatedText')
    
    return translatedText