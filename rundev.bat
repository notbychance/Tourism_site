@echo off
REM Запуск Django сервера в новом окне
start "Django Server" cmd /k "cd backend && .venv\Scripts\activate && python manage.py runserver"

REM Запуск Vue.js dev сервера в новом окне
start "Vue.js Server" cmd /k "cd /d frontend && npm run dev"

REM Запуск нового терминала для git
start "Git Helper" cmd /k "echo Список полезных Git-команд: && echo. && echo git status - проверка изменений && echo git add . - добавить все файлы && echo git commit -m ""Сообщение"" - зафиксировать изменения && echo git push - отправить на сервер && echo git pull - получить обновления && echo. && echo Полный гайд: https://git-scm.com/docs"