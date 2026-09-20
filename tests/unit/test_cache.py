import json
from unittest.mock import Mock, patch, MagicMock


def test_cache_service_init():
  """Проверка создания сервиса кэша."""
  from infrastructure.cache import Cache_Service

  with patch('infrastructure.cache.redis.Redis') as mockRedis:
    mockInstance = Mock()
    mockInstance.ping.return_value = True
    mockRedis.return_value = mockInstance

    cache = Cache_Service()
    assert cache.ttl == 3600


def test_get_key():
  """Проверка генерации ключа."""
  from infrastructure.cache import Cache_Service

  with patch('infrastructure.cache.redis.Redis') as mockRedis:
    mockInstance = Mock()
    mockInstance.ping.return_value = True
    mockRedis.return_value = mockInstance

    cache = Cache_Service()
    key1 = cache._getKey('hello')
    key2 = cache._getKey('hello')
    key3 = cache._getKey('world')

    assert key1 == key2
    assert key1 != key3
    assert key1.startswith('analysis:')


def test_get_cached_result_none():
  """Проверка получения из кэша при отсутствии данных."""
  from infrastructure.cache import Cache_Service

  with patch('infrastructure.cache.redis.Redis') as mockRedis:
    mockInstance = Mock()
    mockInstance.ping.return_value = True
    mockInstance.get.return_value = None
    mockRedis.return_value = mockInstance

    cache = Cache_Service()
    result = cache.getCachedResult('test text')
    assert result is None


def test_get_cached_result_found():
  """Проверка получения из кэша при наличии данных."""
  from infrastructure.cache import Cache_Service

  with patch('infrastructure.cache.redis.Redis') as mockRedis:
    mockInstance = Mock()
    mockInstance.ping.return_value = True

    # Мокаем ответ Redis
    fakeData = {
      'language': 'en',
      'fleschIndex': 90.0,
      'fleschKincaid': 5.0,
      'interpretation': 'Легко',
      'polarity': 'neutral',
      'subjectivity': 0.0,
      'lexicalDiversity': 1.0,
      'rareWordDensity': 0.0,
      'stats': {
        'sentenceCount': 1,
        'wordCount': 2,
        'syllableCount': 2,
        'avgSentenceLength': 2.0,
        'avgWordSyllables': 1.0
      }
    }
    mockInstance.get.return_value = json.dumps(fakeData).encode()
    mockRedis.return_value = mockInstance

    cache = Cache_Service()
    result = cache.getCachedResult('test text')

    assert result is not None
    assert result.language == 'en'
    assert result.fleschIndex == 90.0


def test_set_cached_result():
  """Проверка сохранения в кэш."""
  from infrastructure.cache import Cache_Service

  with patch('infrastructure.cache.redis.Redis') as mockRedis:
    mockInstance = Mock()
    mockInstance.ping.return_value = True
    mockRedis.return_value = mockInstance

    cache = Cache_Service()

    # Создаём фиктивный результат
    mockResult = Mock()
    mockResult.dict.return_value = {'test': 'data'}

    result = cache.setCachedResult('test text', mockResult)

    assert result == True
    mockInstance.setex.assert_called_once()


def test_cache_no_redis_connection():
  """Проверка поведения при отсутствии Redis."""
  from infrastructure.cache import Cache_Service

  with patch('infrastructure.cache.redis.Redis') as mockRedis:
    mockInstance = Mock()
    mockInstance.ping.side_effect = Exception('Connection failed')
    mockRedis.return_value = mockInstance

    cache = Cache_Service()

    # При отсутствии Redis должен вернуть None
    assert cache.getCachedResult('test') is None
    assert cache.setCachedResult('test', Mock()) == False