import pymysql
import pandas as pd
import numpy as np

def init_car_db(cur):
    cur.execute("DROP DATABASE IF EXISTS car_database;")
    cur.execute("CREATE DATABASE IF NOT EXISTS car_database;")

def create_car_tables(cur):
    table_queries = [
        """CREATE TABLE IF NOT EXISTS Car_Make (
            make_id INT PRIMARY KEY AUTO_INCREMENT,
            make_name VARCHAR(50) NOT NULL UNIQUE
        );""",

        """CREATE TABLE IF NOT EXISTS Car_Model (
            model_id INT PRIMARY KEY AUTO_INCREMENT,
            model_name VARCHAR(50) NOT NULL UNIQUE
        );""",

        """CREATE TABLE IF NOT EXISTS Car_Trim (
            trim_id INT PRIMARY KEY AUTO_INCREMENT,
            trim_name VARCHAR(100) NOT NULL UNIQUE
        );""",# trim_description VARCHAR(255)

        """CREATE TABLE IF NOT EXISTS Car_Image (
            image_id INT PRIMARY KEY AUTO_INCREMENT,
            image_url VARCHAR(255) NOT NULL UNIQUE
        );""",

        """CREATE TABLE IF NOT EXISTS Car_Drivetrain (
            drivetrain_id INT PRIMARY KEY AUTO_INCREMENT,
            drivetrain_name VARCHAR(16) NOT NULL UNIQUE
        )""",
        """CREATE TABLE IF NOT EXISTS Car_Fuel_Type (
            fuel_type_id INT PRIMARY KEY AUTO_INCREMENT,
            fuel_type_name VARCHAR(32) NOT NULL UNIQUE
        )""",

        """CREATE TABLE IF NOT EXISTS Car (
            car_id INT PRIMARY KEY AUTO_INCREMENT,
            make_id INT NOT NULL,
            model_id INT NOT NULL,
            trim_id INT NOT NULL,
            image_id INT NOT NULL,
            drivetrain_id INT NOT NULL,
            fuel_type_id INT NOT NULL,
            car_year INT NOT NULL,
            car_min_price DECIMAL(10,2),
            car_med_price DECIMAL(10,2),
            car_expert_score DECIMAL(10,2),
            car_consumer_score DECIMAL(10,2),
            car_city_fuel_economy INT,
            car_hwy_fuel_economy INT,
            car_comb_fuel_economy INT,

            FOREIGN KEY (make_id) REFERENCES Car_Make(make_id) ON DELETE CASCADE,
            FOREIGN KEY (model_id) REFERENCES Car_Model(model_id) ON DELETE CASCADE,
            FOREIGN KEY (trim_id) REFERENCES Car_Trim(trim_id) ON DELETE CASCADE,
            FOREIGN KEY (image_id) REFERENCES Car_Image(image_id) ON DELETE CASCADE,
            FOREIGN KEY (drivetrain_id) REFERENCES Car_Drivetrain(drivetrain_id) ON DELETE CASCADE,
            FOREIGN KEY (fuel_type_id) REFERENCES Car_Fuel_Type(fuel_type_id) ON DELETE CASCADE
        );""",
    ]

    for query in table_queries:
        cur.execute(query)

def insert_car_data(cur, car_data):
    make_insert_query = """INSERT INTO Car_Make (make_id, make_name) VALUES (%s, %s);"""
    model_insert_query = """INSERT INTO Car_Model (model_id, model_name) VALUES (%s, %s);"""
    trim_insert_query = """INSERT INTO Car_Trim (trim_id, trim_name) VALUES (%s, %s);"""
    image_insert_query = """INSERT INTO Car_Image (image_id, image_url) VALUES (%s, %s);"""
    drivetrain_insert_query = """INSERT INTO Car_Drivetrain (drivetrain_id, drivetrain_name) VALUES (%s, %s);"""
    fuel_type_insert_query = """INSERT INTO Car_Fuel_Type (fuel_type_id, fuel_type_name) VALUES (%s, %s);"""
    car_insert_query = """
        INSERT INTO Car (make_id, model_id, trim_id, image_id, drivetrain_id, fuel_type_id, car_year, car_min_price, car_med_price, car_expert_score, car_consumer_score, car_city_fuel_economy, car_hwy_fuel_economy, car_comb_fuel_economy)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    for _, row in car_data.iterrows():
        try:
            cursor.execute(make_insert_query, (row["make_id"], row["make"]))
        except:
            pass

        try:
            cursor.execute(model_insert_query, (row["model_id"], row["model"]))
        except:
            pass

        try:
            cursor.execute(trim_insert_query, (row["trim_id"], row["trim"]))
        except:
            pass

        try:
            cursor.execute(image_insert_query, (row["image_id"], row["image"]))
        except:
            pass

        try:
            cursor.execute(drivetrain_insert_query, (row["drivetrain_id"], row["drivetrain"]))
        except:
            pass

        try:
            cursor.execute(fuel_type_insert_query, (row["fuel_type_id"], row["fuel_type"]))
        except:
            pass

        try:
            cursor.execute(car_insert_query, (row["make_id"], row["model_id"], row["trim_id"], row["image_id"], row["drivetrain_id"], row["fuel_type_id"], row["year"], row["min_price"], row["med_price"], row["expert_score"], row["consumer_score"], row["city_fuel_economy"], row["hwy_fuel_economy"], row["comb_fuel_economy"]))
        except Exception as e:
            print(e)
            print(f"make id: {row['make_id']}")
            print(f"model id: {row['model_id']}")
            print(f"trim id: {row['trim_id']}")
            print(f"year: {row['year']}")
            print()

    print("done")


    # Insert data into Fuel_Economy Table (Now using correct column names)
    # fuel_insert_query = """
    #     INSERT IGNORE INTO Fuel_Economy (trim_id, mileage_epa_combined_mpg, mileage_epa_city_mpg, mileage_epa_highway_mpg)
    #     VALUES (%s, %s, %s, %s);
    # """
    # for _, row in car_data.iterrows():
    #     cursor.execute(fuel_insert_query, (
    #         row["trim_id"], row["mileage_combined_mpg"], row["mileage_epa_city_mpg"], row["mileage_epa_highway_mpg"]
    #     ))

    # Insert data into Electric_Vehicle Table (Only for Electric Vehicles)
    # ev_insert_query = """
    #     INSERT IGNORE INTO Electric_Vehicle (trim_id, range_electric, epa_kwh_100_mi, battery_capacity, charging_time_240v_hr)
    #     VALUES (%s, %s, %s, %s, %s);
    # """
    # ev_data = car_data[car_data["mileage_range_electric"].notnull()]
    # for _, row in ev_data.iterrows():
    #     cursor.execute(ev_insert_query, (
    #         row["trim_id"], row["mileage_range_electric"], row["mileage_epa_kwh_100_mi_electric"],
    #         row["mileage_battery_capacity_electric"], row["mileage_epa_time_to_charge_hr_240v_electric"]
    #     ))

    # Insert data into Safety_Rating Table
    # safety_insert_query = """INSERT IGNORE INTO Safety_Rating (trim_id, accident_safety_rating) VALUES (%s, %s);"""
    # for _, row in car_data.iterrows():
    #     cursor.execute(safety_insert_query, (row["trim_id"], row["accident_safety_rating"]))



def init_user_db(cur):
    """
    """
    cur.execute("DROP DATABASE IF EXISTS user_database;")
    cur.execute("CREATE DATABASE IF NOT EXISTS user_database;")

def create_user_tables(cur):
    """
    """
    table_queries = [
        """CREATE TABLE IF NOT EXISTS User (
            user_id INT PRIMARY KEY AUTO_INCREMENT,
            user_name VARCHAR(100) NOT NULL UNIQUE,
            user_pass VARCHAR(255) NOT NULL,
            user_email VARCHAR(100) NOT NULL UNIQUE,
            user_fname VARCHAR(100) NOT NULL,
            user_lname VARCHAR(100) NOT NULL,
            user_date_created DATETIME DEFAULT (NOW())
        );""",

        """CREATE TABLE IF NOT EXISTS User_Query (
            query_id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT NOT NULL,
            query_min_price INT NOT NULL,
            query_max_price INT NOT NULL,
            query_location INT NOT NULL,
            query_car_type_sedan BOOLEAN NOT NULL,
            query_car_type_suv BOOLEAN NOT NULL,
            query_car_type_truck BOOLEAN NOT NULL,
            query_car_make VARCHAR(128) NOT NULL,
            query_car_elec BOOLEAN NOT NULL,
            query_car_gas BOOLEAN NOT NULL,
            query_car_hybrid BOOLEAN NOT NULL,
            query_car_mpg INT,

            FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
        );""",

        """CREATE TABLE IF NOT EXISTS User_Selection (
            selection_id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT NOT NULL,
            query_id INT NOT NULL,
            selection_rank INT NOT NULL,
            selection_time DATETIME DEFAULT NOW(),

            FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
            FOREIGN KEY (query_id) REFERENCES User_Query(query_id) ON DELETE CASCADE
        );"""
    ]

    for query in table_queries:
        cur.execute(query)

def insert_user_data(cur, user_data):
    """
    """
    user_insert_query = """INSERT INTO User (user_name, user_pass, user_email, user_fname, user_lname) VALUES (%s, %s, %s, %s, %s);"""

    try:
        cursor.execute(user_insert_query, (row["name"], row["pass"], row["email"], row["fname"], row["lname"]))
    except:
        pass





if __name__ == "__main__":
    connection = pymysql.connect(
            host = "database-1.cyjek8guse5h.us-east-1.rds.amazonaws.com",
            user = "admin",
            password = "si699matchmycar",
            port = 3306
            )
    cursor = connection.cursor()



    # init_car_db(cursor)
    # cursor.execute("USE car_database;")
    # create_car_tables(cursor)
    # connection.commit()
    # print("Tables have been created")

    # init_user_db(cursor)
    cursor.execute("USE user_database;")
    # create_user_tables(cursor)
    # connection.commit()
    # print("Tables have been created")

    # car_data = pd.read_csv("all_makes_models_complete.csv")
    # car_data = car_data.replace({np.nan: None})
    # insert_car_data(cursor, car_data)
    # connection.commit()
    # print("Data Inserted")

    # user_data = {"name": "lindonc", "pass": "test", "email": "lindonc@test.com", "fname": "Lindon", "lname": "Camaj"}
    # insert_user_data(cursor, user_data)
    # connection.commit()
    # print("Data Inserted")

    # cursor.execute("SELECT * FROM Car;")
    # data = cursor.fetchall()
    # print(data)

    cursor.execute("SELECT * FROM User;")
    data = cursor.fetchall()
    print(data)

    cursor.close()
    connection.close()