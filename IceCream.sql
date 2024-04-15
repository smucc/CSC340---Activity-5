CREATE DATABASE IceCream;
USE IceCream;

CREATE TABLE Base(
    ID INT PRIMARY KEY,
    Base VARCHAR(255),
    Price DECIMAL(3,2)
);

INSERT INTO Base (ID, Base, Price)
VALUES
    (1, 'SMALL_CUP', 2.50),
    (2, 'MEDIUM_CUP', 3.50),
    (3, 'LARGE_CUP', 5.00),
    (4, 'REGULAR_CONE', 3.00),
    (5, 'WAFFLE_CONE', 4.00);

CREATE TABLE Flavors(
    ID INT PRIMARY KEY,
    Flavor VARCHAR(255),
    Price DECIMAL(3,2)
);

INSERT INTO Flavors (ID, Flavor, Price)
VALUES
    (1, 'CHOCOLATE', 0.00),
    (2, 'VANILLA', 0.00),
    (3, 'STRAWBERRY', 0.00),
    (4, 'MINT', 0.00),
    (5, 'CHOCOLATE_CHIP', 0.00),
    (6, 'COFFEE', 0.00),
    (7, 'COOKIE_DOUGH', 0.50),
    (8, 'FRENCH_VANILLA', 0.50),
    (9, 'CAKE_BATTER', 0.50);

CREATE TABLE Toppings(
    ID INT PRIMARY KEY,
    Topping VARCHAR(255),
    Price DECIMAL(3,2)
);

INSERT INTO Toppings (ID, Topping, Price)
VALUES
    (1, 'SPRINKLES', 0.75),
    (2, 'CHOC_CHIPS', 0.75),
    (3, 'GUMMY_BEARS', 0.75),
    (4, 'M&Ms', 1.00),
    (5, 'OREOS', 1.00),
    (6, 'WHIPPED_CREAM', 1.00),
    (7, 'KIT_KAT', 1.00),
    (8, 'REESES_CUPS', 1.25),
    (9, 'YELLOW_CAKE', 1.50);

CREATE TABLE Orders(
    Base VARCHAR(255),
    Flavor VARCHAR(255),
    Topping VARCHAR(255),
    Price DECIMAL (3,2),
    FOREIGN KEY (Base) REFERENCES Base(Base),
    FOREIGN KEY (Flavor) REFERENCES Flavors(Flavor),
    FOREIGN KEY (Topping) REFERENCES Toppings(Topping)
);

CREATE TABLE Ratings(
    Rating_Id INT,
    Rating_Value INT,
    Rating INT,
    CHECK (Rating >= 1 AND Rating <= 5)
);

SELECT Base, Price FROM base;