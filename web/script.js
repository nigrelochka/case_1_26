const API_URL = 'http://127.0.0.1:8000';

const textInputs = document.getElementById('textInputs');
const addTextButton = document.getElementById('addTextButton');
const analyzeButton = document.getElementById('analyzeButton');
const result = document.getElementById('result');

const languageNames = {
  en: 'Английский',
  ru: 'Русский',
  de: 'Немецкий',
  fr: 'Французский'
};

addTextButton.addEventListener('click', () => {
  // Создаём новое поле для текста.
  const newTextInput = document.createElement('textarea');

  newTextInput.className = 'textInput';
  newTextInput.rows = 10;
  newTextInput.cols = 50;
  newTextInput.placeholder = 'Введите текст...';

  textInputs.appendChild(document.createElement('br'));
  textInputs.appendChild(newTextInput);
});

analyzeButton.addEventListener('click', async () => {
  // Получаем все поля с текстами.
  const inputs = document.querySelectorAll('.textInput');
  const texts = [];

  inputs.forEach((input) => {
    if (input.value.trim()) {
      texts.push(input.value);
    }
  });

  try {
    // Отправляем запрос на сервер.
    let response;

    if (texts.length === 1) {
      // Отправляем один текст.
      response = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          text: texts[0]
        })
      });
    } else {
      // Отправляем несколько текстов.
      response = await fetch(`${API_URL}/analyze-batch`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          texts: texts
        })
      });
    }

    // Получаем JSON-ответ от сервера.
    const data = await response.json();

    // Проверяем, вернул ли сервер ошибку.
    if (!response.ok) {
      result.innerHTML = `
        <p>Ошибка ${response.status}: ${data.message || data.detail || 'Неизвестная ошибка'}</p>
      `;
      return;
    }

    // Очищаем предыдущие результаты.
    result.innerHTML = '';

    if (texts.length === 1) {
      // Показываем результат одного текста.
      showResult(data.result, data.cached, result, data.processingTime);
    } else {
      // Показываем результаты всех текстов.
      data.results.forEach((analysisResult, index) => {
        const resultBlock = document.createElement('div');

        resultBlock.innerHTML = `<h3>Текст ${index + 1}</h3>`;

        result.appendChild(resultBlock);

        showResult(
          analysisResult,
          data.cached[index],
          resultBlock,
          data.totalTime
        );
      });
    }
  } catch (error) {
    // Показываем ошибку соединения с API.
    result.innerHTML = `
      <p>Ошибка соединения с API: ${error.message}</p>
    `;
  }
});

function showResult(analysisResult, cached, container = result, processingTime) {
  // Показываем данные анализа текста.
  const language = languageNames[analysisResult.language] || analysisResult.language;
  const cachedText = cached ? 'Да' : 'Нет';

  const resultBlock = document.createElement('div');

  resultBlock.innerHTML = `
    <p>Язык: ${language}</p>
    <p>Индекс Флеша: ${analysisResult.fleschIndex}</p>
    <p>Индекс Флеша-Кинкейда: ${analysisResult.fleschKincaid}</p>
    <p>Сложность: ${analysisResult.interpretation}</p>
    <p>Тональность: ${analysisResult.polarity}</p>
    <p>Субъективность: ${analysisResult.subjectivity}</p>
    <p>Лексическое разнообразие: ${analysisResult.lexicalDiversity}</p>
    <p>Плотность редких слов: ${analysisResult.rareWordDensity}</p>

    <h4>Статистика</h4>
    <p>Количество предложений: ${analysisResult.stats.sentenceCount}</p>
    <p>Количество слов: ${analysisResult.stats.wordCount}</p>
    <p>Количество слогов: ${analysisResult.stats.syllableCount}</p>
    <p>Средняя длина предложения: ${analysisResult.stats.avgSentenceLength}</p>
    <p>Среднее количество слогов в слове: ${analysisResult.stats.avgWordSyllables}</p>

    <h4>Информация о запросе</h4>
    <p>Результат из кэша: ${cachedText}</p>
    <p>Время обработки: ${processingTime.toFixed(2)} сек.</p>
  `;

  container.appendChild(resultBlock);
}