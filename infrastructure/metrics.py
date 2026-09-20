import re

from wordfreq import zipf_frequency

from domain.types import Language


def lexicalDiversity(text: str) -> float:
  words = re.findall(r'\b\w+\b', text.lower())

  if not words:
    return 0.0

  uniqueWords = set(words)

  return len(uniqueWords) / len(words)


def rareWordDensity(
  text: str,
  language: Language,
  threshold: float = 3.0
) -> float:
  words = re.findall(r'\b\w+\b', text.lower())

  if not words:
    return 0.0

  languageCodes = {
    Language.RU: 'ru',
    Language.EN: 'en',
    Language.DE: 'de',
    Language.FR: 'fr',
  }

  languageCode = languageCodes[language]

  rareWordsCount = 0

  for word in words:
    frequency = zipf_frequency(word, languageCode)

    if frequency < threshold:
      rareWordsCount += 1

  return rareWordsCount / len(words)