from enum import Enum, auto

class Language(Enum):
  # Хранит поддерживаемые языки.
  EN = auto()
  RU = auto()
  DE = auto()
  FR = auto()

class Polarity(Enum):
  # Хранит варианты тональности текста.
  POSITIVE = 'positive'
  NEUTRAL = 'neutral'
  NEGATIVE = 'negative'
