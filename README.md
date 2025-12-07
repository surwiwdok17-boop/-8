# 8 Лабораторна робота

# Flask Shop App (Лабораторна 6–8)

## Опис
Це Flask‑додаток для інтернет‑магазину з:
- SQLite базою даних (через SQLAlchemy)
- Адмін‑панеллю (Flask‑Admin)
- Swagger документацією API (Flasgger)
- Docker‑контейнеризацією (Dockerfile + docker-compose.yml)
- Healthcheck для моніторингу стану

---

##  Встановлення

### 1. Клонування репозиторію
```bash
git clone <repo-url>
cd Лабораторна 6
2. Створення .venv
venv
DATABASE_PATH=/app/data/database.db
SECRET_KEY=your_secret_key
 Запуск у Docker
1. Збірка образу
bash
docker compose build
2. Запуск контейнера
bash
docker compose up -d
3. Перевірка логів
bash
docker compose logs -f web
Перевірка роботи
Головна сторінка: http://localhost:5000

Healthcheck: http://localhost:5000/health

Адмін‑панель: http://localhost:5000/admin

Swagger API: http://localhost:5000/apidocs

Структура
app.py — головний Flask‑додаток

models.py — моделі SQLAlchemy (Product, Order, Feedback, Client)

routes/ — маршрути (shop, demo, api, admin)

requirements.txt — залежності

Dockerfile — інструкції для збірки образу

docker-compose.yml — запуск сервісів

templates/ — HTML‑шаблони

static/ — статичні файли

Volume
База даних зберігається у volume:

yaml
volumes:
  sqlite_data:
Це гарантує збереження даних після перезапуску контейнера.

Що реалізовано
[x] Flask‑додаток з моделями

[x] SQLite база з volume

[x] Автоматичне створення директорії для бази

[x] Демо‑товари додаються при першому запуску

[x] Адмін‑панель для перегляду замовлень

[x] Swagger документація API

[x] Dockerfile з усіма залежностями

[x] docker-compose.yml  без version: (щоб не було попередження

)[x] Healthcheck для контейнер

Запуск локально (без Docker
)bas
hpython -m venv .ven
vsource .venv/bin/activate   # або .venv\Scripts\activate у Window
spip install -r requirements.tx
tpython app.p
y Використані технологі
їPython 3.1

1Flask 3.

1Flask‑SQLAlchemy 3.

0Flask‑Admin 1.

6Flasgger 0.

9Docker + Docker Compos

eКо

д--

-##  Перевірка
Так, ми зробили все необхідне
:-  `requirements.txt` очищений від дублікатів і містить всі потрібні пакети 
 -  `Dockerfile` правильний, з `build-essential` і `python3-dev` 
 -  `docker-compose.yml` без `version:` і з volume 
 -  `.env` використовується для `DATABASE_PATH` 
 -  `app.py` створює директорію для бази і додає демо‑товари
Висновок: закінчивши дану лабораторну роботу ми усвідомили що покащо не є хорошими програмістами але ми постараємося стати краще і дана лабораторна робота показує що ми ще можемо і хочемо стати краще. 
