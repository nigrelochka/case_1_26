from pydantic import BaseModel, Field, validator
from typing import List, Optional

class Analysis_Request(BaseModel):
  """Запрос на анализ одного текста"""
  text: str = Field(..., min_length = 1, max_length = 10000,
                      description = "Текст для анализа")

  @validator('text')
  def validate_text(cls, v):
    """Проверка, что текст не пустой"""
    if not v.strip():
      raise ValueError('Текст не может быть пустым')
    return v

class Batch_Request(BaseModel):
  """Запрос на анализ нескольких текстов"""
  texts: List[str] = Field(..., min_length = 1, max_length = 100,
                          description = 'Список текстов для анализа')

  @validator('texts')
  def validate_texts(cls, v):
    """Проверка, что все тексты не пустые"""
    for text in v:
      if not text.strip():
        raise ValueError('Текст в списке не может быть пустым')
    return v

# Ответы, которые возвращает сервер

class Text_Stats(BaseModel):
  """Статистика текста"""
  sentences: int = Field(..., description = 'Количество предложений')
  words: int = Field(..., description = 'Количество слов')
  syllables: int = Field(..., description = 'Количество слогов')
  avg_sentence_length: float = Field(..., description = 'Средняя длина предложения')
  avg_word_length: float = Field(..., description = 'Средняя длина слова')

class Flesch_Metrics(BaseModel):
  """Метрики Флеша"""
  index: float = Field(..., description = 'Индекс Флеша')
  level: str = Field(..., description = 'Уровень сложности')
  grade_level: Optional[float] = Field(None, description = 'Flesch-Kincaid Grade Level')

class Sentiment_Metrics(BaseModel):
  """Метрики тональности"""
  polarity: float = Field(..., ge = -1, le = 1, description = 'Полярность (-1 до 1)')
  subjectivity: float = Field(..., ge = 0, le = 1, description = 'Субъективность (0 до 1)')
  sentiment: str = Field(..., description = 'Настроение: positive/neutral/negative')

class Analysis_Result(BaseModel):
  """Полный результат анализа"""
  language: str = Field(..., description = 'Язык текста (ru/en/de/fr)')
  stats: Text_Stats = Field(..., description = 'Статистика текста')
  flesch: Flesch_Metrics = Field(..., description = 'Метрики Флеша')
  sentiment: Sentiment_Metrics = Field(..., description = 'Метрики тональности')
  lexical_diversity: float = Field(..., ge = 0, le = 1, description = 'Лексическое разнообразие')
  rare_word_density: float = Field(..., ge = 0, le = 1, description = 'Плотность редких слов')

class Analysis_Response(BaseModel):
  """Ответ на запрос анализа"""
  status: str = Field("success", description = 'Статус ответа')
  result: Analysis_Result = Field(..., description = 'Результат анализа')
  cached: bool = Field(False, description = 'Взят ли результат из кэша')
  processing_time: float = Field(..., description = 'Время обработки в секундах')

class Batch_Response(BaseModel):
  """Ответ на пакетный запрос"""
  status: str = Field("success", description = 'Статус ответа')
  results: List[Analysis_Result] = Field(..., description = 'Результаты анализа')
  cached: List[bool] = Field(..., description = 'Какие результаты из кэша')
  total_time: float = Field(..., description = 'Общее время обработки')




