import psycopg2
import os, sys

conn = psycopg2.connect(
        dbname=sys.argv[1],
        user=sys.argv[2],
        password=sys.argv[3],
        host=sys.argv[4],
        port=sys.argv[5]
    )

conn.autocommit = True
cursor = conn.cursor()

data_folder = os.getcwd()

city_entries = f"COPY city(neighborhood,city_name) FROM '{data_folder}/data/city.csv' DELIMITER ',' CSV HEADER;"
location_entries = f"COPY locations(neighborhood,latitude,longitude) FROM '{data_folder}/data/locations.csv' DELIMITER ',' CSV HEADER;"
room_type_entries = f"COPY room_types(room_type) FROM '{data_folder}/data/room_types.csv' DELIMITER ',' CSV HEADER;"
reviews_entries = f"COPY reviews(listing_id,number_of_reviews,last_review,reviews_per_month,number_of_reviews_ltm) FROM '{data_folder}/data/reviews.csv' DELIMITER ',' CSV HEADER;"
listing_entries = f"COPY listings(listing_id,location_id,room_type_id,name,price,minimum_nights,availability_365) FROM '{data_folder}/data/listings.csv' DELIMITER ',' CSV HEADER;"
hosts_entries = f"COPY hosts(listing_id,host_id,host_name,calculated_host_listings_count) FROM '{data_folder}/data/hosts.csv' DELIMITER ',' CSV HEADER;"

cursor.execute(city_entries)
cursor.execute(location_entries)
cursor.execute(room_type_entries)
cursor.execute(reviews_entries)
cursor.execute(listing_entries)
cursor.execute(hosts_entries)

cursor.close()
conn.commit()
conn.close()
