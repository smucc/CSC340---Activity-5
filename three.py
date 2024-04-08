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

        # Create margin for flavor options
        self.flavor_options_margin = tk.Frame(master)
        self.flavor_options_margin.grid(row=0, column=1)

        # Create margin for topping options
        self.topping_options_margin = tk.Frame(master)
        self.topping_options_margin.grid(row=0, column=2)

        # Create margin for selected items
        self.selected_items_margin = tk.Frame(master)
        self.selected_items_margin.grid(row=0, column=3)

        # Create listbox to display selected items
        self.selected_items_listbox = tk.Listbox(self.selected_items_margin, width=30, height=10)
        self.selected_items_listbox.pack(side=tk.LEFT)

        # Display options for each category
        self.show_base_options()
        self.show_flavors_options()
        self.show_toppings_options()

    def show_base_options(self):
        cursor = self.mydb.cursor()
        cursor.execute("SELECT Base, Price FROM Base")
        self.options = cursor.fetchall()
        for i, (base, price) in enumerate(self.options):
            button_text = f"{base} - ${price:.2f}"
            command = lambda opt=base, prc=price: self.select_base(opt, prc)
            tk.Button(self.base_options_margin, text=button_text, command=command, width=30, height=4).grid(row=i, column=0, padx=5, pady=5)

    def show_flavors_options(self):
        cursor2 = self.mydb.cursor()
        cursor2.execute("SELECT Flavor, Price FROM Flavors")
        self.options = cursor2.fetchall()
        for i, (flavor, price) in enumerate(self.options):
            button_text = f"{flavor} - ${price:.2f}"
            command = lambda opt=flavor, prc=price: self.select_flavor(opt, prc)
            tk.Button(self.flavor_options_margin, text=button_text, command=command, width=30, height=4).grid(row=i,
                                                                                                            column=0,
                                                                                                            padx=5,
                                                                                                            pady=5)

    def show_toppings_options(self):
        cursor2 = self.mydb.cursor()
        cursor2.execute("SELECT Topping, Price FROM Toppings")
        self.options = cursor2.fetchall()
        for i, (topping, price) in enumerate(self.options):
            button_text = f"{topping} - ${price:.2f}"
            command = lambda opt=topping, prc=price: self.select_topping(opt, prc)
            tk.Button(self.topping_options_margin, text=button_text, command=command, width=30, height=4).grid(row=i,
                                                                                                              column=0,
                                                                                                              padx=5,
                                                                                                              pady=5)

    def select_base(self, base, price):
        # Update the selected base directly
        self.selected_base = f"{base} - ${price:.2f}"
        # Call add_to_cart to update the list
        self.add_to_cart(base, price, "Base")

    def select_flavor(self, flavor, price):
        # Update the selected flavor directly
        self.selected_flavor = f"{flavor} - ${price:.2f}"
        # Call add_to_cart to update the list
        self.add_to_cart(flavor, price, "Flavor")

    def select_topping(self, topping, price):
        # Check if already 5 toppings selected
        if len(self.selected_toppings) < 5:
            self.selected_toppings.append((topping, price))
            self.add_to_cart(topping, price, "Topping")
        else:
            print("Maximum 5 toppings allowed.")

    def add_to_cart(self, option, price, category):
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
