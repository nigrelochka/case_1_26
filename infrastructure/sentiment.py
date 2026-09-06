from deep_translator import GoogleTranslator
from textblob import TextBlob

from domain.types import Language


def translateToEnglish(text: str, language: Language) -> str:
  if language == Language.EN:
    return text

  translatedText = GoogleTranslator(
    source='auto',
    target='en'
  ).translate(text)

  return translatedText


def analyzeSentiment(text: str, language: Language) -> tuple[float, float]:
  englishText = translateToEnglish(text, language)

  blob = TextBlob(englishText)

  polarity = blob.sentiment.polarity
  subjectivity = blob.sentiment.subjectivity

  return polarity, subjectivity