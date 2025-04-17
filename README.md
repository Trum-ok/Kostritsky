# Kostritsky

> [!NOTE]
> Перед использованием стоит узнать сколько памяти занимает int.

## Необходимые переменные окружения
Все необходимые переменные окружения указаны в [.env.example](./.env.example) файле. По его подобию должен быть создан .env

## Запуск
### Docker
```bash
docker built -t kostritsky-app . && docker run kostritsky-app -d
```

### Без docker`а
> [!TIP]
> *Рекомендуется использовать [uv](https://docs.astral.sh/uv/)*

```bash
uv sync && uv run main.py
```

## Тесты
<img src="./_assets/no_tests.png" alt="нет тестов нет м..." width="200">

