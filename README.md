# SITERATE BACKEND

### Инструкиця по запуску
Соберите контейнер
```
docker build -t siterate-backend .
```
Запустите контейнер
```
docker run -d -p 8000:8000 --name siterate-app siterate-backend
```
Проверьте что процесс запустился
```
docker ps
```
Откройте сваггер по урлу http://localhost:8000/docs

Чтобы остановить контейнер введите ***docker stop {CONTAINER ID}***