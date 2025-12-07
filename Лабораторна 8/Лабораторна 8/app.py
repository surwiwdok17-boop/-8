import os
from flask import Flask, jsonify, render_template
from models import db, Product, Order, Feedback, Client
from routes import blueprints
from routes.demo import demo_bp
from routes.admin import admin_bp   # імпортуємо адмінку
from flasgger import Swagger
from routes.shop import shop_bp
from routes import api_bp
from dotenv import load_dotenv
from sqlalchemy import text

# Завантажуємо змінні з .env
load_dotenv()

DATABASE_PATH = os.environ.get("DATABASE_PATH", "data/database.db")
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "your_secret_key")

swagger = Swagger(app)
db.init_app(app)

# Реєстрація blueprint'ів
app.register_blueprint(shop_bp, name='shop1')
app.register_blueprint(demo_bp)
app.register_blueprint(admin_bp)   # реєструємо адмінку окремо
for bp in blueprints:
    if bp.name != "admin":         # уникаємо повторної реєстрації
        app.register_blueprint(bp)

# Healthcheck
@app.route('/health')
def health():
    try:
        db.session.execute(text('SELECT 1'))
        return {'status': 'healthy'}, 200
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500

with app.app_context():
    db.create_all()

# Обробка помилок
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not Found"}), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "Bad Request"}), 400

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Server Error"}), 500

# Картинки для головної сторінки
images = [
    "https://cloudy.kyiv.ua/image/cache/catalog/products/Rdini/Zhizha-NOVA-Red-Bull-Blue-Raspberry-Salt-30ml-65mg-870x1131.jpg",
    "https://uestore.in.ua/image/cache/catalog/doublerasp-600x600-900x900.jpg",
    "https://v7par.com.ua/image/cache/catalog/1212/disposablle/elfbarrr/geekbar/2022-09-08%2012.35.34-650x650.jpg",
    "https://vapehub.shop/image/cache/catalog/import_files/51/51785680820711edfc8700505687efca_b93a26048f6811edcd9600505687efca-600x600.jpg",
    "https://uestore.in.ua/image/cache/catalog/pineapplelemonade-600x600-900x900.jpg",
    "https://terra-vape.com.ua/image/cache/catalog/Chaser/Nova-salt-30ml/nova-salt-30ml-mango-peach-1000x1000.jpg",
    "https://v7par.org.ua/image/cache/catalog/1212/disposablle/elfbarrr/geekbar/2-650x650.jpg",
]
index = 0

@app.route('/')
def home():
    global index
    image_url = images[index]
    index = (index + 1) % len(images)
    return render_template('home.html', image_url=image_url)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if not Product.query.first():
            demo_products = [
                Product(name="Nova red bull", price=290, image_url="https://cloudy.kyiv.ua/image/cache/catalog/products/Rdini/Zhizha-NOVA-Red-Bull-Blue-Raspberry-Salt-30ml-65mg-870x1131.jpg"),
                Product(name="Nova spearmint", price=250, image_url="https://vapestore.com.ua/image/cache/webp/catalog/06012021/1NOVA/8-180x180.webp"),
                Product(name="Nova cranberry&mors", price=350, image_url="https://vapestore.com.ua/image/cache/webp/catalog/06012021/1NOVA/9-180x180.webp"),
                Product(name="Double grape", price=255, image_url="https://vapestore.com.ua/image/cache/webp/catalog/06012021/1NOVA/3-180x180.webp"),
                Product(name="Cola lemon", price=322, image_url="https://elfbar-ua.com.ua/image/cache/catalog/image_goods/nova/cola_lemon-700x700.jpg"),
                Product(name="Pinapple lemonade", price=242, image_url="https://vapestore.com.ua/image/cache/webp/catalog/06012021/1NOVA/6-180x180.webp"),
            ]
            db.session.add_all(demo_products)
            db.session.commit()
            print("✅ База заповнена демо‑товарами")
    app.run(debug=True)
