from locust import HttpUser, task, between


class TextAnalyzerUser(HttpUser):
    """Пользователь, который тестирует API анализа текста."""

    wait_time = between(1, 3)

    @task(3)
    def analyze_short_text(self):
        """Анализ короткого текста."""
        self.client.post(
            '/analyze',
            json={'text': 'Hello world! This is a short test.'}
        )

    @task(2)
    def analyze_medium_text(self):
        """Анализ среднего текста."""
        text = 'This is a medium text for testing. ' * 10
        self.client.post(
            '/analyze',
            json={'text': text}
        )

    @task(1)
    def analyze_long_text(self):
        """Анализ длинного текста."""
        text = 'This is a long text for performance testing. ' * 50
        self.client.post(
            '/analyze',
            json={'text': text}
        )

    @task(1)
    def analyze_batch(self):
        """Пакетная обработка."""
        self.client.post(
            '/analyze-batch',
            json={
                'texts': [
                    'First text for batch.',
                    'Second text for batch.',
                    'Third text for batch.'
                ]
            }
        )

    @task(1)
    def health_check(self):
        """Проверка /health."""
        self.client.get('/health')