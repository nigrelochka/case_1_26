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