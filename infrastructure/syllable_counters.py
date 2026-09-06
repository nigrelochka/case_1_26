from domain.types import Language
from domain.interfaces import Syllable_Counter


def countSyllablesRu(word: str) -> int:
  vowels = 'аеёиоуыэюя'

  word = word.lower().strip()

  if not word:
    return 0

  count = 0

  for letter in word:
      if letter in vowels:
          count += 1

  return count


def countSyllablesEn(word: str) -> int:
  vowels = 'aeiouy'

  word = word.lower().strip()

  if not word:
      return 0

  count = 0
  previousWasVowel = False

  for letter in word:
      if letter in vowels:
          if not previousWasVowel:
              count += 1

          previousWasVowel = True
      else:
          previousWasVowel = False

  if word.endswith('e') and count > 1:
      count -= 1

  return max(count, 1)


def countSyllablesDe(word: str) -> int:
  vowels = 'aeiouyäöü'

  word = word.lower().strip()

  if not word:
      return 0

  count = 0
  previousWasVowel = False

  for letter in word:
      if letter in vowels:
          if not previousWasVowel:
              count += 1

          previousWasVowel = True
      else:
          previousWasVowel = False

  return max(count, 1)


def countSyllablesFr(word: str) -> int:
  vowels = 'aeiouyàâäéèêëîïôöùûüÿ'

  word = word.lower().strip()

  if not word:
      return 0

  count = 0
  previousWasVowel = False

  for letter in word:
      if letter in vowels:
          if not previousWasVowel:
              count += 1

          previousWasVowel = True
      else:
          previousWasVowel = False

  if word.endswith('e') and count > 1:
      count -= 1

  return max(count, 1)


def getSyllableCounter(language: Language) -> Syllable_Counter:
  if language == Language.RU:
      return countSyllablesRu

  if language == Language.EN:
      return countSyllablesEn

  if language == Language.DE:
      return countSyllablesDe

  if language == Language.FR:
      return countSyllablesFr

  raise ValueError('Unsupported language')