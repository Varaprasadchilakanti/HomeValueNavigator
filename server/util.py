import json
import pickle
import numpy as np
import os
import logging

# Configure logging with appropriate format and level
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RealEstateModel:
    """
    A class to encapsulate real estate price prediction logic.
    Handles loading model artifacts, location names, and making predictions.
    """

    def __init__(self, artifacts_dir="./artifacts"):
        """
        Initializes the RealEstateModel class by loading required artifacts.

        :param artifacts_dir: Directory containing the artifacts (model and column data).
        """
        self.model = None
        self.locations = None
        self.data_columns = None
        self.artifacts_dir = artifacts_dir
        self.load_saved_artifacts()

    def load_saved_artifacts(self):
        """
        Loads the saved artifacts such as the trained model and column metadata.
        """
        try:
            logging.info("Loading saved artifacts...start")
            columns_path = os.path.join(self.artifacts_dir, "columns.json")
            model_path = os.path.join(self.artifacts_dir, "banglore_home_prices_model.pickle")

            # Load data columns
            with open(columns_path, "r") as f:
                self.data_columns = json.load(f)["data_columns"]
            self.locations = self.data_columns[3:]  # Assuming first three columns are sqft, bath, bhk
            logging.info(f"Loaded column data. Locations: {len(self.locations)} entries")

            # Load model
            with open(model_path, "rb") as f:
                self.model = pickle.load(f)
            logging.info("Loaded trained model successfully")
        except FileNotFoundError as e:
            logging.error(f"Artifact file not found: {e}")
            raise  # Raise exception to alert the user of critical failure
        except Exception as e:
            logging.error(f"An error occurred while loading artifacts: {e}")
            raise

    def get_location_names(self):
        """
        Returns the list of location names available in the data.

        :return: List of location names.
        """
        if not self.locations:
            logging.error("Locations data is not loaded")
            return []
        return self.locations

    def get_estimated_price(self, location, sqft, bhk, bath):
        """
        Predicts the price of a home based on input parameters.

        :param location: Location name (string).
        :param sqft: Total square footage (float).
        :param bhk: Number of bedrooms (int).
        :param bath: Number of bathrooms (int).
        :return: Estimated price (float) or None in case of an error.
        """
        try:
            if not all(isinstance(param, (int, float)) for param in [sqft, bhk, bath]):
                logging.warning("Invalid input types. Ensure sqft, bhk, and bath are numeric.")
                return None

            loc_index = -1
            if location and isinstance(location, str):
                try:
                    loc_index = self.data_columns.index(location.lower())
                except ValueError:
                    logging.warning(f"Location '{location}' not found in data columns")

            # Prepare the input array for the model
            x = np.zeros(len(self.data_columns))
            x[0] = sqft
            x[1] = bath
            x[2] = bhk
            if loc_index >= 0:
                x[loc_index] = 1

            # Make prediction
            estimated_price = round(self.model.predict([x])[0], 2)
            logging.info(f"Prediction successful. Estimated price: {estimated_price}")
            return estimated_price
        except Exception as e:
            logging.error(f"Error during prediction: {e}")
            return None


# Utility functions (outside class, if required)

def validate_artifact_paths(artifacts_dir):
    """
    Validates the existence of required artifact files.

    :param artifacts_dir: Directory containing artifact files.
    :return: Boolean indicating validation success.
    """
    required_files = ["columns.json", "banglore_home_prices_model.pickle"]
    for file in required_files:
        if not os.path.exists(os.path.join(artifacts_dir, file)):
            logging.error(f"Missing required artifact: {file}")
            return False
    return True


# Script entry point
if __name__ == "__main__":
    # Example usage
    artifacts_directory = os.getenv("ARTIFACTS_DIR", "./artifacts")  # Load directory from environment if specified

    if not validate_artifact_paths(artifacts_directory):
        logging.error("Artifact validation failed. Exiting...")
    else:
        model = RealEstateModel(artifacts_directory)

        # Display available locations
        logging.info(f"Available locations: {model.get_location_names()}")

        # Test prediction
        test_location = "1st Phase Jp Nagar"
        test_sqft = 1000
        test_bhk = 3
        test_bath = 3

        predicted_price = model.get_estimated_price(test_location, test_sqft, test_bhk, test_bath)
        logging.info(f"Predicted price for {test_sqft} sqft in {test_location}: {predicted_price}")
