-- Create the 'user' table
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT
);

-- Create the 'appartments' table
CREATE TABLE IF NOT EXISTS appartments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    address TEXT NOT NULL,
    floor_level TEXT CHECK (floor_level IN ('first', 'second', 'third')) NOT NULL,
    number_of_bedrooms INTEGER,
    number_of_bathrooms INTEGER,
    does_have_garage BOOLEAN,
    user_id INTEGER,
    -- Foreign key constraint
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- Create the 'rent_history' table
CREATE TABLE IF NOT EXISTS rent_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_date DATE NOT NULL,
    to_date DATE NOT NULL,
    price REAL,
    appartment_id INTEGER,
    -- Foreign key constraint
    FOREIGN KEY (appartment_id) REFERENCES appartments(id)
);
