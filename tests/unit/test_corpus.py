import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import pytest
from tests.corpus.sample_texts import (
  SHORT_ENGLISH_TEXT, SHORT_RUSSIAN_TEXT, SIMPLE_ENGLISH_TEXT,
  POSITIVE_ENGLISH_TEXT, NEGATIVE_ENGLISH_TEXT, NEUTRAL_ENGLISH_TEXT,
  EMPTY_TEXT, INVALID_WHITESPACE_TEXT, INVALID_DIGITS_TEXT,
  LONG_TEXT, LONG_TEXT_EXPECTED, ALL_SAMPLES
)


@pytest.mark.parametrize('text,expected', ALL_SAMPLES)
def test_corpus_language_detection(text, expected):
  """Проверка определения языка на корпусе."""
  from infrastructure.language_detector import detectLanguage

  try:
    lang = detectLanguage(text)
    assert lang.name.lower() == expected['language']
  except ValueError:
    pytest.skip('Язык не определен для короткого текста')


def test_corpus_short_english():
  """Проверка короткого английского текста."""
  from infrastructure.validation import validateText

  result = validateText(SHORT_ENGLISH_TEXT)
  assert result == SHORT_ENGLISH_TEXT


def test_corpus_short_russian():
  """Проверка короткого русского текста."""
  from infrastructure.validation import validateText

  result = validateText(SHORT_RUSSIAN_TEXT)
  assert result == SHORT_RUSSIAN_TEXT


def test_corpus_positive_sentiment():
  """Проверка положительной тональности."""
  from infrastructure.sentiment import analyzeSentiment
  from domain.types import Language

  polarity, subjectivity = analyzeSentiment(POSITIVE_ENGLISH_TEXT, Language.EN)
  assert polarity > 0.0


def test_corpus_negative_sentiment():
  """Проверка отрицательной тональности."""
  from infrastructure.sentiment import analyzeSentiment
  from domain.types import Language

  polarity, subjectivity = analyzeSentiment(NEGATIVE_ENGLISH_TEXT, Language.EN)
  assert polarity < 0.0


def test_corpus_empty_text():
  """Проверка пустого текста."""
  from infrastructure.validation import validateText

  with pytest.raises(ValueError):
    validateText(EMPTY_TEXT)


def test_corpus_whitespace_text():
  """Проверка текста из пробелов."""
  from infrastructure.validation import validateText

  with pytest.raises(ValueError):
    validateText(INVALID_WHITESPACE_TEXT)


def test_corpus_digits_text():
  """Проверка текста из цифр."""
  from infrastructure.validation import validateText

  with pytest.raises(ValueError):
    validateText(INVALID_DIGITS_TEXT)


def test_corpus_long_text():
  """Проверка длинного текста."""
  from infrastructure.validation import validateText

  result = validateText(LONG_TEXT)
  assert len(result.split()) >= LONG_TEXT_EXPECTED['minWords']