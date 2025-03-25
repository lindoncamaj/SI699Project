from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import requests
from rec_system import recommend
from marketcheck import check

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='/')
cors = CORS(app, origins='*')

CAR_API = "https://carapi.app/api/makes"

user = "admin"
pin = "si699matchmycar"
host = "database2.cyjek8guse5h.us-east-1.rds.amazonaws.com"
db_name = "car_database"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{user}:{pin}@{host}/{db_name}"
db = SQLAlchemy(app)

class Car_Make(db.Model):
    __tablename__ = "Car_Make"
    make_id = db.Column(db.Integer, primary_key=True)
    make_name = db.Column(db.String(50), nullable=False)

class Car_Model(db.Model):
    __tablename__ = 'Car_Model'
    model_id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(50), nullable=False)

class Car_Trim(db.Model):
    __tablename__ = 'Car_Trim'
    trim_id = db.Column(db.Integer, primary_key=True)
    trim_name = db.Column(db.String(100), nullable=False)
    # trim_description = db.Column(db.String(255))

class Car_Image(db.Model):
    __tablename__ = "Car_Image"
    image_id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=False)

class Car(db.Model):
    __tablename__ = "Car"
    car_id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('Car_Model.model_id'), nullable=False)
    make_id = db.Column(db.Integer, db.ForeignKey('Car_Make.make_id'), nullable=False)
    trim_id = db.Column(db.Integer, db.ForeignKey("Car_Trim.trim_id"), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey("Car_Image.image_id"), nullable=False)
    car_year = db.Column(db.Integer, nullable=False)
    car_msrp = db.Column(db.DECIMAL(10, 2), nullable=False)
    car_min_price = db.Column(db.DECIMAL(10, 2))
    car_med_price = db.Column(db.DECIMAL(10, 2))
    car_expert_score = db.Column(db.DECIMAL(10, 2))
    car_consumer_score = db.Column(db.DECIMAL(10, 2))

@app.route("/recommend", methods=['POST'])
def recommend_cars():
    data = request.get_json()

    min_price = data.get("minPrice")
    max_price = data.get("maxPrice")
    location = data.get("location")
    c_type = data.get("carType")
    c_make = data.get("carMake")

    result = recommend(min_price, max_price, location, c_type, c_make)
    m = db.session.execute(db.select(Car).where(Car.car_id.in_(result))).scalars().all()
    n = {}

    for i in range(10):
        make = db.session.execute(db.select(Car_Make).where(Car_Make.make_id == m[i].make_id)).scalar()
        model = db.session.execute(db.select(Car_Model).where(Car_Model.model_id == m[i].model_id)).scalar()
        image = db.session.execute(db.select(Car_Image).where(Car_Image.image_id == m[i].image_id)).scalar()

        n["item"+str(i + 1)] = {"year": m[i].car_year, "make": make.make_name, "model": model.model_name, "image": image.image_url}

    return n

@app.route("/lists", methods=["POST"])
def get_listings():
    data = request.get_json()

    make = data.get("make")
    model = data.get("model")
    year = data.get("year")

    result = check(make, model, year)

    return result

@app.route("/api/makes", methods=["GET"])
def makes():
    try:
        response = requests.get(CAR_API)
        makes = response.json()
        return jsonify(makes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def serve():
   return app.send_static_file("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=8080)
