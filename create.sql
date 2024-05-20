CREATE TABLE City (
    neighborhood VARCHAR(500) PRIMARY KEY,
    city_name VARCHAR(50)
);

CREATE TABLE Locations (
    location_id SERIAL PRIMARY KEY,
    neighborhood VARCHAR(500),
    latitude FLOAT,
    longitude FLOAT,
    FOREIGN KEY (neighborhood) REFERENCES City (neighborhood)
);

CREATE TABLE Room_types (
    room_type_id SERIAL PRIMARY KEY,
    room_type VARCHAR(50)
);

CREATE TABLE Listings (
    listing_id BIGINT PRIMARY KEY,
    location_id INT,
    room_type_id INT,
    name VARCHAR(500),
    price INT,
    minimum_nights INT,
    availability_365 INT,
    FOREIGN KEY (location_id) REFERENCES Locations (location_id),
    FOREIGN KEY (room_type_id) REFERENCES room_types (room_type_id)
);

CREATE TABLE Hosts (
    host_id BIGINT,
    listing_id BIGINT PRIMARY KEY,
    host_name VARCHAR(50),
    calculated_host_listings_count INT
);


CREATE TABLE Reviews (
    listing_id BIGINT PRIMARY KEY,
    number_of_reviews INT,
    last_review DATE,
    reviews_per_month FLOAT,
    number_of_reviews_ltm INT
);
