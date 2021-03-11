from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import UnmappedInstanceError
from datetime import date

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nelot:12345@localhost:5432/netol_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Advertisement(db.Model):
    advert_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    owner = db.Column(db.String(40))
    created_at = db.Column(db.Date, default=date.today())

    def __repr__(self):
        return f'\n№{self.advert_id}:{self.owner}({self.created_at})-{self.description}'


@app.route("/", methods=["GET"])
def get():
    advertisements = Advertisement.query.all()
    return f'Объявления {[adv for adv in advertisements]}'


@app.route("/", methods=["POST"])
def create():
    if request.method == "POST":
        try:
            data = request.get_json()
            advertisement = Advertisement(description=data['text'], owner=data['owner'])
            db.session.add(advertisement)
            db.session.commit()
            return f"Создано объявление - {advertisement}"
        except KeyError:
            db.session.rollback()
            return f"Ошибка создания объявления"


@app.route("/<int:pk>", methods=["DELETE"])
def delete(pk):
    try:
        advertisement = Advertisement.query.get(pk)
        db.session.delete(advertisement)
        db.session.commit()
        return f"Удалено объявление -{advertisement}"
    except UnmappedInstanceError:
        return f'Объявления с номером "{pk}" не существует'


if __name__ == '__main__':
    app.run(debug=True)
