from domain.types import Language, Text_Stats


def fleschIndex(stats: Text_Stats, language: Language) -> float:
  if language == Language.EN:
    return (
      206.835 - 1.015 * stats.avgSentenceLength
      - 84.6 * stats.avgWordSyllables
    )

  if language == Language.RU:
    return (
      206.835 - 1.3 * stats.avgSentenceLength
      - 60.1 * stats.avgWordSyllables
    )

  if language == Language.DE:
    return (
      180 - stats.avgSentenceLength
      - 58.5 * stats.avgWordSyllables
    )

  if language == Language.FR:
    return (
      207 - 1.015 * stats.avgSentenceLength
      - 73.6 * stats.avgWordSyllables
    )

  raise ValueError('Unsupported language')


def fleschKincaid(stats: Text_Stats) -> float:
  return (
    0.39 * stats.avgSentenceLength
    + 11.8 * stats.avgWordSyllables - 15.59
  )


def interpretFlesch(score: float) -> str:
  if score >= 90:
    return 'Очень легко'

  if score >= 80:
    return 'Легко'

  if score >= 70:
    return 'Довольно легко'

  if score >= 60:
    return 'Средняя сложность'

  if score >= 50:
    return 'Довольно трудно'

  if score >= 30:
    return 'Трудно'

  return 'Очень трудно'