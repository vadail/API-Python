import json
import boto3
from models import todoDAO
from utils import decimal_encoder

comprehend = boto3.client(service_name='comprehend')
translator = boto3.client(service_name='translate')


def lambda_handler(event, context):

    # Obtengo el idioma a traducir de la peticion HTTP
    language = event['pathParameters']['language']

    # fetch todo from the database
    result = todoDAO.TodoDAO().get_item(event['pathParameters']['id'])

    # Traduzco el texto al lenguage solicitado
    translatedText = translateText(result['text'], language)

    # Grabo el texto traducido en el campo text del Item
    result['text'] = translatedText

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result,
                           cls=decimal_encoder.DecimalEncoder)
    }

    return response


# Funcion encargada de traducir el texto introducido (text) al lenguaje
# deseado (languageToTranslate) haciendo uso de los servicios comprehend
# y translate
def translateText(text, languageToTranslate):
    dominantLanguage = "unknow"

    # Detectamos el lenguage del texto introducido
    dominantsLanguages = comprehend.detect_dominant_language(Text=text)

    # Si no hemos conseguido detectar el lenguage dominante generamos una
    #  excepción. En caso contrario traducimos el texto al leguage deseado.
    if not dominantsLanguages:
        raise Exception(
            "Couldn't translate the text of the todo item. "
            "Error detecting dominant language\n")
    else:
        dominantLanguage = dominantsLanguages["Languages"][0]["LanguageCode"]
        result = translator.translate_text(
            Text=text,
            SourceLanguageCode=dominantLanguage,
            TargetLanguageCode=languageToTranslate)
        translatedText = result.get('TranslatedText')

    return translatedText
