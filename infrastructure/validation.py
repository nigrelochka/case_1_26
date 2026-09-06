import re


def validateText(text: str) -> str:
  if not isinstance(text, str):
    raise TypeError('Text must be a string')

  text = text.strip()

  if not text:
    raise ValueError('Text must not be empty')

  if not re.search(r'[^\W\d_]', text, re.UNICODE):
    raise ValueError('Text must contain letters')

  return text