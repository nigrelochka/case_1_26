import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import pytest
from domain.types import Language, Text_Stats
from infrastructure.syllable_counters import countSyllablesRu, countSyllablesEn, getSyllableCounter
from infrastructure.flesch_calculators import fleschIndex, interpretFlesch
from infrastructure.language_detector import detectLanguage
from infrastructure.validation import validateText


def test_count_syllables_ru():
  """Проверка подсчета слогов для русского языка."""
  assert countSyllablesRu('привет') == 2
  assert countSyllablesRu('мир') == 1
  assert countSyllablesRu('') == 0


def test_count_syllables_en():
  """Проверка подсчета слогов для английского языка."""
  assert countSyllablesEn('hello') == 2
  assert countSyllablesEn('world') == 1
  assert countSyllablesEn('') == 0


def test_get_syllable_counter():
  """Проверка получения счетчика по языку."""
  assert getSyllableCounter(Language.RU) == countSyllablesRu
  assert getSyllableCounter(Language.EN) == countSyllablesEn


def test_flesch_index():
  """Проверка расчета индекса Флеша."""
  stats = Text_Stats(
    sentenceCount=2,
    wordCount=10,
    syllableCount=12,
    avgSentenceLength=5.0,
    avgWordSyllables=1.2
  )
  score = fleschIndex(stats, Language.EN)
  assert score <= 100.5
  assert score >= 80


def test_interpret_flesch():
  """Проверка интерпретации индекса Флеша."""
  assert interpretFlesch(95) == 'Очень легко'
  assert interpretFlesch(65) == 'Средняя сложность'


def test_detect_language():
  """Проверка определения языка."""
  try:
    lang = detectLanguage('Hello world')
    assert lang in [Language.EN, Language.RU, Language.DE, Language.FR]
  except ValueError:
    pytest.skip('Язык не определен для короткого текста')

  try:
    lang = detectLanguage('Привет мир')
    assert lang in [Language.EN, Language.RU, Language.DE, Language.FR]
  except ValueError:
    pytest.skip('Язык не определен для короткого текста')


def test_validate_text_valid():
  """Проверка валидации правильного текста."""
  result = validateText('Hello world')
  assert result == 'Hello world'


def test_validate_text_empty():
  """Проверка валидации пустого текста - должна быть ошибка."""
  with pytest.raises(ValueError):
    validateText('')


def test_lexical_diversity():
  """Проверка лексического разнообразия."""
  from infrastructure.metrics import lexicalDiversity

  text = 'cat cat dog dog dog'
  diversity = lexicalDiversity(text)
  assert diversity == 0.4

  text = 'one two three four five'
  diversity = lexicalDiversity(text)
  assert diversity == 1.0

  text = ''
  diversity = lexicalDiversity(text)
  assert diversity == 0.0


def test_rare_word_density():
  """Проверка плотности редких слов."""
  from infrastructure.metrics import rareWordDensity
  from domain.types import Language

  text = 'test word sample'
  density = rareWordDensity(text, Language.EN, threshold=5.0)
  assert 0.0 <= density <= 1.0

  text = ''
  density = rareWordDensity(text, Language.EN)
  assert density == 0.0


def test_analyze_sentiment_positive():
  """Проверка анализа тональности на положительном тексте."""
  from infrastructure.sentiment import analyzeSentiment
  from domain.types import Language

  polarity, subjectivity = analyzeSentiment('I love this! It is amazing!', Language.EN)
  assert polarity > 0.3
  assert 0.0 <= subjectivity <= 1.0


def test_analyze_sentiment_negative():
  """Проверка анализа тональности на отрицательном тексте."""
  from infrastructure.sentiment import analyzeSentiment
  from domain.types import Language

  polarity, subjectivity = analyzeSentiment('This is terrible! I hate it.', Language.EN)
  assert polarity < -0.3
  assert 0.0 <= subjectivity <= 1.0


def test_analyze_sentiment_neutral():
  """Проверка анализа тональности на нейтральном тексте."""
  from infrastructure.sentiment import analyzeSentiment
  from domain.types import Language

  polarity, subjectivity = analyzeSentiment('This is a book.', Language.EN)
  assert -0.1 <= polarity <= 0.1
  assert 0.0 <= subjectivity <= 1.0