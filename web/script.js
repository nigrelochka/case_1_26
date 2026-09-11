const API_URL = 'http://127.0.0.1:8000';

const textInput = document.getElementById('textInput');
const analyzeButton = document.getElementById('analyzeButton');
const result = document.getElementById('result');

analyzeButton.addEventListener('click', async () => {
  // Получаем текст из поля ввода.
  const text = textInput.value;

  try {
    // Отправляем текст на сервер.
    const response = await fetch(`${API_URL}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        text: text
      })
    });

    // Получаем JSON-ответ от сервера.
    const data = await response.json();

    // Проверяем, вернул ли сервер ошибку.
    if (!response.ok) {
      result.innerHTML = `
        <p>Ошибка ${response.status}: ${data.message || 'Неизвестная ошибка'}</p>
      `;
      return;
    }

  const language = languageNames[data.result.language] || data.result.language;

  const cachedText = data.cached ? 'Да' : 'Нет';

  result.innerHTML = `
    <p>Язык: ${language}</p>
    <p>Индекс Флеша: ${data.result.fleschIndex}</p>
    <p>Индекс Флеша-Кинкейда: ${data.result.fleschKincaid}</p>
    <p>Сложность: ${data.result.interpretation}</p>
    <p>Тональность: ${data.result.polarity}</p>
    <p>Субъективность: ${data.result.subjectivity}</p>
    <p>Лексическое разнообразие: ${data.result.lexicalDiversity}</p>
    <p>Плотность редких слов: ${data.result.rareWordDensity}</p>

    <h3>Статистика</h3>

    <p>Количество предложений: ${data.result.stats.sentenceCount}</p>
    <p>Количество слов: ${data.result.stats.wordCount}</p>
    <p>Количество слогов: ${data.result.stats.syllableCount}</p>
    <p>Средняя длина предложения: ${data.result.stats.avgSentenceLength}</p>
    <p>Среднее количество слогов в слове: ${data.result.stats.avgWordSyllables}</p>

    <h3>Информация о запросе</h3>

    <p>Результат из кэша: ${cachedText}</p>
    <p>Время обработки: ${data.processingTime.toFixed(2)} сек.</p>
  `;
});