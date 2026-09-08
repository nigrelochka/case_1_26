import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import requests

BASE_URL = 'http://localhost:8000'


def test_health_endpoint():
  """Проверка эндпоинта /health."""
  response = requests.get(f'{BASE_URL}/health')
  assert response.status_code == 200
  assert response.json() == {'status': 'ok'}


def test_analyze_valid_text():
  """Проверка анализа валидного текста."""
  response = requests.post(
    f'{BASE_URL}/analyze',
    json={'text': 'Hello world! This is a test.'}
  )
  assert response.status_code == 200
  data = response.json()
  assert 'status' in data
  assert data['status'] == 'success'
  assert 'result' in data
  assert 'language' in data['result']


def test_analyze_empty_text():
  """Проверка анализа пустого текста - должна быть ошибка."""
  response = requests.post(
    f'{BASE_URL}/analyze',
    json={'text': ''}
  )
  assert response.status_code in [400, 422]


def test_analyze_whitespace_text():
  """Проверка анализа текста с пробелами - должна быть ошибка."""
  response = requests.post(
    f'{BASE_URL}/analyze',
    json={'text': '   '}
  )
  assert response.status_code in [400, 422]


def test_analyze_batch():
  """Проверка пакетной обработки текстов."""
  response = requests.post(
    f'{BASE_URL}/analyze-batch',
    json={'texts': ['First.', 'Second.', 'Third.']}
  )
  assert response.status_code == 200
  data = response.json()
  assert data is not None


def test_analyze_batch_empty():
  """Проверка пакетной обработки с пустым массивом."""
  response = requests.post(
    f'{BASE_URL}/analyze-batch',
    json={'texts': []}
  )
  assert response.status_code in [400, 422]


def test_cache_works():
  """Проверка работы кэша - повторный запрос должен возвращать те же данные."""
  text = 'Cache test text'

  response1 = requests.post(f'{BASE_URL}/analyze', json={'text': text})
  assert response1.status_code == 200
  data1 = response1.json()

  response2 = requests.post(f'{BASE_URL}/analyze', json={'text': text})
  assert response2.status_code == 200
  data2 = response2.json()

  assert data1['result']['language'] == data2['result']['language']
  assert data1['result']['fleschIndex'] == data2['result']['fleschIndex']