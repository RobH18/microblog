import json
import requests
from flask_babel import _
from app import app

def translate(text, source_language, dest_language):
    # if 'YD_TRANSLATOR_KEY' not in app.config or not app.config['YD_TRANSLATOR_KEY']:
    #     return _('Error: the translation service is not configured.')
    # auth = {'Ocp-Apim-Subscription-Key': app.config['YD_TRANSLATOR_KEY']}
    auth = 'trnsl.1.1.20180404T232116Z.45c8e76c703dc4c2.39399ca4c23aefa4c121213b7983e21d5fec66db'
    r = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate?key={}&text={}&lang={}-{}'.format(
        auth, text, source_language, dest_language))
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    result = json.loads(r.content.decode('utf-8-sig'))
    return result.get('text')[0]