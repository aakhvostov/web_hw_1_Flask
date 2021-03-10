from flask import Flask, flash, redirect, url_for, request
from sqlalchemy.orm import sessionmaker
from datetime import date
from models import Advertisement, engine


Session = sessionmaker(bind=engine)
session = Session()

app = Flask('app')
app.config['SECRET_KEY'] = 'hgerg67486sre1g56fgv74we89fc4z1x23v41s6tg7w98fv4w16'


@app.route("/", methods=["GET"])
def get():
    advertisements = session.query(Advertisement).all()
    return f'Объявления = {[adv.description for adv in advertisements]}'


@app.route("/", methods=["POST"])
def create():
    today = date.today()
    data = request.get_json()
    advertisement = Advertisement(description=data['text'], owner=data['owner'], created_at=today)
    session.add(advertisement)
    session.commit()
    flash("Объявление добавлено")
    return f"Создано объявление - №{advertisement.advert_id}: {advertisement.description}"


@app.route("/<int:advert_id>", methods=["DELETE"])
def delete(advert_id):
    advertisement = session.query(Advertisement).filter_by(advert_id=advert_id).one()
    session.delete(advertisement)
    session.commit()
    flash("Объявление удалено")
    return f"Удалено объявление - №{advertisement.advert_id}: {advertisement.description}"


if __name__ == '__main__':
    app.run(debug=True)
