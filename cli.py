import json, click, httpx


API_URL = 'http://127.0.0.1:8000'


@click.group()
def cli():
  # Создаём главную CLI-команду.
  pass


@cli.command()
@click.option('--text', type = str, help = 'Текст для анализа.')
@click.option('--file', 'filePath', type = click.Path(exists = True), help = 'Файл с текстом.')
@click.option('--batch-file', 'batchFilePath', type = click.Path(exists = True), help = 'Файл с несколькими текстами.')
def analyze(text, filePath, batchFilePath):
  # Выбираем способ получения текста.

  optionsCount = sum(value is not None for value in [text, filePath, batchFilePath])

  if optionsCount == 0:
    raise click.UsageError('Укажите --text, --file или --batch-file.')

  if optionsCount > 1:
    raise click.UsageError('Можно использовать только один из параметров.')

  if text is not None:
    sendTextToApi(text)
    return

  if filePath is not None:
    analyzeFile(filePath)
    return

  analyzeBatchFile(batchFilePath)


def sendTextToApi(text):
  # Отправляем один текст в API.

  response = httpx.post(
f'{API_URL}/analyze',
    json={'text': text},
    trust_env=False
  )

  showResponse(response)


def analyzeFile(filePath):
  # Читаем текст из файла и отправляем его в API.

  with open(filePath, 'r', encoding = 'utf-8') as file:
    text = file.read()

  sendTextToApi(text)


def analyzeBatchFile(filePath):
  # Читаем несколько текстов из файла и отправляем их в API.

  with open(filePath, 'r', encoding = 'utf-8') as file:
    texts = [line.strip() for line in file if line.strip()]

  response = httpx.post(
f'{API_URL}/analyze-batch',
    json={'texts': texts},
    trust_env=False
  )

  showResponse(response)


def showResponse(response):
  # Показываем ответ API пользователю.

  if response.status_code >= 400:
    click.echo(f'Ошибка {response.status_code}: {response.text}')
    return

  result = response.json()

  click.echo(
    json.dumps(
      result,
      ensure_ascii = False,
      indent = 2
    )
  )


if __name__ == '__main__':
  # Запускаем CLI.
  cli()