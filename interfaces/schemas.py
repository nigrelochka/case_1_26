from pydantic import BaseModel, Field, validator
from typing import List


class Analysis_Request(BaseModel):
  """Запрос на анализ одного текста"""
  text: str = Field(..., min_length = 1, max_length = 10000,
                    description = 'Текст для анализа')

  @validator('text')
  def validateText(cls, v):
    """Проверка, что текст не пустой"""
    if not v.strip():
      raise ValueError('Текст не может быть пустым')
    return v


class Batch_Request(BaseModel):
  """Запрос на анализ нескольких текстов"""
  texts: List[str] = Field(..., min_length = 1, max_length = 100,
                           description = 'Список текстов для анализа')

  @validator('texts')
  def validateTexts(cls, v):
    """Проверка, что все тексты не пустые"""
    for text in v:
      if not text.strip():
        raise ValueError('Текст в списке не может быть пустым')
    return v


# Ответы, которые возвращает сервер

class Text_Stats(BaseModel):
  """Статистика текста"""
  sentenceCount: int = Field(..., description = 'Количество предложений')
  wordCount: int = Field(..., description = 'Количество слов')
  syllableCount: int = Field(..., description = 'Количество слогов')
  avgSentenceLength: float = Field(..., description = 'Средняя длина предложения')
  avgWordSyllables: float = Field(..., description = 'Среднее количество слогов в слове')


class Analysis_Result(BaseModel):
  """Полный результат анализа"""
  language: str = Field(..., description = 'Язык текста')
  fleschIndex: float = Field(..., description = 'Индекс Флеша')
  fleschKincaid: float = Field(..., description = 'Индекс Флеша-Кинкейда')
  interpretation: str = Field(..., description = 'Уровень сложности')
  polarity: str = Field(..., description = 'Тональность текста')
  subjectivity: float = Field(..., ge = 0, le = 1, description = 'Субъективность')
  lexicalDiversity: float = Field(..., ge = 0, le = 1, description = 'Лексическое разнообразие')
  rareWordDensity: float = Field(..., ge = 0, le = 1, description = 'Плотность редких слов')
  stats: Text_Stats = Field(..., description = 'Статистика текста')


class Analysis_Response(BaseModel):
  """Ответ на запрос анализа"""
  status: str = Field('success', description = 'Статус ответа')
  result: Analysis_Result = Field(..., description = 'Результат анализа')
  cached: bool = Field(False, description = 'Взят ли результат из кэша')
  processingTime: float = Field(..., description = 'Время обработки в секундах')


class Batch_Response(BaseModel):
  """Ответ на пакетный запрос"""
  status: str = Field('success', description = 'Статус ответа')
  results: List[Analysis_Result] = Field(..., description = 'Результаты анализа')
  cached: List[bool] = Field(..., description = 'Какие результаты из кэша')
  totalTime: float = Field(..., description = 'Общее время обработки')