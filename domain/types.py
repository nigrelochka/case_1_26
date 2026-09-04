from dataclasses import dataclass
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

@dataclass(frozen=True)
class Text_Stats:
  # Хранит статистику текста.
  sentenceCount: int
  wordCount: int
  syllableCount: int
  avgSentenceLength: float
  avgWordSyllables: float

@dataclass(frozen=True)
class Analysis_Result:
  # Хранит итоговый результат анализа текста.
  language: Language
  fleschIndex: float
  fleschKincaid: float
  interpretation: str
  polarity: Polarity
  subjectivity: float
  lexicalDiversity: float
  rareWordDensity: float
  stats: Text_Stats