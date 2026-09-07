import logging, time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.extension import _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from infrastructure.cache import Cache_Service
from interfaces.schemas import Analysis_Request, Analysis_Response, Batch_Request, Batch_Response, Analysis_Result

app = FastAPI(title='Text Analyzer')


# Подключение ограничения количества запросов
limiter = Limiter(key_func = get_remote_address)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.add_middleware(
  CORSMiddleware,
  allow_origins = ['*'],
  allow_credentials = False,
  allow_methods = ['*'],
  allow_headers = ['*']
)

cacheService = Cache_Service()

MAX_BODY_SIZE = 1024 * 1024


@app.middleware('http')
async def limitRequestSize(request: Request, callNext):
  # Проверяем размер тела HTTP-запроса.
  contentLength = request.headers.get('content-length')

  if contentLength and int(contentLength) > MAX_BODY_SIZE:
    return JSONResponse(
      status_code = 413,
      content = {
        'status': 'error',
        'message': 'Request body is too large'
      }
    )

  return await callNext(request)


logger = logging.getLogger(__name__)


@app.middleware('http')
async def logRequestMiddleware(request: Request, callNext):
  # Запоминаем время начала обработки запроса.
  startTime = time.perf_counter()

  # Передаём запрос дальше и ждём готового ответа.
  response = await callNext(request)

  # Вычисляем время обработки запроса.
  processingTime = time.perf_counter() - startTime

  # Записываем информацию о запросе в лог.
  logger.info(
    f'{request.method} {request.url.path} - '
    f'{response.status_code} - {processingTime:.4f}s'
  )

  return response


@app.exception_handler(ValueError)
def valueErrorHandler(request: Request, exc: ValueError):
  # Возвращаем ошибку 400 для некорректных данных.
  return JSONResponse(
    status_code = 400,
    content = {
      'status': 'error',
      'message': str(exc)
    }
  )


@app.exception_handler(Exception)
def generalErrorHandler(request: Request, exc: Exception):
  # Возвращаем ошибку 500 для неожиданных ошибок сервера.
  return JSONResponse(
    status_code = 500,
    content = {
      'status': 'error',
      'message': 'Internal server error'
    }
  )


@app.get('/health')
def healthCheck():
  # Проверяем, что API работает.
  return {'status': 'ok'}


@app.post('/analyze', response_model=Analysis_Response)
@limiter.limit('60/minute')
def analyzeText(request: Request, analysisRequest: Analysis_Request):
  # Запоминаем время начала обработки.
  startTime = time.perf_counter()

  # Проверяем, есть ли результат в кэше.
  cachedResult = cacheService.getCachedResult(analysisRequest.text)

  if cachedResult:
    return {
      'status': 'success',
      'result': cachedResult,
      'cached': True,
      'processingTime': 0.0
    }

  # Создаём временный результат анализа.
  result = {
    'language': 'ru',
    'fleschIndex': 0.0,
    'fleschKincaid': 0.0,
    'interpretation': 'unknown',
    'polarity': 'neutral',
    'subjectivity': 0.0,
    'lexicalDiversity': 0.0,
    'rareWordDensity': 0.0,
    'stats': {
      'sentenceCount': 1,
      'wordCount': len(analysisRequest.text.split()),
      'syllableCount': 0,
      'avgSentenceLength': 0.0,
      'avgWordSyllables': 0.0
    }
  }

  # Сохраняем результат в кэш.
  cacheService.setCachedResult(analysisRequest.text, Analysis_Result(**result))

  return {
    'status': 'success',
    'result': result,
    'cached': False,
    'processingTime': time.perf_counter() - startTime
  }


@app.post('/analyze-batch', response_model=Batch_Response)
@limiter.limit('60/minute')
def analyzeBatch(request: Request, batchRequest: Batch_Request):
  # Запоминаем время начала обработки.
  startTime = time.perf_counter()

  results = []
  cachedResults = []

  for text in batchRequest.texts:
    # Проверяем, есть ли результат в кэше.
    cachedResult = cacheService.getCachedResult(text)

    if cachedResult:
      results.append(cachedResult)
      cachedResults.append(True)
      continue

    # Создаём временный результат анализа.
    result = {
      'language': 'ru',
      'fleschIndex': 0.0,
      'fleschKincaid': 0.0,
      'interpretation': 'unknown',
      'polarity': 'neutral',
      'subjectivity': 0.0,
      'lexicalDiversity': 0.0,
      'rareWordDensity': 0.0,
      'stats': {
        'sentenceCount': 1,
        'wordCount': len(text.split()),
        'syllableCount': 0,
        'avgSentenceLength': 0.0,
        'avgWordSyllables': 0.0
      }
    }

    # Сохраняем новый результат в кэш.
    cacheService.setCachedResult(text, Analysis_Result(**result))

    results.append(result)
    cachedResults.append(False)

  return {
    'status': 'success',
    'results': results,
    'cached': cachedResults,
    'totalTime': time.perf_counter() - startTime
  }
