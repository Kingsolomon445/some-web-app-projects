from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
    Bootstrap(app)
    return app


app = create_app()
db = SQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# with app.app_context():
#     db.create_all()


@app.route("/")
def home():
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    locations = [cafe.location for cafe in cafes]
    location = request.args.get("location")
    wifi = request.args.get("wifi")
    toilet = request.args.get("toilet")
    socket = request.args.get("socket")

    # Filter cafe-results based on selected values in the form
    if location:
        cafes = [cafe for cafe in cafes if cafe.location == location]
    if wifi:
        cafes = [cafe for cafe in cafes if cafe.has_wifi == (wifi == "yes")]
    if toilet:
        cafes = [cafe for cafe in cafes if cafe.has_toilet == (toilet == "yes")]
    if socket:
        cafes = [cafe for cafe in cafes if cafe.has_sockets == (socket == "yes")]

    return render_template("index.html", cafes=cafes, locations=locations)


# API

# Get all cafe
@app.route("/cafes")
def all_cafe():
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    return jsonify({"cafes": [cafe.to_dict() for cafe in cafes]})


# Add new cafe
@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    api_key = request.args.get("api-key")
    #  In a real scenario keep api secret and implement a way for user to get api key in website
    if api_key == "kjh2467gfd9867jhgfd098gfd65432":
        new_cafe = Cafe(
            name=request.args.get("name"),
            map_url=request.args.get("map_url"),
            img_url=request.args.get("img_url"),
            location=request.args.get("location"),
            has_sockets=bool(request.args.get("has_sockets")),
            has_toilet=bool(request.args.get("has_toilet")),
            has_wifi=bool(request.args.get("has_wifi")),
            can_take_calls=bool(request.args.get("can_take_calls")),
            seats=request.args.get("seats"),
            coffee_price=request.args.get("coffee_price"),
        )
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(
            {
                "response": {
                    "success": "Successfully added the new cafe."
                }
            }
        )
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403


# search for a cafe by location
@app.route("/search")
def search_cafe():
    location = request.args.get("location")
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    res = [cafe.to_dict() for cafe in cafes if cafe.location == location]
    if res:
        return jsonify({"cafes": res})
    else:
        return jsonify({"error": {
            "Not Found": "Sorry, we don't have a cafe at that location."
        }})


# update coffee price
@app.route('/update-price/<int:cafe_id>', methods=['PATCH'])
def update_coffee_price(cafe_id):
    api_key = request.args.get("api-key")
    if api_key == "kjh2467gfd9867jhgfd098gfd65432":
        coffee_price = request.args.get("new_price")
        if coffee_price:
            cafe = Cafe.query.filter_by(id=cafe_id).first()
            if cafe:
                cafe.coffee_price = coffee_price
                db.session.commit()
                return jsonify({"success": "Successfully updated the price."})
            else:
                return jsonify({"error": "Cafe not found."}), 404
        else:
            return jsonify({"error": "Missing new_price parameter."}), 400
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403


# delete cafe
@app.route('/delete/<cafe_id>', methods=['DELETE'])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")
    #  In a real scenario keep api secret and implement a way for user to get api key in website
    if api_key == "kjh2467gfd9867jhgfd098gfd65432":
        cafe = Cafe.query.filter_by(id=cafe_id).first()
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
        else:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403


if __name__ == '__main__':
    app.run(debug=True)
