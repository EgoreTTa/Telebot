#!/usr/bin/env bash
set -e
echo "📦 переход в рабочую папку ${DEPLOY_DIR}..."
cd ${DEPLOY_DIR} || { echo "❌ Не удалось перейти в $DEPLOY_DIR"; exit 1; }

echo "export ... PIPENV_VENV_IN_PROJECT=${PIPENV_VENV_IN_PROJECT}"
export PIPENV_VENV_IN_PROJECT=${PIPENV_VENV_IN_PROJECT}

echo "📦 Установка зависимостей..."
pipenv install --deploy
pipenv install python-dotenv

echo "🔐 Запись токена в .env..."
echo "API_TOKEN=${API_TOKEN}" > .env

echo "✅ Деплой завершён успешно!"