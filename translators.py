import requests
import json

def format_dmt_translation(translation):
    return translation.replace("🔽", " ")

def translate_sa_to_en(text):
    """Translates Sanskrit text to English using an API."""
    url = "https://dharmamitra.org/api/translation-no-stream/"
    payload = {"input_sentence": text, "input_encoding": "auto", "target_lang": "english"}
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            translation = response.text.strip()
            return format_dmt_translation(translation)
        else:
            print(f"⚠️ API Error: {response.status_code} - {response.text}")
            return ""
    except Exception as e:
        print(f"❌ Translation API Error: {e}")
        return ""

import asyncio
from googletrans import Translator

translator = Translator()

async def translate_en_to_ta(text):
    """Translates English text to Tamil using Google Translate (async)."""
    try:
        translation = await translator.translate(text, src='en', dest='ta')
        return translation.text
    except Exception as e:
        print(f"❌ Tamil Translation Error: {e}")
        return ""
