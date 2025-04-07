import pymysql

# form has min price, max price, body_type, make, drive_train
# drive_train column has FWD,AWD,RWD
# body_type has SUV, Sedan, etc

# helper function created to normalize values that will be used in recommendation sys
def normalize(value, min_val, max_val, reverse=False):
        if value is None or min_val == max_val:
            return 0.5  # Neutral score if no range
        norm = (value - min_val) / (max_val - min_val)
        return 1 - norm if reverse else norm

def filtering(cur, min_price, max_price, c_type_ids=None, c_make_ids=None, drivetrain_ids=None):
    # specify which columns to return later
    query = """
        SELECT 
            Car.car_id,
            Car.car_year,
            Car_Make.make_name,
            Car_Model.model_name,
            Car_Drivetrain.drivetrain_name,
            Body_Type.body_type_name,
            Car_Image.image_url,
            Car.car_min_price,
            Car.car_med_price,
            Car.car_expert_score,
            Car.car_consumer_score
        FROM Car
        JOIN Car_Make ON Car.make_id = Car_Make.make_id
        JOIN Car_Model ON Car.model_id = Car_Model.model_id
        JOIN Car_Drivetrain ON Car.drivetrain_id = Car_Drivetrain.drivetrain_id
        JOIN Car_Image ON Car.image_id = Car_Image.image_id
        JOIN Body_Type ON Car.body_type_id = Body_Type.body_type_id
        WHERE car_min_price >= %s AND car_min_price <= %s
    """
    filters = [min_price, max_price]

    if c_type_ids:
        # count the number of %s to add to query
        q_add = ', '.join(['%s'] * len(c_type_ids))
        # add to current query
        query += f" AND Car.body_type IN ({q_add})"
        # i am assuming c_type_ids is a list
        filters.extend(c_type_ids)

    if c_make_ids:
        q_add = ', '.join(['%s'] * len(c_make_ids))
        query += f" AND Car.make_id IN ({q_add})"
        filters.extend(c_make_ids)

    if drivetrain_ids:
        q_add = ', '.join(['%s'] * len(drivetrain_ids))
        query += f" AND Car.drivetrain_id IN ({q_add})"
        filters.extend(drivetrain_ids)

    cur.execute(query, filters)
    results = cur.fetchall()

    return results

def recommend(matched,
              weight_min_price=0.25, 
              weight_med_price=0.25, 
              weight_expert_score=0.25, 
              weight_consumer_score=0.25):
    
    # Normalize scores and prices for fair comparison
    # First, extract all values to compute min/max for normalization
    min_prices = [row[7] for row in matched if row[7] is not None]
    med_prices = [row[8] for row in matched if row[8] is not None]
    expert_scores = [row[9] for row in matched if row[9] is not None]
    consumer_scores = [row[10] for row in matched if row[10] is not None]

    # score each car
    scored = []
    for row in matched:
        min_price = row[7]
        med_price = row[8]
        expert_score = row[9]
        consumer_score = row[10]

        score = (
            weight_min_price * normalize(min_price, min(min_prices), max(min_prices), reverse=True) +
            weight_med_price * normalize(med_price, min(med_prices), max(med_prices), reverse=True) +
            weight_expert_score * normalize(expert_score, min(expert_scores), max(expert_scores)) +
            weight_consumer_score * normalize(consumer_score, min(consumer_scores), max(consumer_scores))
        )

        scored.append((score, row))

    # sort by score (descending order to prioritize higher value)
    scored.sort(key=lambda x: x[0], reverse=True)

    # return just the ordered rows (score isn't returned)
    # we are returning a list of tuples
    return [row for score, row in scored]

    


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