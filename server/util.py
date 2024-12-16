import json
import pickle
import numpy as np


class RealEstateModel:
    def __init__(self):
        self.model = None
        self.locations = None
        self.data_columns = None
        self.load_saved_artifacts()

    def load_saved_artifacts(self):
        print("Loading saved artifacts...start")
        with open("./artifacts/columns.json", "r") as f:
            data_columns = json.load(f)["data_columns"]
        self.data_columns = data_columns
        self.locations = data_columns[3:]

        with open("./artifacts/banglore_home_prices_model.pickle", "rb") as f:
            self.model = pickle.load(f)
        print("Loading saved artifacts...done")

    def get_estimated_price(self, location, sqft, bhk, bath):
        try:
            loc_index = self.data_columns.index(location.lower())
        except ValueError:
            loc_index = -1

        x = np.zeros(len(self.data_columns))
        x[0] = sqft
        x[1] = bath
        x[2] = bhk

        if loc_index >= 0:
            x[loc_index] = 1

        return round(self.model.predict([x])[0], 2)

    def get_location_names(self):
        return self.locations


if __name__ == "__main__":
    real_estate_model = RealEstateModel()
    print(real_estate_model.get_location_names())
    print(real_estate_model.get_estimated_price("1st Phase Jp Nagar", 1000, 3, 3))
    print(real_estate_model.get_estimated_price("1st Phase Jp Nagar", 1000, 2, 2))

# import json
# import pickle
# import numpy as np
# 
# __locations = None
# __data_columns = None
# __model = None
# 
# 
# def get_estimated_price(location, sqft, bhk, bath):
#     try:
#         loc_index = __data_columns.index(location.lower())
#     except:
#         loc_index = -1
# 
#     x = np.zeros(len(__data_columns))
#     x[0] = sqft
#     x[1] = bath
#     x[2] = bhk
#     if loc_index >= 0:
#         x[loc_index] = 1
# 
#     return round(__model.predict([x])[0], 2)
# 
# 
# def get_location_names():
#     return __locations
# 
# 
# def load_saved_artifacts():
#     print("loading saved artifacts...start")
#     global __data_columns
#     global __locations
#     global __model
# 
#     with open("./artifacts/columns.json", 'r') as f:
#         __data_columns = json.load(f)['data_columns']
#         __locations = __data_columns[3:]
# 
#     with open("./artifacts/banglore_home_prices_model.pickle", 'rb') as f:
#         __model = pickle.load(f)
#     print("loading saved artifacts...done")
# 
# 
# if __name__ == "__main__":
#     load_saved_artifacts()
#     print(get_location_names())
#     print(get_estimated_price('1st Phase Jp Nagar', 1000, 3, 3))
#     print(get_estimated_price('1st Phase Jp Nagar', 1000, 2, 2))
