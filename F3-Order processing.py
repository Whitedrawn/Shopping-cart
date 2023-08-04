"""
Author : Sergiu Macsim 001120364
Date finished : 01/02/2021

F3 - Order Processing
- Shopping basket
- Check-out
- Payment
- Generate sales receipt

"""

#imports
import tkinter as tk
from tkinter import ttk
from functools import partial
from tkinter import messagebox
import sqlite3

#creating a dummy database to demonstrate my features
connection = sqlite3.connect("products.db")
cursor=connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS products (name TEXT, price REAL)")

# function for the add event handler button present in Shooping frame
def add_product(product):
    if product in added_products:
        added_products[product]+=products[product]
    else:
        added_products.update({product:products[product]})
    print(added_products)
# function for deleting items in the basket


#a class used to to add elements to the database
class AddProductDB:
    def __init__(self,pname,price):
        self.name=pname
        self.price=price
        self.add()

    def add(self):
        cursor.execute("INSERT INTO products VALUES (?,?)",(self.name,self.price))


#main controller of the app that cycles through frames
class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):

        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self,width=700, height=550)
        # container['width'] = 700
        # container['height'] = 550
        container.grid_propagate(False)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (Shopping, Basket,CheckOut,Payment,Receipt):
            frame = F(container, self)

            # initializing frame of that object from
            # Shopping, Basket,CheckOut,Payment,Receipt respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        # first window frame Shopping
        self.show_frame(Shopping)



    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    # used from others classes to get a certain frame in order to use it's methods
    def get_frame(self,cont):
        frame=self.frames[cont]
        return frame

    def calc_total_checkout(self,total_received):
        total_checkout = total_received
        self.total_checkout = total_checkout
        return self.total_checkout
    #method used to delete products from the basket
    def delete_product(self,product):
        pass
        if product in added_products:
            del added_products[product]
        self.added_products=added_products
        self.get_frame(Basket).update_basket()
        print(added_products)

#first Frame used to add products in the basket
class Shopping(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # label of frame
        label = ttk.Label(self, text="Products", font=font_large)

        # putting the grid in its place by using
        # grid
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Basket->",
                             command=lambda: [controller.get_frame(Basket).update_basket(),controller.show_frame(Basket)])

        # putting the button in its place by
        # using grid
        button1.grid(row=0, column=20, padx=10, pady=10)

        y_coordinate = 100
        j = 0
        #takes each products form the database and creates a label,a price and an add button
        for product in products:
            # Stores the product name
            label_text = product
            # Stores the product price
            label_price = products[product], '£'
            #creating the label for each product name
            lbl_dict[j] = tk.Label(self,
                                   text=label_text,
                                   font=font_small)
            lbl_dict[j].place(x=10, y=y_coordinate)
            # This creates the label for the price of each product
            lbl_dict[j] = tk.Label(self,
                                   text=label_price,
                                   font=font_small)
            lbl_dict[j].place(x=100, y=y_coordinate)
            #adds a button used for adding products in the basket
            lbl_dict[j] = tk.Button(self,
                                    text='Add',
                                    font=font_small,
                                    command=partial(add_product, product))
                             #calls add_product funtion from above to update the added products dictionary and value
            lbl_dict[j].place(x=150, y=y_coordinate)
            y_coordinate += 30
            j += 1
#second frame - Basket
class Basket(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


        label = ttk.Label(self, text="Shopping Basket", font=font_large)
        label.grid(row=0, column=4, padx=10, pady=10)
        # button used to navigate to previous frame
        button1 = ttk.Button(self, text="<-Continue Shopping",
                             command=lambda: controller.show_frame(Shopping))

        # putting the button in its place
        # by using grid
        button1.grid(row=0, column=1, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        #button used to navigate to the next step : check-out
        #it also updates CheckOut frame with the updated price if we decide to go back and add more
        button2 = ttk.Button(self, text="Check-out->",
                             command=lambda: [controller.get_frame(CheckOut).update_checkout_transport(self.total),controller.get_frame(CheckOut).update_checkout(self.total),controller.show_frame(CheckOut)])

        # putting the button in its place by
        # using grid
        button2.grid(row=0, column=20, padx=10, pady=10)
        self.controller=controller
    #method used to populate the frame with the added products
    #it is also used to refresh the entire frame with the updated products
    def update_basket(self):
        y2_coordinate = 100
        i = 0
        total = 0
        w=0
        for widget in self.winfo_children():
            if w>2:
                widget.destroy()
            w+=1
        for added_product in added_products:
            label_text = added_product
            label_price = added_products[added_product], '£'
            #product name label
            lbl_dict[i] = tk.Label(self,
                                    text=label_text,
                                    font=font_small)
            lbl_dict[i].place(x=140, y=y2_coordinate)
            #price label
            lbl_dict[i] = tk.Label(self,
                                    text=label_price,
                                    font=font_small)
            lbl_dict[i].place(x=230, y=y2_coordinate)
            #delete button
            btn_dict[i] = tk.Button(self,
                                   text='Delete',
                                   font=font_small,
                                   command=lambda:[self.controller.delete_product(added_product)])
            btn_dict[i].place(x=320, y=y2_coordinate)

            y2_coordinate += 30
            i += 1
            #add the value of each product added into a total value
            total += added_products[added_product]
        label_total = 'Total', 'value', '=', total, '£'
        self.total=total
        # total value label
        Total = tk.Label(self,
                            text=label_total,
                            font=font_small)
        Total.place(x=160, y=300)



    # third window frame CheckOut
class CheckOut(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Check-out", font=font_large)
        label.grid(row=0, column=4, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="<-Basket",
                             command=lambda: controller.show_frame(Basket))

        # putting the button in its place by
        # using grid
        button1.grid(row=0, column=1, padx=10, pady=10)

        #Delivery
        #each option buttons refreshes the windows and updates the price
        delivery = tk.Label(self,
                         text="Choose a delivery option",
                         font=font_large)
        delivery.place(x=140, y=100)

        # delivery option 1 (Default)
        delivery_op1 = tk.Label(self,
                            text="Normal delivery - 3-5 days (Def)",
                            font=font_small)
        delivery_op1.place(x=50, y=160)
        delivery_op1 = tk.Label(self,
                                text="Free",
                                font=font_small)
        delivery_op1.place(x=300, y=160)
        btn_delivery_op1 = tk.Button(self,
                                text='Choose',
                                font=font_small,
                                command=lambda: [controller.get_frame(CheckOut).update_checkout_transport(self.discount),
                                                 controller.get_frame(Receipt).update_receipt_transport(self.discount+10),
                                                 controller.show_frame(CheckOut)])
        btn_delivery_op1.place(x=360, y=160)

        # delivery option 2
        delivery_op2 = tk.Label(self,
                                text="Next day delivery",
                                font=font_small)
        delivery_op2.place(x=50, y=190)
        delivery_op2 = tk.Label(self,
                                text="5 £",
                                font=font_small)
        delivery_op2.place(x=300, y=190)
        btn_delivery_op2 = tk.Button(self,
                                     text='Choose',
                                     font=font_small,
                                     command=lambda: [controller.get_frame(CheckOut).update_checkout_transport(self.discount+5),
                                                      controller.get_frame(Receipt).update_receipt_transport(self.discount+5),
                                                      controller.show_frame(CheckOut)])
        btn_delivery_op2.place(x=360, y=190)

        # delivery option 3
        delivery_op3 = tk.Label(self,
                                text="Same day delivery",
                                font=font_small)
        delivery_op3.place(x=50, y=220)
        delivery_op3 = tk.Label(self,
                                text="10 £",
                                font=font_small
                                )
        delivery_op3.place(x=300, y=220)
        btn_delivery_op3 = tk.Button(self,
                                     text='Choose',
                                     font=font_small,
                                     command=lambda: [controller.get_frame(CheckOut).update_checkout_transport(self.discount+10),
                                                      controller.get_frame(Receipt).update_receipt_transport(self.discount+10),
                                                      controller.show_frame(CheckOut)])
        btn_delivery_op3.place(x=360, y=220)

        #button used to apply a discount (10% used as an example for the feature)
        btn_discount = tk.Button(self,
                                     text='Apply discount',
                                     font=font_small,
                                     command=lambda: [controller.get_frame(CheckOut).discount_value(
                                         self.total_checkout - (0.1*self.total_checkout)),
                                         controller.get_frame(CheckOut).update_checkout_transport(self.discount),
                                         controller.get_frame(Receipt).discount_value_receipt(
                                             self.total_checkout - (0.1 * self.total_checkout)),
                                         controller.get_frame(Receipt).update_receipt_transport(self.discount),
                                         controller.show_frame(CheckOut)])
        btn_discount.place(x=300, y=250)

        btn_Pay = tk.Button(self,
                             text="Pay",
                             font=font_small,
                             command=lambda: controller.show_frame(Payment))

        btn_Pay.place(x=340,y=410)

    #updates normal value without discount or transport
    def update_checkout(self,total_checkout):
        self.total_checkout=total_checkout
        label_total_checkout = 'Total', 'value', '=', self.total_checkout,'£'
        Total_checkout=tk.Label(self,
                                text=label_total_checkout,
                                font=font_small)
        Total_checkout.place(x=40,y=350)
    #updates the normal value + discount
    def discount_value(self, discount):
        self.discount=0
        self.discount = discount
        label_total_discount = 'Total', 'value', '(','after', 'discount',')', '=', self.discount, '£'
        Total_checkout = tk.Label(self,
                                  text=label_total_discount,
                                  font=font_small)
        Total_checkout.place(x=40, y=380)
    #updates the discounted value + transport
    def update_checkout_transport(self,transport):
        self.total_checkout_transport = transport
        label_total_checkout_transport = 'Total', 'value','+','transport', '=', self.total_checkout_transport, '£'
        Total_checkout = tk.Label(self,
                                  text=label_total_checkout_transport,
                                  font=font_small)
        Total_checkout.place(x=40, y=410)


#Payment class used to get info from the user and check the
class Payment(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Payment", font=font_large)
        label.grid(row=0, column=4, padx=10, pady=10)

        #button used to navigate to previous window
        button1 = ttk.Button(self, text="<-Check-out",
                             command=lambda: controller.show_frame(CheckOut))
        button1.grid(row=0, column=1, padx=10, pady=10)
        #button used to navigate forward
        button2 = ttk.Button(self, text="Place Order",
                             command=lambda: [controller.get_frame(Receipt).update_receipt(),
                                              controller.show_frame(Receipt)])
        self.button2=button2

        #Label and entry for name
        label_holder_name=ttk.Label(self,text="Please enter your name present on the credit/debit card",font=font_small)
        label_holder_name.place(x=30,y=80)
        holder_name=ttk.Entry(self)
        holder_name.place(x=30,y=110)
        self.holder_name=holder_name
        #Label and entry for card number
        label_card_number = ttk.Label(self, text="Please enter your credit card number",
                                      font=font_small)
        label_card_number.place(x=30, y=140)
        entry_card_number = ttk.Entry(self)
        entry_card_number.place(x=30, y=170)
        self.entry_card_number=entry_card_number
        #Label and entry for date

        label_exp_date = ttk.Label(self, text="Please enter the expiration date",
                                      font=font_small)
        label_exp_date.place(x=30, y=200)
        entry_exp_date = ttk.Entry(self)
        entry_exp_date.place(x=30, y=230)
        self.entry_exp_date=entry_exp_date
        # Label and entry for CVV

        label_cvv = ttk.Label(self, text="Please enter CVV",
                                      font=font_small)
        label_cvv.place(x=30, y=260)
        entry_cvv= ttk.Entry(self)
        entry_cvv.place(x=30, y=290)
        self.entry_cvv=entry_cvv

        #Button for VISA CHECK
        btn_visa = tk.Button(self,
                                text='VISACheck',
                                font=font_small,
                                command=lambda:self.visa_check())
        btn_visa.place(x=40, y=320)
    #method used to check if every field has user information
    def visa_check(self):
        if (len(self.entry_card_number.get()) == 0 or len(self.entry_exp_date.get())==0
            or len(self.entry_cvv.get())==0 or len(self.holder_name.get())==0):
            messagebox.showinfo('Error', 'Please enter valid info in every field')

        else:
        # if the conditions are met the button for advancing is placed on the window
            self.button2.grid(row=0, column=20, padx=10, pady=10)
#Receipt
class Receipt(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Receipt", font=font_large)
        label.grid(row=0, column=5, padx=10, pady=10)

        #button used to navigate to previous window
        button1 = ttk.Button(self, text="<-Payment",
                             command=lambda: controller.show_frame(Payment))
        button1.grid(row=0, column=1, padx=30, pady=10)
        #button used to call print_receipt method that creates a copy for the receipt for the customer
        btn_print = ttk.Button(self, text="Print",
                             command=lambda: self.print_receipt())
        btn_print.grid(row=0, column=6, padx=200, pady=10)
    #method used to create, display and update the products that were purchased and a details about the price paid
    def update_receipt(self):
        y2_coordinate = 100
        i = 0
        total = 0
        f = open("Receipt.txt", "r+")
        f.write("Receipt"+'\n')
        for added_product in added_products:
            label_text = added_product
            label_price = added_products[added_product], '£'
            f.write(str(label_text)+':')
            f.write(str(label_price[0])+'\n')
            lbl_dict[i] = tk.Label(self,
                                    text=label_text,
                                    font=font_small)
            lbl_dict[i].place(x=140, y=y2_coordinate)
            lbl_dict[i] = tk.Label(self,
                                    text=label_price,
                                    font=font_small)
            lbl_dict[i].place(x=230, y=y2_coordinate)

            y2_coordinate += 30
            i += 1
            total += added_products[added_product]
        label_total = 'Total', 'value', '=', total, '£'
        self.total=total
        Total = tk.Label(self,
                            text=label_total,
                            font=font_small)
        Total.place(x=140, y=250)
        f.write('\n'+'Total value = '+str(total) +' £'+ '\n')
        f.write('\n' +'Total value (after discount) = '+ str(self.discount) +' £'+ '\n')
        f.write('\n' +'Total value + transport = '+ str(self.total_checkout_transport) +' £'+ '\n')
        f.close()
    # method used to update part of the price details
    def discount_value_receipt(self, discount):

        self.discount=0
        self.discount = discount
        label_total_discount = 'Total', 'value', '(','after', 'discount',')', '=', self.discount, '£'
        Total_checkout = tk.Label(self,
                                  text=label_total_discount,
                                  font=font_small)
        Total_checkout.place(x=80, y=280)

    # method used to update part of the price details
    def update_receipt_transport(self,transport):

        self.total_checkout_transport = transport
        label_total_checkout_transport = 'Total', 'value','+','transport', '=', self.total_checkout_transport, '£'

        Total_checkout = tk.Label(self,
                                  text=label_total_checkout_transport,
                                  font=font_small)
        Total_checkout.place(x=80, y=310)

    #method used to make a customer copy of the receipt that could be used to print the receipt
    def print_receipt(self):
        open("Customer_copy.txt", "w").writelines([l for l in open("Receipt.txt").readlines() if "" in l])


# declare some empty dictionaries for widgets and products

k=0
lbl_dict = dict()
btn_dict = dict()

total_checkout=0

#instances of the AddProductDB class used to populate the database with some examples
toyCar = AddProductDB("Toy car",20)
doll= AddProductDB("Doll",15)
teddyBear= AddProductDB("Teddy bear",30)
fireTruck= AddProductDB("Fire truck",35)

#an empty dic used to store the basket content
added_products=dict()

# fonts
font_large = ('Georgia',24,'bold')
font_small = ('Georgia','12')

# an empty dictionary for products where all the data from the database will go
products=dict()
# extracting the data from the database
databaseProducts=cursor.execute("SELECT name, price FROM products").fetchall()

# populating the dictionary with the elements form the database
for pro in databaseProducts:
    products.update({pro[0]:pro[1]})

app = tkinterApp()
app.mainloop()