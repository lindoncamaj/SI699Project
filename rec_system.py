import pymysql

# drive_train column has FWD,AWD,RWD
# body_type has SUV, Sedan,
def recommend(cur, min_price, max_price, location, c_type, c_make):
    # specify which columns to return later
    query = """
        SELECT car_id
        FROM Car
        JOIN Car_Make ON Car.make_id = Car_Make.make_id
        JOIN Car_Model ON Car.model_id = Car_Model.model_id
        JOIN Car_Trim ON Car.trim_id = Car_Trim.trim_id
        WHERE car_min_price >= %s AND car_min_price <= %s
    """
    filters = [min_price, max_price]

    if c_type:
        # count the number of %s to add to query
        q_add = ", ".join(['%s'] * len(c_type))
        # add to current query
        query += f" AND Car.body_type IN ({q_add})"
        # add more to filters to use on query
        filters.extend([ctype for ctype in c_type])
    
    if c_make:
        # same as above
        q_add = ", ".join(['%s'] * len(c_make))
        query += f" AND Car_make.make_name IN ({q_add})"
        filters.extend([make for make in c_make])

    # choose what to order by expert_score or consumer_score?
    query += " ORDER BY ???"

    cur.execute(query, filters)
    results = cur.fetchall()

    # WE ARE ONLY RETURNING car_id right now
    return [row[0] for row in results]


if __name__ == "__main__":
    connection = pymysql.connect(
        host="database2.cyjek8guse5h.us-east-1.rds.amazonaws.com",
        user="admin",
        password="si699matchmycar",
        database="car_database",
        port=3306
    )
    cursor = connection.cursor()

    # example test
    recommended_cars = recommend(cursor, min_price=20000,
                                 max_price=50000, c_type=['SUV'],
                                 c_make=["Hyundai", "BMW"])

    cursor.close()
    connection.close()