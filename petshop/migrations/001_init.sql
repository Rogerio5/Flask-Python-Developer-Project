-- Categorias de animais
CREATE TABLE animal_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    is_active INTEGER NOT NULL DEFAULT 1
);

-- Capacidade diária
CREATE TABLE daily_capacity (
    date TEXT PRIMARY KEY,
    max_bookings INTEGER NOT NULL
);

-- Clientes
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL
);

-- Reservas de banho
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    pet_name TEXT,
    status TEXT NOT NULL DEFAULT 'scheduled',
    created_at TEXT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES animal_categories(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Índices
CREATE INDEX idx_bookings_date ON bookings(date);
CREATE INDEX idx_bookings_category ON bookings(category_id);
CREATE INDEX idx_bookings_status ON bookings(status);

