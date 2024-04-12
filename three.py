import tkinter as tk
import mysql.connector

class IceCreamShopApp:
    def __init__(self, master):
        self.master = master
        master.title("Ice Cream Shop")
        self.selected_base = ""  # Variable to hold the selected base
        self.selected_flavor = ""  # Variable to hold the selected flavor
        self.selected_toppings = []  # List to hold selected toppings
        self.options = []

        # Connect to MySQL database
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="fantasyape123",
            database="IceCream"
        )

        # Create margin for base options
        self.base_options_margin = tk.Frame(master)
        self.base_options_margin.grid(row=0, column=0)

        # Create confirm button for base selection
        self.base_confirm_button = tk.Button(master, text="Confirm Base", command=self.confirm_base)
        self.base_confirm_button.grid(row=1, column=0)

        # Create column separator
        tk.Frame(master, width=10, height=10, bg="black").grid(row=0, column=1)

        # Create margin for flavor options
        self.flavor_options_margin = tk.Frame(master)
        self.flavor_options_margin.grid(row=0, column=2)

        # Create confirm button for flavor selection
        self.flavor_confirm_button = tk.Button(master, text="Confirm Flavor", command=self.confirm_flavor)
        self.flavor_confirm_button.grid(row=1, column=2)

        # Create another column separator
        tk.Frame(master, width=10, height=10, bg="black").grid(row=0, column=3)

        # Create margin for topping options
        self.topping_options_margin = tk.Frame(master)
        self.topping_options_margin.grid(row=0, column=4)

        # Create confirm button for topping selection
        self.topping_confirm_button = tk.Button(master, text="Confirm Topping", command=self.confirm_topping)
        self.topping_confirm_button.grid(row=1, column=4)

        # Create margin for selected items
        self.selected_items_margin = tk.Frame(master)
        self.selected_items_margin.grid(row=0, column=5)

        # Create listbox to display selected items
        self.selected_items_listbox = tk.Listbox(self.selected_items_margin, width=30, height=10)
        self.selected_items_listbox.pack(side=tk.LEFT)

        # Display options for each category
        self.show_base_options()
        self.show_flavors_options()
        self.show_toppings_options()

        # State variables to track confirmation status
        self.base_confirmed = False
        self.flavor_confirmed = False
        self.topping_confirmed = False

    def show_base_options(self):
        cursor = self.mydb.cursor()
        cursor.execute("SELECT Base, Price FROM Base")
        self.options = cursor.fetchall()
        num_options = len(self.options)
        num_rows = (num_options + 2) // 3  # Number of rows needed for the grid
        for i, (base, price) in enumerate(self.options):
            button_text = f"{base} - ${price:.2f}"
            command = lambda opt=base, prc=price: self.select_base(opt, prc)
            row_num = i // 3  # Determine the row number
            col_num = i % 3   # Determine the column number
            tk.Button(self.base_options_margin, text=button_text, command=command, width=17, height=4).grid(row=row_num, column=col_num, padx=5, pady=5)

    def show_flavors_options(self):
        cursor2 = self.mydb.cursor()
        cursor2.execute("SELECT Flavor, Price FROM Flavors")
        self.options = cursor2.fetchall()
        num_options = len(self.options)
        num_rows = (num_options + 2) // 3  # Number of rows needed for the grid
        for i, (flavor, price) in enumerate(self.options):
            button_text = f"{flavor} - ${price:.2f}"
            command = lambda opt=flavor, prc=price: self.select_flavor(opt, prc)
            row_num = i // 3  # Determine the row number
            col_num = i % 3   # Determine the column number
            tk.Button(self.flavor_options_margin, text=button_text, command=command, width=17, height=4).grid(row=row_num, column=col_num, padx=5, pady=5)

    def show_toppings_options(self):
        cursor2 = self.mydb.cursor()
        cursor2.execute("SELECT Topping, Price FROM Toppings")
        self.options = cursor2.fetchall()
        num_options = len(self.options)
        num_rows = (num_options + 2) // 3  # Number of rows needed for the grid
        for i, (topping, price) in enumerate(self.options):
            button_text = f"{topping} - ${price:.2f}"
            command = lambda opt=topping, prc=price: self.select_topping(opt, prc)
            row_num = i // 3  # Determine the row number
            col_num = i % 3   # Determine the column number
            tk.Button(self.topping_options_margin, text=button_text, command=command, width=17, height=4).grid(row=row_num, column=col_num, padx=5, pady=5)

    def select_base(self, base, price):
        # Clear previous base selection if any
        if self.selected_base:
            self.selected_base = ""
            self.selected_items_listbox.delete(0, tk.END)
            self.base_confirmed = False

        # Update the selected base directly
        self.selected_base = f"{base} - ${price:.2f}"
        # Update the listbox display
        self.add_to_cart(base, price, "Base")

    def select_flavor(self, flavor, price):
        if self.base_confirmed and not self.flavor_confirmed:
            # Update the selected flavor directly
            self.selected_flavor = f"{flavor} - ${price:.2f}"
            # Call add_to_cart to update the list
            self.add_to_cart(flavor, price, "Flavor")

    def select_topping(self, topping, price):
        if self.base_confirmed and self.flavor_confirmed and not self.topping_confirmed:
            # Check if already 5 toppings selected
            if len(self.selected_toppings) < 5:
                self.selected_toppings.append((topping, price))
                self.add_to_cart(topping, price, "Topping")
            else:
                print("Maximum 5 toppings allowed.")

    def confirm_base(self):
        # Set base confirmation status
        self.base_confirmed = True
        # Update the listbox with the confirmed base selection
        self.add_to_cart(self.selected_base, None, "Base")

    def confirm_flavor(self):
        if self.base_confirmed:
            self.flavor_confirmed = True

    def confirm_topping(self):
        if self.base_confirmed and self.flavor_confirmed:
            self.topping_confirmed = True
            # If all selections are confirmed, add items to the cart
            self.add_to_cart(self.selected_base, None, "Base")
            self.add_to_cart(self.selected_flavor, None, "Flavor")
            for topping, price in self.selected_toppings:
                self.add_to_cart(topping, price, "Topping")

    def add_to_cart(self, option, price, category):
        print("Adding to cart:", option, price, category)
        if price is not None:
            item = f"{option} - ${price:.2f} ({category})"
        else:
            item = f"{option} ({category})"
        # Remove existing item if any
        for i in range(self.selected_items_listbox.size()):
            item_text = self.selected_items_listbox.get(i)
            if f"({category})" in item_text:
                self.selected_items_listbox.delete(i)
                break
        self.selected_items_listbox.insert(tk.END, item)


root = tk.Tk()
app = IceCreamShopApp(root)
root.mainloop()
