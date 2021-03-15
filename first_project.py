from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import UnmappedInstanceError
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nelot:12345@localhost:5432/netol_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(150))
    created_at = db.Column(db.Date, default=date.today())
    advertisement = db.relationship('Advertisement', backref='user', uselist=False)

    def __repr__(self):
        return f'№{self.user_id}:{self.email}'


class Advertisement(db.Model):
    advert_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    owner = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    created_at = db.Column(db.Date, default=date.today())

    def __repr__(self):
        return f'\n№{self.advert_id}:{self.user.name}({self.created_at})-{self.description}'


@app.route("/advertisements", methods=["GET"])
def get():
    advertisements = Advertisement.query.all()
    return f'Объявления {[adv for adv in advertisements]}'


@app.route("/advertisements", methods=["POST"])
def create():
    if request.method == "POST":
        try:
            request_data = request.get_json()
            auth = dict(request.headers)['Authorization'].split()
            user = User.query.filter_by(email=auth[0]).first()
            if user is None:
                return f'Такого пользователя не существует'
            if check_password_hash(user.password, auth[1]):
                advertisement = Advertisement(description=request_data['text'], owner=user.user_id)
                db.session.add(advertisement)
                db.session.commit()
                return f"Создано объявление - {advertisement}"
            else:
                return f'Введены неверные данные'
        except KeyError:
            db.session.rollback()
            return f"Ошибка создания объявления"


@app.route("/advertisements/<int:pk>", methods=["DELETE"])
def delete(pk):
    try:
        advertisement = Advertisement.query.get(pk)
        db.session.delete(advertisement)
        db.session.commit()
        return f"Удалено объявление -{advertisement}"
    except UnmappedInstanceError:
        return f'Объявления с номером "{pk}" не существует'


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            request_data = request.get_json()
            # тут когда-нибудь нужно добавить проверку введенных данных
            password_hash = generate_password_hash(request_data["password"])
            user = User(name=request_data["name"], email=request_data["email"], password=password_hash)
            db.session.add(user)
            db.session.commit()
            return f'Пользователь {user} зарегистрирован'
        except KeyError:
            return f'Введены неверные данные'


if __name__ == '__main__':
    app.run(debug=True)
