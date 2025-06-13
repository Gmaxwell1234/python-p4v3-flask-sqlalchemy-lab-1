from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route("/")
def index():
    return "<h1>Earthquake API</h1>"

@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    earthquake = db.session.get(Earthquake, id)
    
    if earthquake:
        return make_response(jsonify(earthquake.to_dict()), 200)
    else:
        return make_response(jsonify({"message": f"Earthquake {id} not found."}), 404)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_min_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    results = [e.to_dict() for e in earthquakes]
    
    return make_response(
        jsonify({
            "count": len(results),
            "quakes": results
        }),
        200
    )

if __name__ == "__main__":
    app.run(port=5555, debug=True)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
