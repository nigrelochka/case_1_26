from typing import Protocol
from .types import Language, Polarity

class Syllable_Counter(Protocol):
  def __call__(self, word: str) -> int:
    # Возвращает количество слогов в слове.
    ...

class Sentiment_Analyzer(Protocol):
  def __call__(
    self, text: str,
    language: Language
  ) -> tuple[float, float]:
    # Возвращает тональность и субъективность текста.
    ...

class Language_Detector(Protocol):
  def __call__(self, text: str) -> Language:
    # Определяет язык текста.
    ...