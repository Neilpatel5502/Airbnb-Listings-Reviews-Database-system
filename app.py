import streamlit as st
import pandas as pd
import psycopg2
import sys

def execute_query(query):
    conn = psycopg2.connect(
        dbname=sys.argv[1],
        user=sys.argv[2],
        password=sys.argv[3],
        host=sys.argv[4],
        port=sys.argv[5]
    )
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return column_names, rows

def get_city_list():
    df = pd.read_csv("data/city.csv")
    cities = df['city_name'].unique()
    return tuple(cities)

def get_room_types():
    df = pd.read_csv("data/room_types.csv")
    room_types = df['room_type'].unique()
    return tuple(room_types)


st.set_page_config(page_title="Airbnb Listing Reviews", layout="wide")

with st.container():
    st.markdown("<h1 style='text-align: center;'>Airbnb Listing Reviews Data</h1>", unsafe_allow_html=True)

with st.expander("Filtered Query"):
    # filter 1: price range
    price_range = st.slider("Price Range", min_value=0, max_value=100000, value=(100, 500))

    # filter 2: city
    cities = get_city_list()
    filter_cities = tuple(st.multiselect('Choose cities', list(cities)))

    if len(filter_cities) == 1:
        filter_cities = f"('{filter_cities[0]}')"

    # filter 3: room types
    room_types = get_room_types()
    filter_room_types = tuple(st.multiselect('Choose room types', list(room_types)))

    if len(filter_room_types) == 1:
        filter_room_types = f"('{filter_room_types[0]}')"

    # filter 4: Availabilty of minimum number of nights
    minimum_nights = st.number_input("Insert a minimum number of nights of the room", value=None, placeholder="Type a number...")

    # filter 5: Check other fields you want to add
    COLUMNS = {
        "Host ID": "h.host_id",
        "Host name": "h.host_name",
        "Listing count of hosts": "h.calculated_host_listings_count",
        "Last review of listing": "R.last_review",
        "Reviews per month": "R.reviews_per_month",
        "Total reviews received by listing in lifetime": "R.number_of_reviews_ltm",
        "Neighborhood of the listing": "L.neighborhood",
        "Latitude": "L.latitude",
        "Longitude": "L.longitude",
    }
    other_fields = st.multiselect('Check other fields you want to see', COLUMNS.keys())
    other_fields = [COLUMNS[label] for label in other_fields]

    # Add conditions to the Query
    condition_parts = []

    if price_range:
        condition_parts.append(f"Li.price>={price_range[0]} and Li.price<={price_range[1]}")
    if filter_cities:
        condition_parts.append(f"C.city_name IN {filter_cities}")
    if filter_room_types:
        condition_parts.append(f"Rt.room_type IN {filter_room_types}")
    if minimum_nights:
        condition_parts.append(f"Li.minimum_nights>={minimum_nights}")

    if not condition_parts:
        conditions = f"1 = 1;"
    else:
        conditions = " AND ".join(condition_parts) + ";"

    # Add Selections to the query
    selection_list = [
        "Li.listing_id",
        "Li.name",
        "Li.minimum_nights",
        "Li.availability_365",
        "R.number_of_reviews",
        "Rt.room_type",
        "Li.price",
        "C.city_name"
    ]

    selection_list += other_fields
    selection = ",".join(selection_list)

    query = f'''SELECT
                    {selection}
                FROM
                    Listings Li
                JOIN
                    Reviews R ON Li.listing_id = R.listing_id
                JOIN
                    Hosts h ON Li.listing_id = h.listing_id
                JOIN
                    Room_types Rt ON Li.room_type_id = Rt.room_type_id
                JOIN
                    Locations L ON Li.location_id = L.location_id
                JOIN
                    City C ON L.neighborhood = C.neighborhood
                WHERE
                    {conditions}'''

    try:
        column_names, rows = execute_query(query)
        if rows:
            df = pd.DataFrame(rows, columns=column_names)
            df.index = df.index + 1
            st.dataframe(df)
        else:
            st.warning("No results found.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


with st.expander("Custom Query"):

    custom_query = st.text_area("Enter your SQL query:")
    if st.button("Execute Custom Query"):
        try:
            # Execute the custom query
            query = custom_query.strip()
            column_names, rows = execute_query(query)
            if rows:
                df = pd.DataFrame(rows, columns=column_names)
                df.index = df.index + 1
                st.dataframe(df)
            else:
                st.warning("No results found.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
