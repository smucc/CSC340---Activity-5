import tkinter as tk
import mysql.connector
import decimal
from PIL import Image, ImageTk
from tkinter import PhotoImage

class IceCreamShopApp:
    def __init__(self, master):
        self.master = master
        master.title("Ice Cream Shop")
        master.configure(bg="#FFB6C1")

        # Connect to MySQL database
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="20Horses!",
            database="IceCream"
        )


        # Creating frames for each category
        self.base_frame = tk.Frame(master)
        self.flavor_frame = tk.Frame(master)
        self.toppings_frame = tk.Frame(master)
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
        self.selected_items_listbox = tk.Listbox(master, width=50, height=20, font=("Arial", 14))
        self.selected_items_listbox.grid(row=3, column=1, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Create confirm buttons for base, flavor, and topping selection
        self.create_confirm_buttons()

        # Display options for each category
        self.show_base_options()
        self.show_flavors_options()
        self.show_toppings_options()

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

        self.total_price = decimal.Decimal('0.0')
        #self.total_price = 0.0  # Initialize total price variable

    def create_frames_and_dividers(self):
        # Configuring grid rows and columns for flexibility
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1, minsize=300)
        self.master.grid_columnconfigure(2, weight=1, minsize=300)
        self.master.grid_columnconfigure(4, weight=1, minsize=300)

        # Create frame for base options
        self.base_options_frame = tk.Frame(self.master)
        self.base_options_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Create frame for flavor options
        self.flavor_options_frame = tk.Frame(self.master)
        self.flavor_options_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # Create frame for topping options
        self.topping_options_frame = tk.Frame(self.master)
        self.topping_options_frame.grid(row=0, column=4, padx=10, pady=10, sticky="nsew")

        # Create divider frames
        divider1 = tk.Frame(self.master, bg="black", width=2)
        divider1.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky="ns")
        divider2 = tk.Frame(self.master, bg="black", width=2)
        divider2.grid(row=0, column=3, rowspan=3, padx=10, pady=10, sticky="ns")

        divider3 = tk.Frame(self.master, bg="black", width=50)
        divider3.grid(row=2, column=10, columnspan=5, padx=10, pady=10, sticky="ew")

        # Create label to display total price
        # Create label to display total price
        self.total_label = tk.Label(self.master, text="TOTAL: $0.00", font=("Arial", 24))
        self.total_label.grid(row=3, column=15, columnspan=15, padx=50, pady=70, sticky="s")

    def create_confirm_buttons(self):
        # Create confirm buttons for base, flavor, and topping selection
        self.base_confirm_button = tk.Button(self.master, text="Confirm Base", command=self.confirm_base)
        self.base_confirm_button.grid(row=1, column=0, padx=5, pady=5)
        self.flavor_confirm_button = tk.Button(self.master, text="Confirm Flavor", command=self.confirm_flavor, state=tk.DISABLED)
        self.flavor_confirm_button.grid(row=2, column=2, padx=5, pady=5)
        self.topping_confirm_button = tk.Button(self.master, text="Confirm Topping", command=self.confirm_topping, state=tk.DISABLED)
        self.topping_confirm_button.grid(row=2, column=4, padx=5, pady=5)

    def create_reset_button(self):
        self.reset_button = tk.Button(self.master, width=30, height=6, text="Reset Order", font=("Arial", 15), command=self.reset_order)
        self.reset_button.grid(row=3, column=4, padx=10, pady=10, sticky="n")


    def create_complete_order_button(self):
        self.complete_order_button = tk.Button(self.master, width=30, height=6, text = "Complete Order", font=("Arial", 15), command=self.complete_order)
        self.complete_order_button.grid(row=3, column=4, padx=10, pady=10)

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
        cursor = self.mydb.cursor()
        cursor.execute("SELECT Base, Price FROM Base")
        options = cursor.fetchall()
        # num_options = len(options)
        # num_rows = (num_options + 2) // 3  # Number of rows needed for the grid
        image_filenames = ['images1.jpg', 'images2.jpg', 'images3.jpg', 'images4.jpg', 'images5.jpg']

        for i, (base, price) in enumerate(options):
            img_path = image_filenames[i % len(image_filenames)]  # Cycle through images
            img = Image.open(img_path)
            img = img.resize((45, 45), Image.Resampling.LANCZOS)  # Resize image
            photo = ImageTk.PhotoImage(img)

            self.base_images.append(photo)  # Keep a reference to avoid garbage collection

            button_text = f"{base} - ${price:.2f}"
            command = lambda opt=base, prc=price: self.select_base(opt, prc)
            row_num = i // 2  # Determine the row number
            col_num = i % 2  # Determine the column number
            button = tk.Button(self.base_options_frame, text=button_text, image=photo, compound='top', command=command)
            button.image = photo  # Keep reference to image
            button.grid(row=row_num, column=col_num, padx=5, pady=5)

    def show_flavors_options(self):
        cursor = self.mydb.cursor()
        cursor.execute("SELECT Flavor, Price FROM Flavors")
        options = cursor.fetchall()
        num_options = len(options)
        image_filenames = ['images6.jpg', 'images7.jpg', 'images8.jpg', 'images9.jpg', 'images10.jpg', 'images11.jpg', 'images12.jpg', 'images13.jpg', 'images14.jpg']

        for i, (flavor, price) in enumerate(options):
            img_path = image_filenames[i % len(image_filenames)]  # Cycle through images
            img = Image.open(img_path)
            img = img.resize((45, 45), Image.Resampling.LANCZOS)  # Resize image
            photo = ImageTk.PhotoImage(img)

            self.flavor_images.append(photo)  # Keep a reference to avoid garbage collection

            button_text = f"{flavor} - ${price:.2f}"
            command = lambda opt=flavor, prc=price: self.select_flavor(opt, prc)
            row_num = i // 2  # Determine the row number
            col_num = i % 2  # Determine the column number
            button = tk.Button(self.flavor_options_frame, text=button_text, image=photo, compound='top', command=command)
            button.image = photo  # Keep reference to image
            button.grid(row=row_num, column=col_num, padx=5, pady=5)

            #tk.Button(self.flavor_options_frame, text=button_text, command=command, width=17, height=4, state=tk.DISABLED).grid(row=row_num, column=col_num, padx=5, pady=5)

    def show_toppings_options(self):
        cursor = self.mydb.cursor()
        cursor.execute("SELECT Topping, Price FROM Toppings")
        options = cursor.fetchall()
        # num_options = len(options)
        image_filenames = ['images15.jpg', 'images16.jpg', 'images17.jpg', 'images18.jpg', 'images19.jpg',
                           'images20.jpg', 'images21.jpg', 'images22.jpg', 'images23.jpg']

        for i, (topping, price) in enumerate(options):
            img_path = image_filenames[i % len(image_filenames)]  # Cycle through images
            img = Image.open(img_path)
            img = img.resize((45, 45), Image.Resampling.LANCZOS)  # Resize image
            photo = ImageTk.PhotoImage(img)

            self.topping_images.append(photo)  # Keep a reference to avoid garbage collection

            button_text = f"{topping} - ${price:.2f}"
            command = lambda opt=topping, prc=price: self.select_topping(opt, prc)
            row_num = i // 2  # Determine the row number
            col_num = i % 2  # Determine the column number
            button = tk.Button(self.topping_options_frame, text=button_text, image=photo, compound='top', command=command)
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

'''
if __name__ == "__main__":
    root = tk.Tk()
    app = IceCreamShopApp(root)
    root.mainloop()
'''

root = tk.Tk()
app = IceCreamShopApp(root)
root.mainloop()

