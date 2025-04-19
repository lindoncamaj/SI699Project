from flask import Flask, request, jsonify, session, redirect, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import requests
from rec_system import recommend
from marketcheck import check
import random

app = Flask(__name__)
cors = CORS(app, origins='*', supports_credentials=True)

user = "admin"
pin = "si699matchmycar"
host = "database-2.cyjek8guse5h.us-east-1.rds.amazonaws.com"
db_name = "car_database"
db2_name = "user_database"

app.config['SQLALCHEMY_BINDS'] = {
    'car_data': f"mysql+pymysql://{user}:{pin}@{host}/{db_name}",
    'user_data': f"mysql+pymysql://{user}:{pin}@{host}/{db2_name}"
}
app.config["SECRET_KEY"] = 'your_unique_secret_key'
db = SQLAlchemy(app)

class Car_Make(db.Model):
    __bind_key__ = 'car_data'
    __tablename__ = "Car_Make"
    make_id = db.Column(db.Integer, primary_key=True)
    make_name = db.Column(db.String(50), nullable=False)

class Car_Model(db.Model):
    __bind_key__ = 'car_data'
    __tablename__ = 'Car_Model'
    model_id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(50), nullable=False)

class Car_Trim(db.Model):
    __bind_key__ = 'car_data'
    __tablename__ = 'Car_Trim'
    trim_id = db.Column(db.Integer, primary_key=True)
    trim_name = db.Column(db.String(100), nullable=False)
    # trim_description = db.Column(db.String(255))

class Car_Image(db.Model):
    __bind_key__ = 'car_data'
    __tablename__ = "Car_Image"
    image_id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=False)

class Car_Drivetrain(db.Model):
    __bind_key__ = 'car_data'
    __tablename__ = "Car_Drivetrain"
    drivetrain_id = db.Column(db.Integer, primary_key=True)
    drivetrain_name = db.Column(db.String(16), nullable=False)

class Car_Fuel_Type(db.Model):
    __bind_key__ = 'car_data'
    __tablename__ = "Car_Fuel_Type"
    fuel_type_id = db.Column(db.Integer, primary_key=True)
    fuel_type_name = db.Column(db.String(32), nullable=False)

class Car(db.Model):
    __bind_key__ = 'car_data'
    __tablename__ = "Car"
    car_id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('Car_Model.model_id'), nullable=False)
    make_id = db.Column(db.Integer, db.ForeignKey('Car_Make.make_id'), nullable=False)
    trim_id = db.Column(db.Integer, db.ForeignKey("Car_Trim.trim_id"), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey("Car_Image.image_id"), nullable=False)
    drivetrain_id = db.Column(db.Integer, db.ForeignKey("Car_Drivetrain.drivetrain_id"), nullable=False)
    fuel_type_id = db.Column(db.Integer, db.ForeignKey("Car_Fuel_Type.fuel_type_id"), nullable=False)
    car_year = db.Column(db.Integer, nullable=False)
    car_min_price = db.Column(db.DECIMAL(10, 2))
    car_med_price = db.Column(db.DECIMAL(10, 2))
    car_expert_score = db.Column(db.DECIMAL(10, 2))
    car_consumer_score = db.Column(db.DECIMAL(10, 2))
    car_city_fuel_economy = db.Column(db.Integer)
    car_hwy_fuel_economy = db.Column(db.Integer)
    car_comb_fuel_economy = db.Column(db.Integer)

class User(db.Model):
    __bind_key__ = 'user_data'
    __tablename__ = "User"
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), unique=True, nullable=False)
    user_pass = db.Column(db.String(256), nullable=False)
    user_email = db.Column(db.String(), unique=True, nullable=False)
    user_fname = db.Column(db.String(100), nullable=False)
    user_lname = db.Column(db.String(100), nullable=False)
    user_date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

class User_Query(db.Model):
    __bind_key__ = 'user_data'
    __tablename__ = "User_Query"
    query_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    query_min_price = db.Column(db.Integer, nullable=False)
    query_max_price = db.Column(db.Integer, nullable=False)
    query_location = db.Column(db.Integer, nullable=False)
    query_car_type_sedan = db.Column(db.Boolean, nullable=False)
    query_car_type_suv = db.Column(db.Boolean, nullable=False)
    query_car_type_truck = db.Column(db.Boolean, nullable=False)
    query_car_make = db.Column(db.String(128), nullable=False)
    query_car_elec = db.Column(db.Boolean, nullable=False)
    query_car_gas = db.Column(db.Boolean, nullable=False)
    query_car_hybrid = db.Column(db.Boolean, nullable=False)
    query_car_mpg = db.Column(db.Integer)

class User_Selection(db.Model):
    __bind_key__ = 'user_data'
    __tablename__ = "User_Selection"
    selection_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    query_id = db.Column(db.Integer, db.ForeignKey('User_Query.query_id'), nullable=False)
    selection_rank = db.Column(db.Integer, nullable=False)
    selection_time = db.Column(db.DateTime, default=db.func.current_timestamp())


@app.route("/recommend", methods=['POST'])
def recommend_cars():
    data = request.get_json()

    min_price = data.get("minPrice")
    max_price = data.get("maxPrice")
    location = data.get("location")
    c_type = data.get("carType")
    sedan = c_type["sedan"]
    suv = c_type["suv"]
    truck = c_type["truck"]
    c_make = [int(car["value"]) for car in data.get("carMake")]
    c_year = int(data.get("carYear")["value"])
    elec = data.get("electric")["elec"]
    gas = data.get("electric")["gas"]
    hybrid = data.get("electric")["hybrid"]
    fwd = data.get("drivetrain")["fwd"]
    rwd = data.get("drivetrain")["rwd"]
    awd = data.get("drivetrain")["awd"]
    minMPG = data.get("minMPG")

    if "user_id" in session:
        new_query = User_Query(
            user_id=session["user_id"],
            query_min_price = min_price,
            query_max_price = max_price,
            query_location = location,
            query_car_type_sedan = sedan,
            query_car_type_suv = suv,
            query_car_type_truck = truck,
            query_car_make  = str(c_make),
            query_car_elec = elec,
            query_car_gas = gas,
            query_car_hybrid = hybrid,
            query_car_mpg = minMPG
        )
        db.session.add(new_query)
        db.session.commit()
        query_id = new_query.query_id
        print(query_id)
    else:
        print("no user in session")
        query_id = 0

    return recommend(min_price, max_price, c_make, c_year, elec, gas, hybrid, awd, fwd, rwd, minMPG, query_id, location)

@app.route("/lists", methods=["POST"])
def get_listings():
    data = request.get_json()

    q_id = data.get("query_id")
    s_rank = data.get("selection_rank").split("m")[1]
    make = data.get("make")
    model = data.get("model")
    year = data.get("year")
    location = data.get("zip")

    if int(q_id) == 0:
        pass
    else:
        new_query = User_Selection(
            user_id=int(session["user_id"]),
            query_id=int(q_id),
            selection_rank=int(s_rank)
        )
        db.session.add(new_query)
        db.session.commit()

    result = check(make, model, year, location)

    return result


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("user_name")
    password = data.get("user_pass")
    email = data.get("user_email")
    fname = data.get("user_fname")
    lname = data.get("user_lname")

    try:
        new_user = User(user_name=username, user_pass=password, user_email=email, user_fname=fname, user_lname=lname)
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User Created"}
    except Exception as e:
        # (pymysql.err.IntegrityError) (1062, "Duplicate entry 'lindonc' for key 'User.user_name'")
        # [SQL: INSERT INTO `User` (user_name, user_pass, user_email, user_fname, user_lname, user_date_created) VALUES (%(user_name)s, %(user_pass)s, %(user_email)s, %(user_fname)s, %(user_lname)s, CURRENT_TIMESTAMP)]
        # [parameters: {'user_name': 'lindonc', 'user_pass': 'test', 'user_email': 'lindonc@test.com', 'user_fname': 'Lindon', 'user_lname': 'Camaj'}]
        # (Background on this error at: https://sqlalche.me/e/20/gkpj)
        print(e)
        return {"message": "User Already Exists"}


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("user_name")
    password = data.get("user_pass")

    user_info = db.session.execute(db.select(User).where(User.user_name == username)).scalar()

    if user_info and user_info.user_pass == password:
        session["user_id"] = user_info.user_id
        print(session)
        return {"message": "Successfully Logged-in"}
    else:
        return {"message": "Invalid username or password."}

@app.route("/logout", methods=["POST"])
def logout():
    session.pop('user_id', None)
    return {}

@app.route("/profile", methods=["GET"])
def get_profile_info():
    if "user_id" not in session:
        return jsonify({"message": "Not logged in"}), 401

    user = db.session.get(User, session["user_id"])
    if user:
        user_queries = db.session.execute(db.select(User_Query).where(User_Query.user_id == session["user_id"])).scalars()
        for q in user_queries:
            print(q)
        if user_queries:
            return jsonify({
                "user_name": user.user_name,
                "user_email": user.user_email,
                "user_fname": user.user_fname,
                "user_lname": user.user_lname
            })
        else:
            return jsonify({
                "user_name": user.user_name,
                "user_email": user.user_email,
                "user_fname": user.user_fname,
                "user_lname": user.user_lname
            })
    return jsonify({"message": "User not found"}), 404

@app.route("/edit-profile", methods=["GET"])
def get_profile():
    if "user_id" not in session:
        return jsonify({"message": "Not logged in"}), 401

    user = db.session.get(User, session["user_id"])
    if user:
        return jsonify({
            "user_name": user.user_name,
            "user_email": user.user_email,
            "user_fname": user.user_fname,
            "user_lname": user.user_lname,
            "user_pass": user.user_pass
        })
    return jsonify({"message": "User not found"}), 404

@app.route("/edit-profile", methods=["POST"])
def update_profile():
    if "user_id" not in session:
        return jsonify({"message": "Not logged in"}), 401

    data = request.get_json()
    user = db.session.get(User, session["user_id"])

    if user:
        user.user_name = data.get("user_name", user.user_name)
        user.user_fname = data.get("user_fname", user.user_fname)
        user.user_lname = data.get("user_lname", user.user_lname)
        user.user_email = data.get("user_email", user.user_email)
        new_password = data.get("user_pass")

        if new_password:
            user.user_pass = new_password
        db.session.commit()
        return jsonify({"message": "Profile updated successfully"})

    return jsonify({"message": "User not found"}), 404

@app.route("/session", methods=["GET"])
def check_session():
    print(session)
    if "user_id" in session:
        print("login")
        return {"logged_in": True, "user_id": session["user_id"]}, 200
    print("logout")
    return {"logged_in": False}, 200

if __name__ == "__main__":
    app.run(debug=True, port=8080)
