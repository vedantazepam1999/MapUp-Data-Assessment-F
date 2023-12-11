import pandas as pd

dataset = pd.read_csv('submissions/dataset-1.csv')
def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here

    #generating matrix by creating a pivot table
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car')

    # adding zero in place of a missing value
    car_matrix = car_matrix.fillna(0)
    
    # Setting diagonal values to 0
    for idx in car_matrix.index:
        car_matrix.loc[idx, idx] = 0

    return car_matrix


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    car_counts = df['car'].value_counts().to_dict()

    return car_counts


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    # Finding the mean of the 'bus' column
    bus_mean = df['bus'].mean()

    # Finding  indexes where 'bus' values are greater than twice the mean
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()

    return bus_indexes


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    # Grouping by 'route' and calculating the mean of 'truck' for each group
    route_means = df.groupby('route')['truck'].mean()

    # Filtering routes where the average 'truck' values are greater than 7
    filtered_routes = route_means[route_means > 7].index.tolist()

    # Sorting the list of routes
    sorted_routes = sorted(filtered_routes)

    return sorted_routes
    

def multiply_matrix(car_matrix: pd.DataFrame) -> pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    # Applying custom conditions to multiply values
    modified_car_matrix = car_matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    # Rounding values to 1 decimal place
    modified_car_matrix = modified_car_matrix.round(1)

    return modified_car_matrix



def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    # Combining date and time columns into a single datetime column
    df['datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])  

    # Extracting day of the week and hour of the day
    df['day_of_week'] = df['datetime'].dt.day_name()
    df['hour_of_day'] = df['datetime'].dt.hour

    # Creating a mask for incorrect timestamps
    incorrect_timestamps = (
        (df['day_of_week'].nunique() != 7) |  # Checking if all 7 days are present
        (df['hour_of_day'].nunique() != 24)   # Checking if all 24 hours are present
    )

    # Group by (id, id_2) and check if any group has incorrect timestamps
    result_series = df.groupby(['id', 'id_2'])['timestamp'].agg(lambda x: incorrect_timestamps.any())

    return result_series