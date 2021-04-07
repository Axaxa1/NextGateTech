from tools import *
from data import *

if __name__ == '__main__':
    # Load training dataset
    data = create_data("Data/example.csv")

    # Create NAV series for each asset
    nav_data = reshape_nav_data(data)

    # Connect to fire base
    datab = connect_firebase("nextgatetech-d5ce1-firebase-adminsdk-yb2su-69834d4a42.json")

    # Compute and write tests (only no_nan is implemented here see notebook for other)
    update_test(data, datab)

    # Compute and write correlations
    update_correlations(nav_data, datab)

    # Print firebase
    read_firebase(datab)
