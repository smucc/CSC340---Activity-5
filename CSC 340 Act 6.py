from pymongo import MongoClient

host = "localhost"
port_number = 27017

client = MongoClient(host, port_number)

db = client["IceCream"]

base = [
    {
        "ID": 1,
        "Base": "SMALL_CUP",
        "Price": 2.50
    },
    {
        "ID": 2,
        "Base": "MEDIUM_CUP",
        "Price": 3.50
    },
    {
        "ID": 3,
        "Base": "LARGE_CUP",
        "Price": 5.00
    },
    {
        "ID": 4,
        "Base": "REGULAR_CONE",
        "Price": 3.00
    },
    {
        "ID": 5,
        "Base": "WAFFLE_CONE",
        "Price": 4.00
    }
]

bases = db['base']

# Clear existing documents in the 'base' collection
bases.delete_many({})

# Insert new documents into the 'base' collection
bases.insert_many(base)

# Print contents of the 'base' collection
for document in bases.find({}):
    print(document)


flavor = [
    {
        "ID": 1,
        "Flavor": "CHOCOLATE",
        "Price": 0.00
    },
    {
        "ID": 2,
        "Flavor": "VANILLA",
        "Price": 0.00
    },
    {
        "ID": 3,
        "Flavor": "STRAWBERRY",
        "Price": 0.00
    },
    {
        "ID": 4,
        "Flavor": "MINT",
        "Price": 0.00
    },
    {
        "ID": 5,
        "Flavor": "CHOCOLATE_CHIP",
        "Price": 0.00
    },
    {
        "ID": 6,
        "Flavor": "COFFEE",
        "Price": 0.00
    },
    {
        "ID": 7,
        "Flavor": "COOKIE_DOUGH",
        "Price": 0.50
    },
    {
        "ID": 8,
        "Flavor": "FRENCH_VANILLA",
        "Price": 0.50
    },
    {
        "ID": 9,
        "Flavor": "CAKE_BATTER",
        "Price": 0.50
    },
]

flavors = db['flavor']

# Clear existing documents in the 'base' collection
flavors.delete_many({})

# Insert new documents into the 'base' collection
flavors.insert_many(flavor)

# Print contents of the 'base' collection
for document in flavors.find({}):
    print(document)


topping = [
    {
        "ID": 1,
        "Topping": "SPRINKLES",
        "Price": 0.75
    },
    {
        "ID": 2,
        "Topping": "CHOC_CHIPS",
        "Price": 0.75
    },
    {
        "ID": 3,
        "Topping": "GUMMY_BEARS",
        "Price": 0.75
    },
    {
        "ID": 4,
        "Topping": "M&Ms",
        "Price": 1.00
    },
    {
        "ID": 5,
        "Topping": "OREOS",
        "Price": 1.00
    },
    {
        "ID": 6,
        "Topping": "WHIPPED_CREAM",
        "Price": 1.00
    },
    {
        "ID": 7,
        "Topping": "KIT_KAT",
        "Price": 1.00
    },
    {
        "ID": 8,
        "Topping": "REESES_CUPS",
        "Price": 1.25
    },
    {
        "ID": 9,
        "Topping": "YELLOW_CAKE",
        "Price": 1.50
    },
]

toppings = db['topping']

# Clear existing documents in the 'base' collection
toppings.delete_many({})

# Insert new documents into the 'base' collection
toppings.insert_many(topping)

# Print contents of the 'base' collection
for document in toppings.find({}):
    print(document)

###########################################################################################################################


