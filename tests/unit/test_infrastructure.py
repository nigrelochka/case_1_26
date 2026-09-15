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


def test_count_syllables_de():
  """Проверка подсчета слогов для немецкого языка."""
  from infrastructure.syllable_counters import countSyllablesDe

  assert countSyllablesDe('hallo') == 2
  assert countSyllablesDe('welt') == 1
  assert countSyllablesDe('') == 0


def test_count_syllables_fr():
  """Проверка подсчета слогов для французского языка."""
  from infrastructure.syllable_counters import countSyllablesFr

  assert countSyllablesFr('bonjour') == 2
  assert countSyllablesFr('monde') == 1
  assert countSyllablesFr('') == 0


def test_get_syllable_counter_all_languages():
  """Проверка получения счетчика для всех языков."""
  from infrastructure.syllable_counters import (
    getSyllableCounter, countSyllablesRu, countSyllablesEn,
    countSyllablesDe, countSyllablesFr
  )
  from domain.types import Language

  assert getSyllableCounter(Language.RU) == countSyllablesRu
  assert getSyllableCounter(Language.EN) == countSyllablesEn
  assert getSyllableCounter(Language.DE) == countSyllablesDe
  assert getSyllableCounter(Language.FR) == countSyllablesFr


def test_flesch_index_german():
  """Проверка расчета индекса Флеша для немецкого."""
  from infrastructure.flesch_calculators import fleschIndex
  from domain.types import Language, Text_Stats

  stats = Text_Stats(
    sentenceCount=2,
    wordCount=10,
    syllableCount=12,
    avgSentenceLength=5.0,
    avgWordSyllables=1.2
  )
  score = fleschIndex(stats, Language.DE)
  assert isinstance(score, (int, float))


def test_flesch_index_french():
  """Проверка расчета индекса Флеша для французского."""
  from infrastructure.flesch_calculators import fleschIndex
  from domain.types import Language, Text_Stats

  stats = Text_Stats(
    sentenceCount=2,
    wordCount=10,
    syllableCount=12,
    avgSentenceLength=5.0,
    avgWordSyllables=1.2
  )
  score = fleschIndex(stats, Language.FR)
  assert isinstance(score, (int, float))


def test_flesch_kincaid():
  """Проверка индекса Флеша-Кинкейда."""
  from infrastructure.flesch_calculators import fleschKincaid
  from domain.types import Text_Stats

  stats = Text_Stats(
    sentenceCount=2,
    wordCount=10,
    syllableCount=12,
    avgSentenceLength=5.0,
    avgWordSyllables=1.2
  )
  grade = fleschKincaid(stats)
  assert isinstance(grade, (int, float))


def test_interpret_flesch_all_levels():
  """Проверка всех уровней интерпретации Флеша."""
  from infrastructure.flesch_calculators import interpretFlesch

  assert interpretFlesch(95) == 'Очень легко'
  assert interpretFlesch(85) == 'Легко'
  assert interpretFlesch(75) == 'Довольно легко'
  assert interpretFlesch(65) == 'Средняя сложность'
  assert interpretFlesch(55) == 'Довольно трудно'
  assert interpretFlesch(40) == 'Трудно'
  assert interpretFlesch(20) == 'Очень трудно'


def test_detect_language_german():
  """Проверка определения немецкого языка."""
  from infrastructure.language_detector import detectLanguage
  from domain.types import Language

  lang = detectLanguage('Das ist ein deutscher Text mit vielen Wörtern')
  assert lang == Language.DE


def test_detect_language_french():
  """Проверка определения французского языка."""
  from infrastructure.language_detector import detectLanguage
  from domain.types import Language

  lang = detectLanguage('Ceci est un texte français avec beaucoup de mots')
  assert lang == Language.FR


def test_validate_text_not_string():
  """Проверка валидации, если передан не текст."""
  from infrastructure.validation import validateText
  import pytest

  with pytest.raises(TypeError):
    validateText(123)


def test_validate_text_only_digits():
  """Проверка валидации текста только из цифр."""
  from infrastructure.validation import validateText
  import pytest

  with pytest.raises(ValueError):
    validateText('12345')


def test_validate_text_strips_whitespace():
  """Проверка, что валидация убирает пробелы."""
  from infrastructure.validation import validateText

  result = validateText('  hello  ')
  assert result == 'hello'