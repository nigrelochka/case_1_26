import re
from domain.types import Text_Stats
from infrastructure.validation import validateText
from infrastructure.language_detector import detectLanguage
from infrastructure.syllable_counters import getSyllableCounter
from infrastructure.flesch_calculators import fleschIndex, fleschKincaid, interpretFlesch
from infrastructure.sentiment import analyzeSentiment
from infrastructure.metrics import lexicalDiversity, rareWordDensity

def analyzeTextService(text: str) -> dict:
  # Собирает полный результат анализа текста.
  text = validateText(text)

  language = detectLanguage(text)

  words = re.findall(r'\b\w+\b', text)
  sentences = re.split(r'[.!?]+', text)
  sentences = [sentence for sentence in sentences if sentence.strip()]

  wordCount = len(words)
  sentenceCount = max(len(sentences), 1)

  syllableCounter = getSyllableCounter(language)
  syllableCount = 0

  for word in words:
    syllableCount += syllableCounter(word)

  avgSentenceLength = wordCount / sentenceCount

  if wordCount > 0:
    avgWordSyllables = syllableCount / wordCount
  else:
    avgWordSyllables = 0.0

  stats = Text_Stats(
    sentenceCount = sentenceCount,
    wordCount = wordCount,
    syllableCount = syllableCount,
    avgSentenceLength = avgSentenceLength,
    avgWordSyllables = avgWordSyllables
  )

  fleschScore = fleschIndex(stats, language)
  kincaidScore = fleschKincaid(stats)
  interpretation = interpretFlesch(fleschScore)

  polarityValue, subjectivity = analyzeSentiment(text, language)

  if polarityValue > 0.1:
    polarity = 'positive'
  elif polarityValue < -0.1:
    polarity = 'negative'
  else:
    polarity = 'neutral'

  return {
    'language': language.name.lower(),
    'fleschIndex': round(fleschScore, 2),
    'fleschKincaid': round(kincaidScore, 2),
    'interpretation': interpretation,
    'polarity': polarity,
    'subjectivity': round(subjectivity, 2),
    'lexicalDiversity': round(lexicalDiversity(text), 2),
    'rareWordDensity': round(rareWordDensity(text, language), 2),
    'stats': {
      'sentenceCount': sentenceCount,
      'wordCount': wordCount,
      'syllableCount': syllableCount,
      'avgSentenceLength': round(avgSentenceLength, 2),
      'avgWordSyllables': round(avgWordSyllables, 2)
    }
  }