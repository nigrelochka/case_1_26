"""Тестовый корпус текстов с эталонными значениями."""

# Короткие тексты
SHORT_ENGLISH_TEXT = 'Hello world.'
SHORT_ENGLISH_EXPECTED = {'language': 'en', 'minWords': 2}

SHORT_RUSSIAN_TEXT = 'Привет мир.'
SHORT_RUSSIAN_EXPECTED = {'language': 'ru', 'minWords': 2}

# Простой текст для Flesch
SIMPLE_ENGLISH_TEXT = 'The cat sat on the mat.'
SIMPLE_ENGLISH_EXPECTED = {
  'language': 'en',
  'wordCount': 6,
  'sentenceCount': 1
}

# Тексты для sentiment
POSITIVE_ENGLISH_TEXT = 'I love this! It is amazing and wonderful!'
POSITIVE_ENGLISH_EXPECTED = {'language': 'en', 'polarity': 'positive'}

NEGATIVE_ENGLISH_TEXT = 'This is terrible. I hate it so much.'
NEGATIVE_ENGLISH_EXPECTED = {'language': 'en', 'polarity': 'negative'}

NEUTRAL_ENGLISH_TEXT = 'This is a book. It has pages.'
NEUTRAL_ENGLISH_EXPECTED = {'language': 'en', 'polarity': 'neutral'}

# Невалидные тексты
EMPTY_TEXT = ''
INVALID_WHITESPACE_TEXT = '   '
INVALID_DIGITS_TEXT = '12345'

# Длинный текст для нагрузочных
LONG_TEXT = 'This is a long text for testing performance. ' * 50
LONG_TEXT_EXPECTED = {'language': 'en', 'minWords': 300}

# Все тексты для параметризации
ALL_SAMPLES = [
  (SHORT_ENGLISH_TEXT, SHORT_ENGLISH_EXPECTED),
  (SHORT_RUSSIAN_TEXT, SHORT_RUSSIAN_EXPECTED),
  (SIMPLE_ENGLISH_TEXT, SIMPLE_ENGLISH_EXPECTED),
  (POSITIVE_ENGLISH_TEXT, POSITIVE_ENGLISH_EXPECTED),
  (NEGATIVE_ENGLISH_TEXT, NEGATIVE_ENGLISH_EXPECTED),
  (NEUTRAL_ENGLISH_TEXT, NEUTRAL_ENGLISH_EXPECTED),
]