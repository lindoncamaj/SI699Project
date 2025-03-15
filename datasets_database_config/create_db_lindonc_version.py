import pymysql
import pandas as pd
import numpy as np

# def init_db_construct():
#     conn = pymysql.connect('match-my-car.cj2q0agii4v1.us-east-1.rds.amazonaws.com', user='admin',
#                            passwd='si699matchmycar', connect_timeout=10)
#     with conn.cursor() as cur:
#         cur.execute('create database car_db;')

def init_db(cur):
    cur.execute("DROP DATABASE IF EXISTS car_database;")
    cur.execute("CREATE DATABASE IF NOT EXISTS car_database;")

def create_tables(cur):
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

        """CREATE TABLE IF NOT EXISTS Car (
            car_id INT PRIMARY KEY AUTO_INCREMENT,
            make_id INT NOT NULL,
            model_id INT NOT NULL,
            trim_id INT NOT NULL,
            car_year INT NOT NULL,
            car_msrp DECIMAL(10,2) NOT NULL,
            car_min_price DECIMAL(10, 2),
            car_med_price DECIMAL(10,2),

            FOREIGN KEY (make_id) REFERENCES Car_Make(make_id) ON DELETE CASCADE,
            FOREIGN KEY (model_id) REFERENCES Car_Model(model_id) ON DELETE CASCADE,
            FOREIGN KEY (trim_id) REFERENCES Car_Trim(trim_id) ON DELETE CASCADE
        );""",

        """CREATE TABLE IF NOT EXISTS Fuel_Economy (
            trim_id INT PRIMARY KEY,
            mileage_epa_combined_mpg DECIMAL(5,2),
            mileage_epa_city_mpg DECIMAL(5,2),
            mileage_epa_highway_mpg DECIMAL(5,2),
            FOREIGN KEY (trim_id) REFERENCES Car_Trim(trim_id) ON DELETE CASCADE
        );""",

        """CREATE TABLE IF NOT EXISTS Electric_Vehicle (
            trim_id INT PRIMARY KEY,
            range_electric DECIMAL(5,2) NOT NULL,
            epa_kwh_100_mi DECIMAL(5,2) NOT NULL,
            battery_capacity DECIMAL(5,2),
            charging_time_240v_hr DECIMAL(5,2),
            FOREIGN KEY (trim_id) REFERENCES Car_Trim(trim_id) ON DELETE CASCADE
        );""",

        """CREATE TABLE IF NOT EXISTS Safety_Rating (
            trim_id INT PRIMARY KEY,
            accident_safety_rating DECIMAL(3,1) NOT NULL,
            FOREIGN KEY (trim_id) REFERENCES Car_Trim(trim_id) ON DELETE CASCADE
        );"""
    ]

    for query in table_queries:
        cur.execute(query)







def insert_data(cur, car_data):
    make_insert_query = """INSERT INTO Car_Make (make_id, make_name) VALUES (%s, %s);"""
    model_insert_query = """INSERT INTO Car_Model (model_id, model_name) VALUES (%s, %s);"""
    trim_insert_query = """INSERT INTO Car_Trim (trim_id, trim_name) VALUES (%s, %s);"""
    car_insert_query = """
        INSERT INTO Car (make_id, model_id, trim_id, car_year, car_msrp, car_min_price, car_med_price)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
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
            cursor.execute(car_insert_query, (row["make_id"], row["model_id"], row["trim_id"], row["year"], row["trim_msrp"], row["min_price"], row["median_price"]))
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











if __name__ == "__main__":
    connection = pymysql.connect(
            host = "database2.cyjek8guse5h.us-east-1.rds.amazonaws.com",
            user = "admin",
            password = "si699matchmycar",
            port = 3306
            )

    cursor = connection.cursor()

    # create db if not exists and use db
    # init_db(cursor)
    cursor.execute("USE car_database;")

    # create tables if it doesn't exist and commit the changes
    # create_tables(cursor)
    # connection.commit()
    # print("Tables have been created")

    # insert data into tables
    # car_data = pd.read_csv("updated_car_info_and_safety_ratings2.csv")
    # print(car_data.make.unique())
    # car_data = car_data.replace({np.nan: None})
    # insert_data(cursor, car_data)
    # connection.commit()
    # print("Data Inserted")

    cursor.execute("SELECT * FROM Car;")
    data = cursor.fetchall()
    print(data)

    cursor.close()
    connection.close()