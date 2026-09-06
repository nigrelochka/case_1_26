import time

from fastapi import FastAPI

from infrastructure.cache import Cache_Service
from interfaces.schemas import Analysis_Request, Analysis_Response, Batch_Request, Batch_Response, Analysis_Result

app = FastAPI(title='Text Analyzer')

cacheService = Cache_Service()


@app.get('/health')
def healthCheck():
  # Проверяем, что API работает.
  return {'status': 'ok'}


@app.post('/analyze', response_model=Analysis_Response)
def analyzeText(request: Analysis_Request):
  # Запоминаем время начала обработки.
  startTime = time.perf_counter()

  # Проверяем, есть ли результат в кэше.
  cachedResult = cacheService.getCachedResult(request.text)

  if cachedResult:
    return {
      'status': 'success',
      'result': cachedResult,
      'cached': True,
      'processing_time': 0.0
    }


  # Создаём временный результат анализа (потом будет заменён на работу Роли 2).
  result = {
    'language': 'ru',
    'stats': {
      'sentences': 1,
      'words': len(request.text.split()),
      'syllables': 0,
      'avg_sentence_length': 0.0,
      'avg_word_length': 0.0
    },
    'flesch': {
      'index': 0.0,
      'level': 'unknown',
      'grade_level': None
    },
    'sentiment': {
      'polarity': 0.0,
      'subjectivity': 0.0,
      'sentiment': 'neutral'
    },
    'lexical_diversity': 0.0,
    'rare_word_density': 0.0
  }

  # Сохраняем результат в кэш.
  cacheService.setCachedResult(request.text, Analysis_Result(**result))

  return {
    'status': 'success',
    'result': result,
    'cached': False,
    'processing_time': time.perf_counter() - startTime
  }

@app.post('/analyze-batch', response_model=Batch_Response)
def analyzeBatch(request: Batch_Request):
  # Запоминаем время начала обработки.
  startTime = time.perf_counter()

  results = []
  cachedResults = []

  for text in request.texts:
    # Проверяем, есть ли результат в кэше.
    cachedResult = cacheService.getCachedResult(text)

    if cachedResult:
      results.append(cachedResult)
      cachedResults.append(True)
      continue

    # Создаём временный результат анализа (временная заглушка)
    result = {
      'language': 'ru',
      'stats': {
        'sentences': 1,
        'words': len(text.split()),
        'syllables': 0,
        'avg_sentence_length': 0.0,
        'avg_word_length': 0.0
      },
      'flesch': {
        'index': 0.0,
        'level': 'unknown',
        'grade_level': None
      },
      'sentiment': {
        'polarity': 0.0,
        'subjectivity': 0.0,
        'sentiment': 'neutral'
      },
      'lexical_diversity': 0.0,
      'rare_word_density': 0.0
    }

    # Сохраняем новый результат в кэш.
    cacheService.setCachedResult(text, Analysis_Result(**result))

    results.append(result)
    cachedResults.append(False)

  return {
    'status': 'success',
    'results': results,
    'cached': cachedResults,
    'total_time': time.perf_counter() - startTime
  }