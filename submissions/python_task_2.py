import pandas as pd

df = pd.read_csv("datasets/dataset-3.csv")
def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    # Creating a directed graph from the DataFrame
    G = nx.from_pandas_edgelist(df, 'id_1', 'id_2', ['distance'], create_using=nx.DiGraph())

    # Calculating the cumulative distances between IDs
    distance_matrix = nx.floyd_warshall_numpy(G, weight='distance', nodelist=sorted(G.nodes))

    # Creating a DataFrame from the distance matrix
    distance_df = pd.DataFrame(distance_matrix, index=sorted(G.nodes), columns=sorted(G.nodes))

    # Setting diagonal values to 0
    distance_df.values[[range(len(distance_df))]*2] = 0

    return distance_df


def unroll_distance_matrix(distance_matrix: pd.DataFrame) -> pd.DataFrame:
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    # Creating an empty list to store unrolled data
    unrolled_data = []

    # Iterate through the distance matrix
    for id_start in distance_matrix.index:
        for id_end in distance_matrix.columns:
            if id_start != id_end:
                # Append the unrolled data to the list
                unrolled_data.append({'id_start': id_start, 'id_end': id_end, 'distance': distance_matrix.loc[id_start, id_end]})

    # Create a DataFrame from the unrolled data
    unrolled_df = pd.DataFrame(unrolled_data)

    return unrolled_df



def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
    # Filter rows where id_start is the reference value
    reference_rows = distance_df[distance_df['id_start'] == reference_value]

    # Calculate the average distance for the reference value
    average_distance = reference_rows['distance'].mean()

    # Calculate the threshold range (10% of the average distance)
    threshold_range = 0.1 * average_distance

    # Filter rows within the threshold range
    within_threshold_rows = reference_rows[(reference_rows['distance'] >= (average_distance - threshold_range)) & (reference_rows['distance'] <= (average_distance + threshold_range))]

    # Get unique values from id_start column within the threshold
    within_threshold_ids = sorted(within_threshold_rows['id_start'].unique())

    return within_threshold_id


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    # Define rate coefficients for each vehicle type
    rate_coefficients = {'moto': 0.8,'car': 1.2,'rv': 1.5,'bus': 2.2,'truck': 3.6}

    # Create new columns for each vehicle type with toll rates
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        distance_df[vehicle_type] = distance_df['distance'] * rate_coefficient

    return distance_df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    # Define time ranges and discount factors
    time_ranges_weekdays = [(time(0, 0, 0), time(10, 0, 0)), (time(10, 0, 0), time(18, 0, 0)), (time(18, 0, 0), time(23, 59, 59))]
    time_ranges_weekends = [(time(0, 0, 0), time(23, 59, 59))]
    discount_factors_weekdays = [0.8, 1.2, 0.8]
    discount_factor_weekends = 0.7

    # Initialize lists to store unrolled data
    unrolled_data = []

    # Iterate through each row in the input DataFrame
    for _, row in input_df.iterrows():
        id_start, id_end, distance, datetime_val = row['id_start'], row['id_end'], row['distance'], row['datetime']
        
        # Determine the day of the week
        day_of_week = datetime_val.strftime('%A')

        # Choose the appropriate discount factor based on the day of the week
        if day_of_week in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            discount_factors = discount_factors_weekdays
            time_ranges = time_ranges_weekdays
        else:
            discount_factors = [discount_factor_weekends]
            time_ranges = time_ranges_weekends

        # Iterate through time ranges and calculate toll rates
        for start_time, end_time in time_ranges:
            if start_time <= datetime_val.time() <= end_time:
                discount_factor = discount_factors[time_ranges.index((start_time, end_time))]
                toll_rate = distance * discount_factor

                # Append the unrolled data to the list
                unrolled_data.append({
                    'id_start': id_start,
                    'id_end': id_end,
                    'distance': distance,
                    'datetime': datetime_val,
                    'start_day': day_of_week,
                    'start_time': start_time,
                    'end_day': day_of_week,
                    'end_time': end_time,
                    'toll_rate': toll_rate
                })

    # Create a DataFrame from the unrolled data
    result_df = pd.DataFrame(unrolled_data)

    return result_df






    