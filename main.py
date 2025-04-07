from flask import *
import json
import os


from repository import Repository

app = Flask(__name__)

CONFIG_FILE = os.path.join("config", "settings.json")
DEFAULT_CONFIG = {
    "admin_key": "admin",
    "ai_key": ""
}

if not os.path.exists(CONFIG_FILE):
    print("Конфиг отсутствует, добавлен конфиг по умолчанию")
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_CONFIG, f, indent=4)
    print(f"Created default config: {CONFIG_FILE}")

# Читаем настройки
with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    config = json.load(f)
    ADMIN_KEY = config["admin_key"]
    AI_KEY = config["ai_key"]

# Инициализация репозитория
DATA_FILE = os.path.join("data", "messages.json")
repo = Repository(DATA_FILE, AI_KEY)

# Главная страница
@app.route("/")
def index():
    messages = repo.load_messages()
    return render_template("index.html", messages=messages)

# Добавление отзыва
@app.route("/add", methods=["POST"])
def add_message():
    name = request.form.get("name")
    text = request.form.get("text")
    if name and text:
        repo.add_message(name, text)
    return redirect(url_for("index"))

# Страница входа
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("key") == ADMIN_KEY:
            resp = make_response(redirect(url_for("admin")))
            resp.set_cookie("auth_key", ADMIN_KEY, max_age=3600)
            return resp
        return render_template("login.html", error="Неверный ключ")
    return render_template("login.html")

# Админ-панель
@app.route("/admin")
def admin():
    if request.cookies.get("auth_key") != ADMIN_KEY:
        return redirect(url_for("login"))
    messages = repo.load_messages()
    return render_template("admin.html", messages=messages)

# Удаление отзыва
@app.route("/delete/<int:message_id>")
def delete_message(message_id):
    if request.cookies.get("auth_key") != ADMIN_KEY:
        return redirect(url_for("login"))
    repo.delete_message(message_id)
    return redirect(url_for("admin"))

if __name__ == "__main__":
    app.run(debug=True)