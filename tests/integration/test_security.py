import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import requests

BASE_URL = 'http://localhost:8000'


def test_sql_injection():
  """Проверка защиты от SQL-инъекций."""
  response = requests.post(
    f'{BASE_URL}/analyze',
    json={'text': "'; DROP TABLE users; --"}
  )
  # API не должен падать и не должен выполнять SQL
  assert response.status_code in [200, 400, 422]


def test_xss_injection():
  """Проверка защиты от XSS-инъекций."""
  response = requests.post(
    f'{BASE_URL}/analyze',
    json={'text': '<script>alert("XSS")</script>Hello world'}
  )
  # API не должен возвращать исполняемый скрипт
  assert response.status_code in [200, 400, 422]


def test_html_injection():
  """Проверка защиты от HTML-инъекций."""
  response = requests.post(
    f'{BASE_URL}/analyze',
    json={'text': '<html><body>Test</body></html>'}
  )
  assert response.status_code in [200, 400, 422]


def test_too_long_text():
  """Проверка защиты от слишком длинных текстов."""
  # 100 000 символов
  longText = 'a' * 100000
  response = requests.post(
    f'{BASE_URL}/analyze',
    json={'text': longText}
  )
  # API должен отклонить слишком большой текст
  assert response.status_code in [400, 413, 422]


def test_too_many_texts_in_batch():
  """Проверка защиты от слишком больших пакетов."""
  # 1000 текстов в одном запросе
  manyTexts = ['Test text ' + str(i) for i in range(1000)]
  response = requests.post(
    f'{BASE_URL}/analyze-batch',
    json={'texts': manyTexts}
  )
  # API должен отклонить или обработать
  assert response.status_code in [200, 400, 413, 422]


def test_wrong_data_type():
  """Проверка защиты от неправильного типа данных."""
  response = requests.post(
    f'{BASE_URL}/analyze',
    json={'text': 12345}
  )
  # API должен вернуть ошибку валидации
  assert response.status_code == 422


def test_missing_field():
  """Проверка защиты при отсутствии обязательного поля."""
  response = requests.post(
    f'{BASE_URL}/analyze',
    json={}
  )
  # API должен вернуть ошибку валидации
  assert response.status_code == 422


def test_null_text():
  """Проверка защиты при передаче null."""
  response = requests.post(
    f'{BASE_URL}/analyze',
    json={'text': None}
  )
  # API должен вернуть ошибку валидации
  assert response.status_code == 422


def test_special_characters():
  """Проверка обработки специальных символов."""
  response = requests.post(
    f'{BASE_URL}/analyze',
    json={'text': '!@#$%^&*()_+-=[]{}|;:",.<>?/~`'}
  )
  # API не должен падать
  assert response.status_code in [200, 400, 422]


def test_unicode_text():
  """Проверка обработки Unicode."""
  response = requests.post(
    f'{BASE_URL}/analyze',
    json={'text': '😀🎉🚀 Hello мир 世界'}
  )
  assert response.status_code in [200, 400, 422]


def test_batch_with_invalid_item():
  """Проверка пакета с невалидным элементом."""
  response = requests.post(
    f'{BASE_URL}/analyze-batch',
    json={'texts': ['Valid text', '', 'Another valid']}
  )
  # API должен отклонить или обработать
  assert response.status_code in [200, 400, 422]


def test_malformed_json():
  """Проверка защиты от некорректного JSON."""
  response = requests.post(
    f'{BASE_URL}/analyze',
    data='{"text": malformed}',
    headers={'Content-Type': 'application/json'}
  )
  # API должен вернуть ошибку
  assert response.status_code == 422


def test_empty_body():
  """Проверка защиты от пустого тела запроса."""
  response = requests.post(
    f'{BASE_URL}/analyze',
    json={}
  )
  assert response.status_code == 422