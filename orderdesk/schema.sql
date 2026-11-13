DROP TABLE IF EXISTS order_item;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  email TEXT NOT NULL,
  is_admin INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE product (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  sku TEXT UNIQUE NOT NULL,
  price_cents INTEGER NOT NULL
);

CREATE TABLE orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL REFERENCES user (id),
  status TEXT NOT NULL DEFAULT 'open',
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  invoice TEXT
);

CREATE TABLE order_item (
  order_id INTEGER NOT NULL REFERENCES orders (id),
  product_id INTEGER NOT NULL REFERENCES product (id),
  quantity INTEGER NOT NULL
);

INSERT INTO product (name, sku, price_cents) VALUES
  ('USB-C cable 2m', 'CAB-USBC-2', 1299),
  ('Wireless mouse', 'MOU-WL-01', 2499),
  ('27" monitor', 'MON-27-4K', 32900),
  ('Laptop stand', 'STD-LAP-AL', 4599);
