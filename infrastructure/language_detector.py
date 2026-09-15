from langdetect import detect, DetectorFactory

from domain.types import Language


DetectorFactory.seed = 0


def detectLanguage(text: str) -> Language:
  detectedLanguage = detect(text)

  if detectedLanguage == 'ru':
    return Language.RU

  if detectedLanguage == 'en':
    return Language.EN

  if detectedLanguage == 'de':
    return Language.DE

  if detectedLanguage == 'fr':
    return Language.FR

  raise ValueError(
    f'Unsupported language: {detectedLanguage}'
  )