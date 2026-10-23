# Стайлгайд документации ЕГЭРывка

Учебный проект для лабораторной работы № 3 по дисциплине «Проектная документация».
Объект — документация существующего проекта `egorr-gubanov/ege_jerk`.
Это отдельное руководство: исходное приложение не изменялось.

## Что подготовлено

- Правила языка, терминологии, структуры, Markdown и оформления примеров.
- Два образца документов и протокол проверки правил.
- MkDocs, линтинг и workflow проверки с публикацией в GitHub Pages.
- Инструкция для участников в [CONTRIBUTING.md](CONTRIBUTING.md).
- Отдельная ветка `codex/accessibility` для раздела доступности.

Архив сохраняет скрытую папку `.git` с локальной историей и обеими ветками.
После распаковки выполняйте команды в папке `style-guide-project`.

## Локальный запуск

Нужен Python 3.12. Создайте окружение в корне этого репозитория.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/check.py
python -m mkdocs serve
```

В Windows вместо `source` выполните `.venv\Scripts\Activate.ps1` в PowerShell.
Откройте адрес из вывода MkDocs, обычно `http://127.0.0.1:8000/`.
Остановите сервер сочетанием Ctrl+C.

## Публикация и ревью

- [Сайт руководства](https://egorr-gubanov.github.io/style-guide-project/).
- [Репозиторий](https://github.com/egorr-gubanov/style-guide-project).
- [Проверки и публикация](https://github.com/egorr-gubanov/style-guide-project/actions).

Раздел доступности находится в ветке `codex/accessibility` и предлагается через PR.
Обмен ревью, исправления по замечаниям, одобрение и слияние выполняются позже.
Последовательность приведена в [инструкции завершения](SUBMISSION.md).
