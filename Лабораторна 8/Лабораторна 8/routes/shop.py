from flask import Blueprint, jsonify, render_template, request, redirect, url_for, session
from datetime import datetime
from models import Feedback, db, Order, Product, Client, OrderItem

shop_bp = Blueprint("shop", __name__)

# 🔹 Кошик
@shop_bp.route("/cart")
def view_cart():
    cart = session.get("cart", [])
    total = sum(item.get("price", 0) * item.get("quantity", 1) for item in cart)
    return render_template("cart.html", cart=cart, total=total)

# 🔹 API: Відгуки
@shop_bp.route("/api/feedback", methods=["GET", "POST"])
def api_feedback():
    if request.method == "GET":
        feedback = Feedback.query.all()
        return jsonify([{
            "id": f.id,
            "name": f.name,
            "email": f.email,
            "message": f.message
        } for f in feedback])

    if request.method == "POST":
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        if not name or not email or not message:
            return jsonify({"error": "Всі поля обов’язкові"}), 400

        fb = Feedback(name=name, email=email, message=message)
        db.session.add(fb)
        db.session.commit()
        return jsonify({"success": True, "id": fb.id}), 201


# 🔹 Видалення відгуку
@shop_bp.route("/api/feedback/<int:feedback_id>", methods=["DELETE"])
def delete_feedback(feedback_id):
    fb = Feedback.query.get_or_404(feedback_id)
    db.session.delete(fb)
    db.session.commit()
    return jsonify({"success": True})

# 🔹 API: Продукти
@shop_bp.route("/api/products")
def api_products():
    products = Product.query.all()
    return jsonify({
        "products": [
            {
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "image_url": p.image_url
            } for p in products
        ]
    })

# 🔹 Очистити кошик
@shop_bp.route("/clear_cart", methods=["POST"])
def clear_cart():
    session["cart"] = []
    return redirect(url_for("shop.view_cart"))

# 🔹 Додати товар у кошик
@shop_bp.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart = session.get("cart", [])

    # перевірка на дублікати
    for item in cart:
        if item["id"] == product.id:
            item["quantity"] += 1
            break
    else:
        cart.append({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": 1
        })

    session["cart"] = cart
    return redirect(url_for("shop.shop"))

# 🔹 Магазин
@shop_bp.route("/shop")
def shop():
    products = Product.query.all()
    return render_template("shop.html", products=products)

@shop_bp.route("/order/<int:order_id>")
def user_order_details(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template("order_details.html", order=order)

# 🔹 Оформлення замовлення
@shop_bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        # Дані з форми
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")
        cart = session.get("cart", [])

        # Перевірка
        if not name or not email or not phone or not address or not cart:
            return render_template("checkout.html", error="Заповніть всі поля та додайте товари до кошика")

        # Клієнт
        client = Client.query.filter_by(email=email).first()
        if not client:
            client = Client(name=name, email=email, phone=phone, address=address)
            db.session.add(client)
            db.session.flush()

        # Загальна сума
        total_price = sum(item.get("price", 0) * item.get("quantity", 1) for item in cart)

        # Замовлення
        order = Order(
            client=client,
            total_price=total_price,
            status="нове",
            date=datetime.now().strftime("%Y-%m-%d %H:%M")
        )

        # Товари у замовленні
        for item in cart:
            product = Product.query.get(item["id"])
            if product:
                order_item = OrderItem(product=product, quantity=item.get("quantity", 1))
                order.items.append(order_item)

        db.session.add(order)
        db.session.commit()
        session["cart"] = []

        return redirect(url_for("shop.user_order_details", order_id=order.id))


    return render_template("checkout.html")
