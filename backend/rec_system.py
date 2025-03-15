import random

def recommend(min_price, max_price, location, c_type, c_make):
    cars = []

    for i in range(10):
        cars.append(random.randint(1, 9190))

    return cars