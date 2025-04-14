import pymysql

# form has min price, max price, body_type, make, drive_train
# drive_train column has FWD,AWD,RWD
# body_type has SUV, Sedan, etc

# ev/gas/hybrid list
# fuel economy int

# car type T/F values for Sedan, SUV, Truck
# same for ev/gas/hybrid
# check for drivetrain later


# helper function created to normalize values that will be used in recommendation sys
def normalize(value, min_val, max_val, reverse=False):
        if value is None or min_val == max_val:
            return 0.5  # neutral score if no range
        norm = (value - min_val) / (max_val - min_val)
        return 1 - norm if reverse else norm


def filtering(cur, min_price, max_price,
              c_make_ids=None,
              ev=False, gas=False, hybrid=False,
              awd=False, fwd=False, rwd=False,
              fuel_economy=0):
    # specify which columns to return later
    query = """
        SELECT 
            Car.car_id,
            Car.car_year,
            Car_Make.make_name,
            Car_Model.model_name,
            Car_Drivetrain.drivetrain_name,
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
        JOIN Car_Fuel_Type ON Car.fuel_type_id = Car_Fuel_Type.fuel_type_id
        WHERE car_min_price >= %s AND car_min_price <= %s
        AND car_comb_fuel_economy >= %s
        """
    filters = [min_price, max_price, fuel_economy]

    # add specific makes
    if c_make_ids:
        # count the number of %s to add to query
        q_add = ', '.join(['%s'] * len(c_make_ids))
        # add to current query
        query += f" AND Car.make_id IN ({q_add})"
        # i am assuming c_type_ids is a list
        filters.extend(c_make_ids)

    # add specific fuel types
    fuel_type_names = []
    if ev:
        fuel_type_names.append('Electric')
    if gas:
        fuel_type_names.append('Gas')
    if hybrid:
        fuel_type_names.append('Hybrid')

    if fuel_type_names:
        q_add = ', '.join(['%s'] * len(fuel_type_names))
        query += f" AND Car_Fuel_Type.fuel_type_name IN ({q_add})"
        filters.extend(fuel_type_names)

    # add specific drive trains
    drivetrain_names = []
    if awd:
        drivetrain_names.append('AWD')
    if fwd:
        drivetrain_names.append('FWD')
    if rwd:
        drivetrain_names.append('RWD')

    if drivetrain_names:
        q_add = ', '.join(['%s'] * len(drivetrain_names))
        query += f" AND Car_Drivetrain.drivetrain_name IN ({q_add})"
        filters.extend(drivetrain_names)

    cur.execute(query, filters)
    results = cur.fetchall()

    return results

def recommend(matched,
              query_id=None,
              location=None,
              weight_min_price=0.25, 
              weight_med_price=0.25, 
              weight_expert_score=0.25, 
              weight_consumer_score=0.25):
    
    # normalize scores and prices for fair comparison
    # first, extract all values to compute min/max for normalization
    min_prices = [row[7] for row in matched if row[7] is not None]
    med_prices = [row[8] for row in matched if row[8] is not None]
    expert_scores = [row[9] for row in matched if row[9] is not None]
    consumer_scores = [row[10] for row in matched if row[10] is not None]

    # need to consider cases for all values are missing values
    min_price_min = min(min_prices) if min_prices else 0
    min_price_max = max(min_prices) if min_prices else 1
    med_price_min = min(med_prices) if med_prices else 0
    med_price_max = max(med_prices) if med_prices else 1
    expert_score_min = min(expert_scores) if expert_scores else 0
    expert_score_max = max(expert_scores) if expert_scores else 10
    consumer_score_min = min(consumer_scores) if consumer_scores else 0
    consumer_score_max = max(consumer_scores) if consumer_scores else 10

    # score each car
    scored = []
    for row in matched:
        min_price = row[7]
        med_price = row[8]
        expert_score = row[9]
        consumer_score = row[10]

        score = (
            weight_min_price * normalize(min_price, min_price_min, min_price_max, reverse=True) +
            weight_med_price * normalize(med_price, med_price_min, med_price_max, reverse=True) +
            weight_expert_score * normalize(expert_score, expert_score_min, expert_score_max) +
            weight_consumer_score * normalize(consumer_score, consumer_score_min, consumer_score_max)
        )
        # balance out null fields

        scored.append((score, row))

    # sort by score (descending order to prioritize higher value)
    scored.sort(key=lambda x: x[0], reverse=True)

    # create output dict
    result = {}
    # how many results do we want to show?
    for i, (score, row) in enumerate(scored[:50]):
        # figure out which info we need
        result[f"item{i+1}"] = {
            "query_id": query_id,
            "zip": location,
            "year": row[1],                     # car_year
            "make": row[2].capitalize(),        # make_name
            "model": row[3].capitalize(),       # model_name
            "drivetrain": row[4],               # drivetrain_name
            "image": row[5],                    # image_url
            "min_price": float(row[6]) if row[6] is not None else None, # min_price in db
            "med_price": float(row[7]) if row[7] is not None else None, # med_price in db
            "expert_score": float(row[8]) if row[8] is not None else None, # expert_score in db
            "consumer_score": float(row[9]) if row[9] is not None else None, # consumer_score in db
        }
    
    return result

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