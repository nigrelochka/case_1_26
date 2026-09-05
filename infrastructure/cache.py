import hashlib
import json
import logging
from typing import Optional

import redis

from interfaces.schemas import Analysis_Result


logger = logging.getLogger(__name__)


class Cache_Service:
  """Сервис для работы с Redis кэшем."""

  def __init__(
      self,
      redisHost: str = 'localhost',
      redisPort: int = 6379,
      redisDb: int = 0,
      ttl: int = 3600
  ):
    """Инициализирует подключение к Redis."""
    self.ttl = ttl

    try:
      self.redis = redis.Redis(
        host=redisHost,
        port=redisPort,
        db=redisDb,
        decode_responses=True,
        socket_connect_timeout=2
      )

      # Проверяем подключение.
      self.redis.ping()
      logger.info(
        f'Подключение к Redis успешно: {redisHost}:{redisPort}'
      )

    except Exception as e:
      logger.error(f'Не удалось подключиться к Redis: {e}')
      self.redis = None

  def _getKey(self, text: str) -> str:
    """Генерирует уникальный ключ для текста."""
    # Хешируем текст, чтобы получить короткий ключ.
    textHash = hashlib.md5(text.encode('utf-8')).hexdigest()
    return f'analysis:{textHash}'

  def getCachedResult(
      self,
      text: str
  ) -> Optional[Analysis_Result]:
    """Получает результат анализа из кэша."""
    if not self.redis:
      return None

    try:
      key = self.getKey(text)
      cached = self.redis.get(key)

      if cached:
        # Превращаем JSON обратно в объект.
        data = json.loads(cached)
        logger.info(f'Найдено в кэше: {key[:20]}...')
        return Analysis_Result(**data)

      logger.info(f'В кэше нет: {key[:20]}...')
      return None

    except Exception as e:
      logger.error(f'Ошибка при чтении из кэша: {e}')
      return None

  def setCachedResult(
      self,
      text: str,
      result: Analysis_Result
  ) -> bool:
    """Сохраняет результат анализа в кэш."""
    if not self.redis:
      return False

    try:
      key = self.getKey(text)

      # Превращаем результат в JSON-строку.
      value = json.dumps(
        result.dict(),
        ensure_ascii = False,
        default = str
      )

      # Сохраняем в Redis с TTL.
      self.redis.setex(key, self.ttl, value)
      logger.info(
        f'Сохранено в кэш: {key[:20]}... (TTL: {self.ttl}с)'
      )
      return True

    except Exception as e:
      logger.error(f'Ошибка при сохранении в кэш: {e}')
      return False

  def clearCache(self, text: Optional[str] = None) -> bool:
    """Очищает кэш для одного текста или полностью."""
    if not self.redis:
      return False

    try:
      if text:
        key = self.getKey(text)
        self.redis.delete(key)
        logger.info(f'Удален из кэша: {key[:20]}...')
      else:
        self.redis.flushdb()
        logger.info('Весь кэш очищен')

      return True

    except Exception as e:
      logger.error(f'Ошибка при очистке кэша: {e}')
      return False

  def getStats(self) -> dict:
    """Получает статистику кэша."""
    if not self.redis:
      return {'status': 'not_connected'}

    try:
      keys = self.redis.keys('analysis:*')

      return {
        'status': 'connected',
        'totalKeys': len(keys),
        'ttl': self.ttl
      }

    except Exception as e:
      return {
        'status': 'error',
        'message': str(e)
      }