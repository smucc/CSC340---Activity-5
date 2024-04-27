from pymongo import MongoClient
import tkinter as tk
import mysql.connector
import decimal
from PIL import Image, ImageTk
from tkinter import PhotoImage
from datetime import datetime

host = "localhost"
port_number = 27017

client = MongoClient(host, port_number)

db = client["IceCream"]

# Your base data
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

# Format the price in each base
for base_item in base:
    base_item["Price"] = "{:.2f}".format(base_item["Price"])

# Now, you can insert the data into the MongoDB collection
bases = db['base']


# Clear existing documents in the 'base' collection
bases.delete_many({})

# Insert new documents into the 'base' collection
bases.insert_many(base)

# Print contents of the 'base' collection
#for document in bases.find({}):
#    print(document)


# Your flavor data
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

# Format the price in each flavor
for flavor_item in flavor:
    flavor_item["Price"] = "{:.2f}".format(flavor_item["Price"])

# Now, you can insert the data into the MongoDB collection
flavors = db['flavor']

# Clear existing documents in the 'base' collection
flavors.delete_many({})

# Insert new documents into the 'base' collection
flavors.insert_many(flavor)

# Print contents of the 'base' collection
#for document in flavors.find({}):
#    print(document)


# Your topping data
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

# Format the price in each topping
for topping_item in topping:
    topping_item["Price"] = "{:.2f}".format(topping_item["Price"])

# Now, you can insert the data into the MongoDB collection
toppings = db['topping']
#toppings.insert_many(topping)


# Clear existing documents in the 'topping' collection
toppings.delete_many({})

# Insert new documents into the 'topping' collection
toppings.insert_many(topping)

# Print contents of the 'base' collection
#for document in toppings.find({}):
#    print(document)

print('\n')

# Retrieve base options
bases = bases.find({})
for base in bases:
    print(base)

# Retrieve flavor options
flavors = flavors.find({})
for flavor in flavors:
    print(flavor)

# Retrieve topping options
toppings = toppings.find({})
for topping in toppings:
    print(topping)

###########################################################################################################################

class IceCreamShopApp:
    def __init__(self, master):
        self.master = master
        master.title("Ice Cream Shop")
        #master['background']='#856ff8'
        #master.option_add("*Label*Background", "blue")
        #master.option_add("*Button*Background", "blue")
        master.configure(bg="#FFB6C1")
        master.attributes("-fullscreen", True)

        # Connect to MySQL database
        #self.mydb = mysql.connector.connect(
        #    host="localhost",
        #    user="root",
        #    password="fantasyape123",
        #    database="IceCream"
        #)

        # Creating frames for each category
        self.base_frame = tk.Frame(master, bg="#FFB6C1")
        self.flavor_frame = tk.Frame(master, bg="#FFB6C1")
        self.toppings_frame = tk.Frame(master, bg="#FFB6C1")
        self.base_frame.grid(row=0, column=0)
        self.flavor_frame.grid(row=1, column=0)
        self.toppings_frame.grid(row=2, column=0)

        # Initializing a list to hold PhotoImage objects
        self.base_images = []
        self.flavor_images = []
        self.topping_images = []

        # Create frames for options and dividers
        self.create_frames_and_dividers()

        # Create listbox for selected items
        # Create listbox for selected items with larger font size
        self.selected_items_listbox = tk.Listbox(master, width=40, height=12, font=("Courier", 14))
        self.selected_items_listbox.grid(row=4, column=1, columnspan=3, padx=10, pady=10, sticky="n")

        # Create confirm buttons for base, flavor, and topping selection
        self.create_confirm_buttons()

        # Display options for each category
        self.show_base_options()
        self.show_flavors_options()
        self.show_toppings_options()

        # Create rating buttons
        self.create_bad_rating_button()
        self.create_ok_rating_button()
        self.create_great_rating_button()

        # Create reset order button
        self.create_reset_button()
        self.create_complete_order_button()

        # State variables to track confirmation status
        self.base_confirmed = False
        self.flavor_confirmed = False
        self.topping_confirmed = False
        self.complete_order_button.config(state=tk.DISABLED)

        # Initialize selected items variables
        self.selected_base = None
        self.selected_flavor = None
        self.selected_toppings = []

        # Labels for displaying most popular items
        self.most_popular_base_label = tk.Label(master, text="", font=("Arial", 22), bg="#FFB6C1")
        #self.most_popular_base_label.grid(row=4, column=0, padx=10, pady=10, sticky="nw")
        self.most_popular_base_label.place(x=11, y=575)

        self.most_popular_flavor_label = tk.Label(master, text="", font=("Arial", 22), bg="#FFB6C1")
        #self.most_popular_flavor_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.most_popular_flavor_label.place(x=11, y=615)

        self.most_popular_topping_label = tk.Label(master, text="", font=("Arial", 22), bg="#FFB6C1")
        #self.most_popular_topping_label.grid(row=4, column=0, padx=10, pady=10, sticky="sw")
        self.most_popular_topping_label.place(x=11, y=655)

        # Display the most popular items
        self.display_most_popular_items()

        self.total_price = decimal.Decimal('0.0')

        # Display the most recent ratings initially
        self.update_recent_ratings()


    def create_frames_and_dividers(self):
        # Configuring grid rows and columns for flexibility
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1, minsize=300)
        self.master.grid_columnconfigure(2, weight=1, minsize=300)
        self.master.grid_columnconfigure(4, weight=1, minsize=300)

        # Create frame for base options
        self.base_options_frame = tk.Frame(self.master, bg="#FFB6C1")
        self.base_options_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Create frame for flavor options
        self.flavor_options_frame = tk.Frame(self.master, bg="#FFB6C1")
        self.flavor_options_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        # Create frame for topping options
        self.topping_options_frame = tk.Frame(self.master, bg="#FFB6C1")
        self.topping_options_frame.grid(row=1, column=4, padx=10, pady=10, sticky="nsew")

        # Create divider frames
        divider1 = tk.Frame(self.master, bg="black", width=2)
        divider1.grid(row=1, column=1, rowspan=3, padx=10, pady=10, sticky="ns")
        divider2 = tk.Frame(self.master, bg="black", width=2)
        divider2.grid(row=1, column=3, rowspan=3, padx=10, pady=10, sticky="ns")

        divider3 = tk.Frame(self.master, bg="black", width=50)
        divider3.grid(row=3, column=0, columnspan=5, padx=10, pady=5, sticky="ew")

        # Create label to display total price
        self.total_label = tk.Label(self.master, text="TOTAL: $0.00", font=("Arial", 30), bg="#FFB6C1")
        #self.total_label.grid(row=4, column=4, columnspan=15, padx=50, pady=70, sticky= "s")
        self.total_label.place(x=1180, y=795)

        self.rate_us_label = tk.Label(self.master, text="Rate Us!", font=("Arial", 24), bg="#FFB6C1")
        # self.total_label.grid(row=4, column=4, columnspan=15, padx=50, pady=70, sticky= "s")
        self.rate_us_label.place(x=105, y=700)

        self.bases_label = tk.Label(self.master, text="Select a Base", font=("Vivaldi Italic", 34), bg="#FFB6C1")
        #self.bases_label.grid(row=0, column=0, sticky="n")
        self.bases_label.place(x=129, y=0)

        self.flavors_label = tk.Label(self.master, text="Select a Flavor", font=("Vivaldi Italic", 34), bg="#FFB6C1")
        #self.flavors_label.grid(row=0, column=2,sticky="n")
        self.flavors_label.place(x=668, y=0)

        self.toppings_label = tk.Label(self.master, text="Select up to 5 Toppings", font=("Vivaldi Italic", 34), bg="#FFB6C1")
        #self.toppings_label.grid(row=0, column=4, sticky="n")
        self.toppings_label.place(x=1100, y=0)

    def create_confirm_buttons(self):
        # Create confirm buttons for base, flavor, and topping selection
        self.base_confirm_button = tk.Button(self.master, font = ("Arial", 24), text="Confirm Base", command=self.confirm_base)
        self.base_confirm_button.grid(row=2, column=0, padx=5, pady=5)
        self.flavor_confirm_button = tk.Button(self.master, font = ("Arial", 24), text="Confirm Flavor", command=self.confirm_flavor, state=tk.DISABLED)
        self.flavor_confirm_button.grid(row=2, column=2, padx=5, pady=5)
        self.topping_confirm_button = tk.Button(self.master, font = ("Arial", 24), text="Confirm Topping", command=self.confirm_topping, state=tk.DISABLED)
        self.topping_confirm_button.grid(row=2, column=4, padx=5, pady=5)

    def create_reset_button(self):
        self.reset_button = tk.Button(self.master, width=20, height=8, text="Reset Order", font=("Arial", 15), command=self.reset_order)
        #self.reset_button.grid(row=4, column=4, padx=10, pady=10, sticky="n")
        self.reset_button.place(x=1296, y=585)


    def create_complete_order_button(self):
        self.complete_order_button = tk.Button(self.master, width=20, height=8, text = "Complete Order", font=("Arial", 15), command=self.complete_order)
        #self.complete_order_button.grid(row=4, column=4, padx=10, pady=10)
        self.complete_order_button.place(x=1076, y=585)

    from PIL import Image, ImageTk

    def create_bad_rating_button(self):
        img_path = 'frowny.jpeg'
        img = Image.open(img_path)

        # Resize the image while preserving its aspect ratio
        width, height = 85, 85  # Adjust these values to fit your layout
        img = img.resize((width, height), Image.LANCZOS)

        photo = ImageTk.PhotoImage(img)

        # Keep a reference to the photo to prevent garbage collection
        self.bad_rating_button_photo = photo

        self.bad_rating_button = tk.Button(self.master, image=photo, width=width, height=height,
                                           font=("Arial", 10), command=self.give_bad_rating)
        self.bad_rating_button.place(x=35, y=749)  # Adjust these coordinates as needed

    def create_ok_rating_button(self):
        img_path = 'neutral.jpeg'
        img = Image.open(img_path)

        # Resize the image while preserving its aspect ratio
        width, height = 85, 85  # Adjust these values to fit your layout
        img = img.resize((width, height), Image.LANCZOS)

        photo = ImageTk.PhotoImage(img)

        # Keep a reference to the photo to prevent garbage collection
        self.ok_rating_button_photo = photo

        self.ok_rating_button = tk.Button(self.master, image=photo, width=width, height=height,
                                           font=("Arial", 10), command=self.give_ok_rating)
        self.ok_rating_button.place(x=125, y=749)

    def create_great_rating_button(self):
        img_path = 'smiley.jpeg'
        img = Image.open(img_path)

        # Resize the image while preserving its aspect ratio
        width, height = 85, 85  # Adjust these values to fit your layout
        img = img.resize((width, height), Image.LANCZOS)

        photo = ImageTk.PhotoImage(img)

        # Keep a reference to the photo to prevent garbage collection
        self.great_rating_button_photo = photo

        self.great_rating_button = tk.Button(self.master, image=photo, width=width, height=height,
                                           font=("Arial", 10), command=self.give_great_rating)
        self.great_rating_button.place(x=215, y=749)

    def add_to_cart(self, option, price, category):
       # Debug: Output when adding to cart
        print(f"Adding to cart: {option}, {price}, {category}")

        # Format the option, category, and price to display in the listbox
        formatted_item = f"{option} ({category})"
        if price is not None:
            formatted_price = f"${price:.2f}"
            # Calculate padding length based on the length of the formatted item and price
            padding_length = 40 - len(formatted_item) - len(formatted_price)
            padded_item = f"{formatted_item}{' ' * padding_length}{formatted_price}"

            item = padded_item
            # Update total price
            self.total_price += decimal.Decimal(str(price))
        else:
            item = formatted_item
        # Check if the item is already in the list
        if item not in self.selected_items_listbox.get(0, tk.END):
            # Append the item to the list
            self.selected_items_listbox.insert(tk.END, item)

        # Remove existing "Total" entries
        total_indices = [i for i, item in enumerate(self.selected_items_listbox.get(0, tk.END)) if "Total" in item]
        for index in total_indices:
            self.selected_items_listbox.delete(index)

        # Display the total price at the bottom of the list
        self.display_total_price()

    def display_total_price(self):
        # Check if the total price item is already in the list
        total_indices = [i for i, item in enumerate(self.selected_items_listbox.get(0, tk.END)) if "Total" in item]
        for index in reversed(total_indices):
            self.selected_items_listbox.delete(index)

        total_price_item = f"Total: ${self.total_price:.2f}"
        self.selected_items_listbox.insert(tk.END, total_price_item)
        # if total_price_item not in self.selected_items_listbox.get(0, tk.END):
            # Append the total price item to the list
        total_price = f"Total: ${self.total_price:.2f}"
        self.selected_items_listbox.insert(tk.END, total_price_item)

        # Debug: Output current total price
        print(f"Current total price: {self.total_price}")

    def show_base_options(self):
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

        image_filenames = ['images1.jpg', 'images2.jpg', 'images3.jpg', 'images4.jpg', 'images5.jpg']

        for i, base_info in enumerate(base):
            base_name = base_info['Base'].replace("_", " ")
            price = base_info['Price']
            img_path = image_filenames[i % len(image_filenames)]  # Cycle through images
            img = Image.open(img_path)
            img = img.resize((150, 150), Image.Resampling.LANCZOS)  # Resize image
            photo = ImageTk.PhotoImage(img)

            self.base_images.append(photo)  # Keep a reference to avoid garbage collection

            button_text = f"{base_name} - ${price:.2f}"
            command = lambda opt=base_name, prc=price: self.select_base(opt, prc)
            row_num = i // 3  # Determine the row number
            col_num = i % 3  # Determine the column number
            button = tk.Button(self.base_options_frame, text=button_text, image=photo, compound='top', command=command,
                               bg="#40FEBE", highlightthickness=0, highlightbackground="#40FEBE")
            button.image = photo  # Keep reference to image
            button.grid(row=row_num, column=col_num, padx=5, pady=5)

    def show_flavors_options(self):
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

        image_filenames = ['images6.jpg', 'images7.jpg', 'images8.jpg', 'images9.jpg', 'images10.jpg', 'images11.jpg',
                           'images12.jpg', 'images13.jpg', 'images14.jpg']

        for i, flavor_info in enumerate(flavor):
            flavor = flavor_info["Flavor"].replace("_", " ")
            price = flavor_info["Price"]

            img_path = image_filenames[i % len(image_filenames)]  # Cycle through images
            img = Image.open(img_path)
            img = img.resize((100, 100), Image.Resampling.LANCZOS)  # Resize image
            photo = ImageTk.PhotoImage(img)

            self.flavor_images.append(photo)  # Keep a reference to avoid garbage collection

            button_text = f"{flavor} - ${price:.2f}"
            command = lambda opt=flavor, prc=price: self.select_flavor(opt, prc)
            row_num = i // 3  # Determine the row number
            col_num = i % 3  # Determine the column number
            button = tk.Button(self.flavor_options_frame, width=140, height=118, text=button_text, image=photo,
                               compound='top', command=command, state=tk.DISABLED, bg="#40FEBE", highlightthickness=0,
                               highlightbackground="#40FEBE")
            button.image = photo  # Keep reference to image
            button.grid(row=row_num, column=col_num, padx=5, pady=5)

            #tk.Button(self.flavor_options_frame, text=button_text, command=command, width=17, height=4, state=tk.DISABLED).grid(row=row_num, column=col_num, padx=5, pady=5)

    def show_toppings_options(self):
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

        image_filenames = ['images15.jpg', 'images16.jpg', 'images17.jpg', 'images18.jpg', 'images19.jpg',
                           'images20.jpg', 'images21.jpg', 'images22.jpg', 'images23.jpg']

        for i, topping_info in enumerate(topping):
            topping = topping_info["Topping"].replace("_", " ")
            price = topping_info["Price"]

            img_path = image_filenames[i % len(image_filenames)]  # Cycle through images
            img = Image.open(img_path)
            img = img.resize((100, 100), Image.Resampling.LANCZOS)  # Resize image
            photo = ImageTk.PhotoImage(img)

            self.topping_images.append(photo)  # Keep a reference to avoid garbage collection

            button_text = f"{topping} - ${price:.2f}"
            command = lambda opt=topping, prc=price: self.select_topping(opt, prc)
            row_num = i // 3  # Determine the row number
            col_num = i % 3  # Determine the column number
            button = tk.Button(self.topping_options_frame, width=140, height=118, text=button_text, image=photo,
                               compound='top', command=command, state=tk.DISABLED, bg="#40FEBE", highlightthickness=0,
                               highlightbackground="#40FEBE")
            button.image = photo  # Keep reference to image
            button.grid(row=row_num, column=col_num, padx=5, pady=5)

    def select_base(self, base, price):
        # Clear previous base selection if any
        self.selected_base = f"{base} - ${price:.2f}"
        # Remove previously added base from the cart if it exists
        self.selected_items_listbox.delete(0, tk.END)
        # Convert price to Decimal
        price_decimal = decimal.Decimal(price)
        # Add the most recent base to the cart
        self.add_to_cart(base, price_decimal, "Base")
        # Update the total price with the price of the most recent base
        self.total_price = price_decimal
        # Display the total price
        self.display_total_price()
        self.final_base = base

        # Enable flavor buttons
        #for button in self.flavor_options_frame.winfo_children():
            #button.config(state=tk.NORMAL)

    '''def select_flavor(self, flavor, price):
        if self.base_confirmed:
            # Update the selected flavor directly
            self.selected_flavor = f"{flavor} - ${price:.2f}"
            # Call add_to_cart to update the list
            self.add_to_cart(flavor, price, "Flavor")

            # Increment the number of selected flavors
            num_selected_flavors = len(self.selected_items_listbox.get(0, tk.END))

            # If the fifth flavor is selected, automatically confirm flavors
            if num_selected_flavors >= 4:
                self.confirm_flavor()'''

    def select_flavor(self, flavor, price):
        if self.base_confirmed:
            # Clear previous base selection if any
            self.selected_flavor = f"{flavor} - ${price:.2f}"
            # Remove previously added base from the cart if it exists
            self.selected_items_listbox.delete(1, tk.END)
            # Convert price to Decimal
            price_decimal = decimal.Decimal(price)
            # Add the most recent base to the cart
            self.add_to_cart(flavor, price_decimal, "Flavor")
            # Update the total price with the price of the most recent base
            #self.total_price = price_decimal
            # Display the total price
            self.display_total_price()
            self.final_flavor = flavor

            # Enable confirm button
            self.flavor_confirm_button.config(state=tk.NORMAL)

    def select_topping(self, topping, price):
        if self.base_confirmed and self.flavor_confirmed:
            # Enable confirm button
            self.topping_confirm_button.config(state=tk.NORMAL)
            # Check if already 5 toppings selected
            if len(self.selected_toppings) < 5:
                self.selected_toppings.append((topping, price))
                self.add_to_cart(topping, price, "Topping")
            else:
                print("Maximum 5 toppings allowed.")

    def confirm_base(self):
        if self.selected_base:
            # Clear the selected base
            self.selected_base = None
            # Set base confirmation status
            self.base_confirmed = True
            # Disable base buttons
            for button in self.base_options_frame.winfo_children():
                button.config(state=tk.DISABLED)
            #Disable base confirm button
            self.base_confirm_button.config(state=tk.DISABLED)
            # Enable flavor buttons
            for button in self.flavor_options_frame.winfo_children():
                button.config(state=tk.NORMAL)
        else:
            print("Please select a base before confirming.")

    '''def confirm_flavor(self):
        if self.base_confirmed and not self.flavor_confirmed:
            # Set flavor confirmation status
            self.flavor_confirmed = True
            # Enable topping buttons
            for button in self.topping_options_frame.winfo_children():
                button.config(state=tk.NORMAL)'''

    def confirm_flavor(self):
        if self.selected_flavor:
            # Clear the selected base
            self.selected_flavor = None
            # Set base confirmation status
            self.flavor_confirmed = True
            # Disable base buttons
            for button in self.flavor_options_frame.winfo_children():
                button.config(state=tk.DISABLED)

            self.flavor_confirm_button.config(state=tk.DISABLED)
            # Enable flavor buttons
            for button in self.topping_options_frame.winfo_children():
                button.config(state=tk.NORMAL)
        else:
            print("Please select a base before confirming.")

    def confirm_topping(self):
        if self.base_confirmed and self.flavor_confirmed:
            self.topping_confirmed = True
            # Disable confirm button
            self.topping_confirm_button.config(state=tk.DISABLED)
            # Disable topping buttons
            for button in self.topping_options_frame.winfo_children():
                button.config(state=tk.DISABLED)
            self.complete_order_button.config(state=tk.NORMAL)

            # If all selections are confirmed, add items to the cart
            #self.add_to_cart(self.selected_base, None, "Base")
            #self.add_to_cart(self.selected_flavor, None, "Flavor")
            #for topping, price in self.selected_toppings:
                #self.add_to_cart(topping, price, "Topping")

    def display_total_price(self):
        # Update the text of the total label with the current total price
        self.total_label.config(text=f"TOTAL: ${self.total_price:.2f}")

    def reset_order(self):
        # Clear selected items list
        self.selected_items_listbox.delete(0, tk.END)

        # Reset confirmation status
        self.base_confirmed = False
        self.flavor_confirmed = False
        self.topping_confirmed = False

        # Reset selected items variables
        self.selected_base = None
        self.selected_flavor = None
        self.selected_toppings = []

        # Reset total price
        self.total_price = decimal.Decimal('0.0')

        # Reset buttons
        self.base_confirm_button.config(state=tk.NORMAL)
        self.flavor_confirm_button.config(state=tk.DISABLED)
        self.topping_confirm_button.config(state=tk.DISABLED)

        for button in self.base_options_frame.winfo_children():
            button.config(state=tk.NORMAL)

        for button in self.flavor_options_frame.winfo_children():
            button.config(state=tk.DISABLED)

        for button in self.topping_options_frame.winfo_children():
            button.config(state=tk.DISABLED)

        # Display the total price
        self.display_total_price()

    def complete_order(self):
        # Get order information
        order_base = self.final_base
        order_flavor = self.final_flavor
        order_toppings = ', '.join([topping[0] for topping in self.selected_toppings])
        #order_price = float(self.total_price)  # Convert Decimal to float
        order_price = float(self.total_price)  # Convert total price to float
        order_price_str = "{:.2f}".format(order_price)

        global db
        # Insert order into MongoDB collection
        orders = db['orders']
        order_data = {
            "base": order_base,
            "flavor": order_flavor,
            "toppings": order_toppings,
            "price": order_price_str
        }
        orders.insert_one(order_data)

        # Reset order variables
        self.reset_order()

        # Display the total price
        self.display_total_price()

        # Clear selected items list
        self.selected_items_listbox.delete(0, tk.END)

        # Reset confirmation status
        self.base_confirmed = False
        self.flavor_confirmed = False
        self.topping_confirmed = False

        # Reset selected items variables
        self.selected_base = None
        self.selected_flavor = None
        self.selected_toppings = []

        # Reset total price
        self.total_price = decimal.Decimal('0.0')

        # Reset buttons
        self.base_confirm_button.config(state=tk.NORMAL)
        self.flavor_confirm_button.config(state=tk.DISABLED)
        self.topping_confirm_button.config(state=tk.DISABLED)

        for button in self.base_options_frame.winfo_children():
            button.config(state=tk.NORMAL)

        for button in self.flavor_options_frame.winfo_children():
            button.config(state=tk.DISABLED)

        for button in self.topping_options_frame.winfo_children():
            button.config(state=tk.DISABLED)

        self.print_orders()

    def display_most_popular_items(self):

        global db
        orders = db['orders']

        # Aggregate the most popular base
        most_popular_base = orders.aggregate([
            {"$group": {"_id": "$base", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 1}
        ])
        most_popular_base = list(most_popular_base)
        if most_popular_base:
            self.most_popular_base_label.config(
                text=f"Most Popular Base: {most_popular_base[0]['_id'].replace('_', ' ')}")
        else:
            self.most_popular_base_label.config(text=f"Most Popular Base: None")

        # Aggregate the most popular flavor
        most_popular_flavor = orders.aggregate([
            {"$group": {"_id": "$flavor", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 1}
        ])
        most_popular_flavor = list(most_popular_flavor)
        if most_popular_flavor:
            self.most_popular_flavor_label.config(
                text=f"Most Popular Flavor: {most_popular_flavor[0]['_id'].replace('_', ' ')}")
        else:
            self.most_popular_flavor_label.config(text=f"Most Popular Flavor: None")

        # Aggregate the most popular topping
        most_popular_topping = orders.aggregate([
            {"$group": {"_id": "$toppings", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 1}
        ])
        most_popular_topping = list(most_popular_topping)
        if most_popular_topping:
            self.most_popular_topping_label.config(
                text=f"Most Popular Topping: {most_popular_topping[0]['_id'].replace('_', ' ')}")
        else:
            self.most_popular_topping_label.config(text=f"Most Popular Topping: None")

    def give_bad_rating(self):
        # Access the 'ratings' collection using the 'db' attribute
        global db
        ratings = db['ratings']

        # Insert the new rating
        ratings.insert_one({"rating_value": "BAD"})

        # Check the total number of ratings
        total_ratings = ratings.count_documents({})

        # If there are already three ratings, remove the oldest one
        if total_ratings > 3:
            ratings.find_one_and_delete({}, sort=[('_id', 1)])



    def give_ok_rating(self):
        global db
        ratings = db['ratings']
        ratings.insert_one({"rating_value": "OK"})
        total_ratings = ratings.count_documents({})

        if total_ratings > 3:
            ratings.find_one_and_delete({}, sort=[('_id', 1)])


        self.print_ratings()

    def give_great_rating(self):
        global db
        ratings = db['ratings']
        ratings.insert_one({"rating_value": "GREAT"})
        total_ratings = ratings.count_documents({})

        if total_ratings > 3:
            ratings.find_one_and_delete({}, sort=[('_id', 1)])


    def update_recent_ratings(self):
        # Access the 'ratings' collection using the 'db' attribute
        global db
        ratings = db['ratings']

        # Retrieve the most recent 3 ratings from the 'ratings' collection
        recent_ratings_cursor = ratings.find({}, {'rating_value': 1}).sort('_id', -1).limit(3)

        # Extract the rating values from the cursor
        recent_ratings = [rating['rating_value'] for rating in recent_ratings_cursor]

        # Now 'recent_ratings' contains the most recent 3 ratings

    def print_orders(self):
        # Retrieve all documents from the orders collection
        global db
        orders = db['orders']
        all_orders = orders.find()

        print("All orders:")
        # Print each order document
        for order in all_orders:
            print(order)

    def print_ratings(self):
        # Retrieve all documents from the orders collection
        global db
        ratings = db['ratings']
        all_ratings = ratings.find()

        print("All ratings:")
        # Print each order document
        for r in all_ratings:
            print(r)

    def reset_orders_table(self):
        global db
        orders = db['orders']
        orders.delete_many({})

    def reset_ratings_table(self):
        global db
        ratings = db['ratings']
        ratings.delete_many({})



root = tk.Tk()
app = IceCreamShopApp(root)
root.mainloop()

