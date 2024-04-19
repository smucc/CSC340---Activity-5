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

'''
CREATE TABLE Orders(
    ID INT PRIMARY KEY AUTO_INCREMENT,
    BaseID INT,
    FlavorID INT,
    ToppingID INT,
    Price DECIMAL (3,2),
    FOREIGN KEY (BaseID) REFERENCES Base(ID),
    FOREIGN KEY (FlavorID) REFERENCES Flavors(ID),
    FOREIGN KEY (ToppingID) REFERENCES Toppings(ID)
);'''

CREATE TABLE Orders (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    Base VARCHAR(255),
    Flavor VARCHAR(255),
    Toppings VARCHAR(255),
    Price DECIMAL(10, 2),
    OrderTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);




-- Step 2: Create the Ratings Table
CREATE TABLE Ratings (
    rating_id INT AUTO_INCREMENT PRIMARY KEY,
    rating_value ENUM('GREAT', 'OK', 'BAD') NOT NULL,
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER //

CREATE PROCEDURE DeleteOldestRating()
BEGIN
    DECLARE oldest_id INT;
    SET oldest_id = (SELECT rating_id FROM Ratings ORDER BY inserted_at ASC LIMIT 1);
    DELETE FROM Ratings WHERE rating_id = oldest_id;
END//

CREATE TRIGGER maintain_ratings_limit_trigger
AFTER INSERT ON Ratings
FOR EACH ROW
BEGIN
    IF (SELECT COUNT(*) FROM Ratings) > 3 THEN
        CALL DeleteOldestRating();
    END IF;
END//

DELIMITER ;

DELIMITER $$
CREATE TRIGGER maintain_ratings_limit_trigger
AFTER INSERT ON Ratings
FOR EACH ROW
BEGIN
    DECLARE rating_count INT;
    SELECT COUNT(*) INTO rating_count FROM Ratings;
    IF rating_count > 3 THEN
        DELETE FROM Ratings
        WHERE rating_id = (SELECT rating_id FROM Ratings ORDER BY inserted_at LIMIT 1);
    END IF;
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE InsertRating(
    IN rating_value VARCHAR(10)
)
BEGIN
    DECLARE rating_count INT;

    -- Get the count of ratings
    SELECT COUNT(*) INTO rating_count FROM Ratings;

    -- If there are more than three ratings, delete the oldest one
    IF rating_count >= 3 THEN
        DELETE FROM Ratings ORDER BY inserted_at ASC LIMIT 1;
    END IF;

    -- Insert the new rating
    INSERT INTO Ratings (rating_value) VALUES (rating_value);
END $$
DELIMITER ;

SELECT *
FROM RATINGS;
