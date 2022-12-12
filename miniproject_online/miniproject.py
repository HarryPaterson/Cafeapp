# Cafe App

from logging import exception
import pickle
import pymysql
from time import sleep
from datetime import datetime



try:
    connection = pymysql.connect(
    host="localhost",
    user="root",
    password="mysql_pass",
    db="mini_project"
    )
    print ("\n*Connected to cafe's database*")
except pymysql.OperationalError as e:
    print(f"\nERROR: Unable to successfully connect to Database.\n{e}")
    print("Please check database connection. Quitting application...\n")
    quit()
sleep(1)


def print_product_menu():
    print("\nProduct Menu")
    print("Press 0 to return to main menu ")
    print("Press 1 to view products list")
    print("Press 2 to add a new product")
    print("Press 3 to update a products details")
    print("Press 4 to delete a product")
    print("Press 5 to update a products quantity\n")


def print_couriers_menu():
    print("\nCouriers Menu")
    print("Press 0 to return to main menu")
    print("Press 1 to view couriers")
    print("Press 2 to add a new courier")
    print("Press 3 to update a courier")
    print("Press 4 to delete a courier\n")


def print_orders_menu():
    print("\nOrders Menu")
    print("Press 0 to return to main menu")
    print("Press 1 to view orders")
    print("Press 2 to create a new order")
    print("Press 3 to update order status") 
    print("Press 4 to update order details")
    print("Press 5 to delete an order\n")

def print_export_menu():
    print("\nExport Menu")
    print("Press 0 to return to main menu")
    print("Press 1 to export products")
    print("Press 2 to export couriers")
    print("Press 3 to export orders\n")

def print_main_menu():
    print("\nMain Menu")
    print("Press 0 to exit")
    print("Press 1 for products")
    print("Press 2 for couriers")
    print("Press 3 for orders")
    print("Press 4 to export database\n")


def main_menu():
    while True:
        try:
            print_main_menu()
            option = int(input("Select option: "))
        except ValueError:
            print("ERROR: try again numnuts.")
            continue
        if option == 0:
            print("\nExiting App...")
            quit()
        elif option not in range(5):
            print(
                f"ERROR: can you count dumb dumb?."
            )
            continue
        while option == 1:
            print_product_menu()
            try:
                product_menu_choice = int(input("Select option: "))
            except ValueError:
                print("ERROR: You entered a letter value. Please enter a number option.")
                continue
            match product_menu_choice:
                case 0:
                    break
                case 1:
                    view_table("products")
                case 2:
                    add_new_product()
                case 3:
                    update_product()
                case 4:
                    delete_item("products")
                case 5:
                    update_product_quantity()
                case _:
                    print(f"ERROR: The number option you have input ({option}) does not exist. Please view the options and choose accordingly.")
        
        while option == 2:
            print_couriers_menu()
            try:
                courier_menu_choice = int(input("Select option: "))
            except ValueError:
                print("Please enter a valid number option!")
                continue
            match courier_menu_choice:
                case 0:
                    break
                case 1:
                    view_table("couriers")
                case 2:
                    add_new_courier()
                case 3:
                    update_courier()
                case 4:
                    delete_item("couriers")
                case _:
                    print(
                        f"ERROR: The number option you have input ({option}) does not exist. Please view the options and choose accordingly."
                    )

        while option == 3:
            print_orders_menu()
            try:
                orders_menu_choice = int(input("Select option: "))
            except ValueError:
                print("Please enter a valid number option!")
                continue
            match orders_menu_choice:
                case 0:
                    break
                case 1:
                    view_table("orders")
                case 2:
                    add_new_order()
                case 3:
                    update_order_status()
                case 4:
                    update_order_details()
                case 5:
                    delete_item("orders")
                case _:
                    print(
                    f"ERROR: The number option you have input ({option}) does not exist. Please view the options and choose accordingly."
                )

        while option == 4:
            print_export_menu()
            try:
                export_menu_choice = int(input("Select option: "))
            except ValueError:
                print("Please enter a valid number option!")
                continue
            match export_menu_choice:
                case 0:
                    break
                case 1:
                    export_to_dat("products")
                case 2:
                    export_to_dat("couriers")
                case 3:
                    export_to_dat("orders")


def view_table(table):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    result = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    column_names_string = ", ".join(column_names).title()
    if not result:
        print(f"{table} table is empty".capitalize())
    else:
        if table == "products":
            print(f"\n[Loading {table}] How would you like the list to be displayed?")
            print("Press 0 to go back")
            print("Press 1 to sort by name")
            print("Press 2 to sort by price")
            print("Press 3 to sort by ID")
            print("Press 4 to sort by quantity")
            try:
                order_by_option = int(input("Select option: "))
            except ValueError:
                print("ERROR: You have input a letter value where a number option is required.")
                main_menu()
            
            match order_by_option:
                case 0:
                    main_menu()
                case 1:
                    order_by_query("name", "products", column_names_string)
                case 2:
                    order_by_query("price", "products", column_names_string)
                case 3:
                    order_by_query("products_id", "products", column_names_string)
                case 4:
                    order_by_query("quantity", "products", column_names_string)
                case _:
                    print(f"ERROR: That number option ({order_by_option}) does not exist.")
                    main_menu()
        
        elif table == "couriers":
            print(f"\n[Loading {table}] How would you like the list to be displayed?")
            print("Press 0 to go back")
            print("Press 1 to sort by name")
            print("Press 2 to sort by phone number")
            print("Press 3 to sort by ID")
            try:
                order_by_option = int(input("Select an option to view list sorted, or enter 0 to exit: "))
            except ValueError:
                print("ERROR: You have input a letter value where a number option is required.")
                main_menu()
            
            match order_by_option:
                case 0:
                    main_menu()
                case 1:
                    order_by_query("name", "couriers", column_names_string)
                case 2:
                    order_by_query("phone_number", "couriers", column_names_string)
                case 3:
                    order_by_query("couriers_id", "couriers", column_names_string)
                case _:
                    print(f"ERROR: That number option ({order_by_option}) does not exist.")
                    main_menu()

        elif table == "orders":
            print(f"\n[Loading {table}] How would you like the list to be displayed?")
            print("Press 0 to go back")
            print("Press 1 to sort by name")
            print("Press 2 to sort by address")
            print("Press 3 to sort by phone number")
            print("Press 4 to sort by courier")
            print("Press 5 to sort by status")
            print("Press 6 to sort by product")
            print("Press 7 to sort by ID")
            print("Press 8 to sort by time created")
            try:
                order_by_option = int(input("Select an option to view list sorted, or enter 0 to exit: "))
            except ValueError:
                print("ERROR: You have input a letter value where a number option is required.")
                main_menu()
            
            match order_by_option:
                case 0:
                    main_menu()
                case 1:
                    order_by_query("customer_name", "orders", column_names_string)
                case 2:
                    order_by_query("customer_address", "orders", column_names_string)
                case 3:
                    order_by_query("customer_address", "orders", column_names_string)
                case 4:
                    order_by_query("couriers_id", "orders", column_names_string)
                case 5:
                    order_by_query("status_id", "orders", column_names_string)
                case 6:
                    order_by_query("products_id", "orders", column_names_string)
                case 7:
                    order_by_query("orders_id", "orders", column_names_string)
                case 8:
                    order_by_query("time_created", "orders", column_names_string)
                case _:
                    print(f"ERROR: That number option ({order_by_option}) does not exist.")
                    main_menu()

        elif table == "orders_status":
            order_by_query("status_id", "orders_status", column_names_string)
                
    cursor.close()


def order_by_query(column, table, column_names_string):
    sql = f"SELECT * FROM {table} ORDER BY {column}"
    result = retrieve_fetchall(sql)
    print(f"\n({column_names_string})")
    if table == "orders":
        for item in result:
            print (f"({item[0]}, {item[1]}, {item[2]}, {item[3]}, {item[4]}, {item[5]}, '{item[6]}', {item[7]})")
    else:
        for item in result:
            print(item)
    print(f"Number of items: {len(result)}")
    print(f"\n(Results were ordered by {column})")


def add_new_product():
    try:
        cursor = connection.cursor()
        product_name = input("Type the name of product to add: ").title().strip()
        product_price = float(input("Type the price of the product: "))
        product_quantity = int(input("Type the number quantity of the product: "))
        if not product_name:
            print("ERROR: Product name field cannot be blank.")
            return

        sql = f"INSERT INTO products (name, price, quantity) VALUES (%s,%s,%s)"
        cursor.execute(sql, (product_name, product_price, product_quantity))
        print(f"\n{product_name} successfully added to products.")
        connection.commit()
        cursor.close()

    except ValueError:
        print(f"ERROR: Please input the correct value type for the associated field.\nExample: Product price must be int or float")


def add_new_courier():
    try:
        cursor = connection.cursor()
        courier_name = input("Type the name of courier to add: ").title().strip()
        courier_phone = input("Type the phone number of the courier: ").strip()
        if not courier_name or not courier_phone:
            print("ERROR: When adding a new courier, fields cannot be left blank")
            return
        
        sql = f"INSERT INTO couriers (name, phone_number) VALUES (%s,%s)"
        cursor.execute(sql, (courier_name, courier_phone))
        print(f"\n{courier_name} successfully added")
        connection.commit()
        cursor.close()

    except ValueError:
        print(f"ERROR: Please input the correct value type for the associated field.")


def add_new_order():
    try:
        cursor = connection.cursor()
        customer_name = input("Type customer name: ").title().strip()
        customer_address = input("Type customer address: ").title().strip()
        customer_phone_number = input("Type customer's phone number: ").strip()
        if not customer_name or not customer_address or not customer_phone_number:
            print(f"ERROR: Input cannot be blank.")
            return

        view_table("products")
        products_input = input("Type ID of products you wish to order, seperated by commas: ")
        removed_spaces = products_input.replace(" ","")
        listed_version = removed_spaces.split(",")
        products_list_chosen = []
        for number in listed_version:
            cursor.execute(f"SELECT * FROM mini_project.products WHERE products_id = {number}")
            products_choice = cursor.fetchone()
            product_quantity = products_choice[3]
            product_name = products_choice[1]
            if product_quantity == 0:
                print(f"A product you have tried to order ({product_name}) is out of stock. Please order products that have quantity greater than 0.")
                return

            products_list_chosen.append(products_choice)
        print(f"\n*{products_list_chosen} added to order*")

        view_table("couriers")
        courier_input = int(input("Type ID of courier you wish to use: "))
        cursor.execute(f"SELECT name FROM mini_project.couriers WHERE couriers_id = {courier_input}")
        courier_choice = cursor.fetchone()[0]
        print(f"\n*{courier_choice} chosen as courier*\n")

        try:
            for number in listed_version:
                sql = f"UPDATE products SET quantity = quantity - 1 WHERE products_id = {number}"
                cursor = connection.cursor()
                cursor.execute(sql)
        except pymysql.OperationalError:
            print("Error: There was not enough stock of a product to perform your order.")
            connection.rollback()
            return
        else:
            connection.commit()
        
        sql = f"""INSERT INTO mini_project.orders (customer_name, customer_address, customer_phone, couriers_id, status_id, products_id, time_created) 
        VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql, (customer_name, customer_address, customer_phone_number, courier_input, 1, products_input, datetime.now()))
        connection.commit()
        cursor.close()
        print("Order successfully created! Order is being prepared.")

        for number in listed_version:    
            sql = f"SELECT quantity, name FROM products WHERE products_id = {number}"
            result = retrieve_fetchone(sql)
            new_quantity = result[0]
            product_name = result[1]
            print(f"As a result of this order, quantity of {product_name} has been reduced to {new_quantity}.")

    except ValueError:
        print("ERROR: Please enter correct number associated with courier.")
    except IndexError:
        print("ERROR: No such number item exists.")
    except TypeError:
        print("ERROR: Invalid entry.")


def update_product():
    try:
        view_table("products")
        sql = f"SELECT COUNT(*) FROM products"
        check_empty = retrieve_fetchone(sql)
        if check_empty[0] == 0:
            print("Exiting update menu")
            return

        user_choice = int(input("Type the product_id of item you wish to update: "))
        sql = f"SELECT * FROM products WHERE products_id = {user_choice}"
        old_item = retrieve_fetchone(sql)
        if not old_item:
            print(f"ERROR: The products_id you have entered ({user_choice}) could not be found")
            return
        
        old_name = old_item[1]
        old_price = old_item[2]
        product_id = old_item[0]
        print(f"*{old_item} selected*")

        new_name = input("Type updated name of product, or leave blank for no change: ").strip().title()
        new_price = input("Type the updated product price, or leave blank for no change: ").strip()

        if new_name:
            sql = F"UPDATE products SET name = \'{new_name}\' WHERE products_id = {user_choice}"
            commit_query(sql)
            print(f"\n*[ID {product_id}]: Product name {old_name} updated to {new_name} successfully*")
        else:
            print(f'\n*[ID {product_id}]: Product name not changed as entry was left blank*')

        if new_price:
            sql = f"UPDATE products SET price = {new_price} WHERE (products_id = {user_choice})"
            commit_query(sql)
            print(f"*[ID {product_id}]: Price of {old_price} updated to {new_price} successfully*")
        else:
            print(f'*[ID {product_id}]: Product price not changed as entry was left blank*')

    except ValueError:
        print(f"ERROR: Please input the correct value type for the associated field")
    except pymysql.OperationalError:
        print(f"ERROR: Please ensure that price is a float value")


def update_courier():
    try:
        view_table("couriers")
        sql = f"SELECT COUNT(*) FROM couriers"
        check_empty = retrieve_fetchone(sql)
        if check_empty[0] == 0:
            print("Exiting update menu")
            return
        
        user_choice = int(input("Type the courier_id of courier you wish to update: "))
        sql = (f"SELECT * FROM couriers WHERE couriers_id = {user_choice}")
        old_item = retrieve_fetchone(sql)

        if not old_item:
            print(f"ERROR: The couriers_id you have entered ({user_choice}) could not be found")
            return
        
        old_name = old_item[1]
        old_number = old_item[2]
        courier_id = old_item[0]
        print(f"*{old_item} selected*")

        new_name = input("Type updated name of courier, or leave blank for no change: ").strip().title()
        new_number = input("Type the courier phone number, or leave blank for no change: ").strip()

        if new_name:
            sql = F"UPDATE couriers SET name = \'{new_name}\' WHERE couriers_id = {user_choice}"
            commit_query(sql)
            print(f"\n*[ID {courier_id}]: {old_name} updated to {new_name} successfully*")
        else:
            print(f"\n*[ID {courier_id}]: Product name not changed as entry was left blank*")

        if new_number:
            sql = f"UPDATE couriers SET phone_number = {new_number} WHERE couriers_id = {user_choice}"
            commit_query(sql)
            print(f"*[ID {courier_id}]: {old_number} updated to {new_number} successfully*")
        else:
            print(f"*[ID {courier_id}]: Courier phone number not changed as entry was left blank*")

    except ValueError:
        print(f"ERROR: Please input the correct value type for the associated field")
    except pymysql.OperationalError:
        print(f"ERROR: operationalerror")


def update_order_details():
    try:
        view_table("orders")
        sql = f"SELECT COUNT(*) FROM orders"
        check_empty = retrieve_fetchone(sql)
        if check_empty[0] == 0:
            print("Exiting update menu")
            return
    
        order_id_input = int(input("Type the orders_id of order you wish to update: "))
        sql = f"SELECT * FROM orders WHERE orders_id = {order_id_input}"
        old_order = retrieve_fetchone(sql)

        if old_order == None:
            print(f"ERROR: The orders_id you have entered ({order_id_input}) could not be found")
            return
        
        orders_id = old_order[0]
        old_customer_name = old_order[1]
        old_customer_address = old_order[2]
        old_customer_phonenumber = old_order[3]
        old_order_courier = old_order[4]
        
        old_order_products = old_order[6]
        old_order_products_listed = old_order_products.split(",")
        cursor = connection.cursor()
        old_products_list = []
        for number in old_order_products_listed:
            cursor.execute(f"SELECT * FROM mini_project.products WHERE products_id = {number}")
            old_product_query = cursor.fetchone()
            old_products_list.append(old_product_query)
        
        print(f"*{old_order} selected*")

        new_name = input("Type updated name of customer, or leave blank for no change: ").strip().title()
        new_address = input("Type updated customer address, or leave blank for no change: ").strip().title()
        new_phonenumber = input("Type updated customer phone number, or leave blank for no change: ").strip()

        view_table("products")
        products_input = input("Type ID of products you wish to overwrite with, or leave blank for no change: ")
        removed_spaces = products_input.replace(" ","")
        listed_version = removed_spaces.split(",")

        if removed_spaces:
            try:
                for number in listed_version:
                    sql = f"UPDATE products SET quantity = quantity - 1 WHERE products_id = {number}"
                    cursor = connection.cursor()
                    cursor.execute(sql)
            except pymysql.OperationalError:
                print("Error: There was not enough stock of a product to perform your order.")
                connection.rollback()
                return
            else:
                connection.commit()
            products_list_chosen = []
            cursor = connection.cursor()
            for number in listed_version:
                cursor.execute(f"SELECT * FROM mini_project.products WHERE products_id = {number}")
                products_choice = cursor.fetchone()
                products_list_chosen.append(products_choice)
            sql = f"UPDATE orders SET products_id = \'{products_input}\' WHERE orders_id = {order_id_input}"
            commit_query(sql)
            print(f"\n*[Order ID {orders_id}]: Products ordered changed from {old_products_list} to {products_list_chosen}*")
        else:
            print(f"\n*[Order ID {orders_id}]: Products ordered not changed as entry was left blank*")
        
        view_table("couriers")
        courier_input = input("Type ID of courier you want to use, or leave blank for no change: ").strip()

        if courier_input:
            courier_input = int(courier_input)
            cursor = connection.cursor()
            sql = F"UPDATE orders SET couriers_id = \'{courier_input}\' WHERE orders_id = {order_id_input}"
            commit_query(sql)
            print(f"\n*[Order ID {orders_id}]: Courier_ID {old_order_courier} updated to Courier_ID {courier_input} successfully*")
        else:
            print(f"\n*[Order ID {orders_id}]: Courier was not changed as entry was left blank*")
    
        if new_name:
            cursor = connection.cursor()
            sql = F"UPDATE orders SET customer_name = \'{new_name}\' WHERE orders_id = {order_id_input}"
            commit_query(sql)
            print(f"\n*[Order ID {orders_id}]: Customer name '{old_customer_name}' updated to '{new_name}' successfully*")
        else:
            print(f"\n*[Order ID {orders_id}]: Customer name not changed as entry was left blank*")

        if new_address:
            cursor = connection.cursor()
            sql = f"UPDATE orders SET customer_address = \'{new_address}\' WHERE orders_id = {order_id_input}"
            commit_query(sql)
            print(f"\n*[Order ID {orders_id}]: Customer address '{old_customer_address}' updated to '{new_address}' successfully*")
        else:
            print(f"\n*[Order ID {orders_id}]: Customer address not changed as entry was left blank*")

        if new_phonenumber:
            cursor = connection.cursor()
            sql = f"UPDATE orders SET customer_phone= \'{new_phonenumber}\' WHERE orders_id = {order_id_input}"
            commit_query(sql)
            print(f"\n*[Order ID {orders_id}]: Customer phone number '{old_customer_phonenumber}' updated to '{new_phonenumber}' successfully*")
        else:
            print(f"\n*[Order ID {orders_id}]: Customer phone number not changed as entry was left blank*")

    except ValueError:
        print(f"ERROR: ID not found")
    except pymysql.OperationalError:
        print(f"ERROR: operationalerror")


def update_order_status():
    try:
        view_table("orders")
        sql = f"SELECT COUNT(*) FROM orders"
        check_empty = retrieve_fetchone(sql)
        if check_empty[0] == 0:
            print("Exiting update menu")
            return
        
        order_id_input = input("Type the order_id you want to update status for: ")
        sql = (f"SELECT * FROM orders WHERE orders_id = {order_id_input}")
        old_item = retrieve_fetchone(sql)
        order_id = old_item[0]
        if old_item == None:
            print(f"ERROR: The orders_id you have entered ({order_id_input}) could not be found")
            return

        print(f"*[Order ID {order_id}] selected*")

        view_table("orders_status")
        new_status_input = input("Type status_id of status name you wish to update to, or leave blank for no change: ")

        if new_status_input:
            new_status_input = int(new_status_input)
            sql = F"UPDATE orders SET status_id = {new_status_input} WHERE orders_id = {order_id_input}"
            commit_query(sql)
            cursor = connection.cursor()
            cursor.execute(f"SELECT name FROM orders_status WHERE status_id = {new_status_input}")
            status_name_choice = cursor.fetchone()[0]
            print(f"\n*[Order ID {order_id}]: Updated to {status_name_choice} successfully*")
        else:
            print('\n*Order status not changed as entry was left blank*')

    except ValueError:
        print("ERROR: Please input the correct value type for the associated field")
    except pymysql.OperationalError:
        print("ERROR: You have entered a letter where number input was needed.")
    except TypeError:
        print("ERROR: Order")
    except pymysql.IntegrityError:
        print("ERROR: The status_id you have entered does not exist.")


def delete_item(table):
    try:
        view_table(table)
        sql = f"SELECT COUNT(*) FROM {table}"
        check_empty = retrieve_fetchone(sql)
        if check_empty[0] == 0:
            print("Exiting delete menu")
            return
        
        deleted_item = int(input("Type ID number of item you wish to delete: "))
        sql = (f"SELECT * FROM {table} WHERE {table}_id = {deleted_item}")
        selection = retrieve_fetchone(sql)

        if not selection:
            print(f"\nError: Item associated with chosen ID ({deleted_item}) not found.")
            return
    
        sql = (f"DELETE FROM {table} WHERE {table}_id = {deleted_item}")
        commit_query(sql)
        print(f"\n*Deleted {selection} from database*")

    except pymysql.IntegrityError:
        print(
            "ERROR: The item you are trying to delete is currently present in an order. "
        "The item cannot be deleted until the order is either deleted or completed."
        )
    except ValueError:
        print("ERROR: You did not input an ID value. To select an item, please input the ID.")


def update_product_quantity():
    view_table("products")
    sql = f"SELECT COUNT(*) FROM products"
    check_empty = retrieve_fetchone(sql)
    if check_empty[0] == 0:
        print("Products list empty. Please add a product to use this feature.")
        print("Exiting update menu")
        return
    try:
        user_product_choice = int(input("Type the Products_ID to modify it's quantity: "))
        sql = f"SELECT * FROM products WHERE products_id = {user_product_choice}"
        old_item = retrieve_fetchone(sql)
        if not old_item:
            print(f"ERROR: The products_id you have entered ({user_product_choice}) could not be found")
            return

        product_id = old_item[0]
        old_name = old_item[1]
        old_price = old_item[2]
        old_quantity = old_item[3]

        print(f"[ID {product_id}]: {old_name} selected with a quantity of {old_quantity}.")

    except ValueError:
        print("ERROR: You have entered a letter. A number option for the ID is needed.")

    print("\nUpdate Product Quantity")
    print("Press 0 to go back")
    print("Press 1 to add quantity")
    print("Press 2 to lower quantity")
    print("Press 3 to input correct quantity")
    try:
        user_input = int(input("How would you like to update that product? Please select option: "))
    except ValueError:
        print("ERROR: You must input a number option, not a letter.")
        return
    try:
        match user_input:
            case 0:
                return

            case 1:
                add_quantity = int(input(f"The quantity of {old_name} is currently at {old_quantity}. Input value you'd like to add by: ").strip())
                new_quantity = (old_quantity + add_quantity)
                sql = f"UPDATE products SET quantity = {new_quantity} WHERE (products_id = {user_product_choice})"
                commit_query(sql)
                print(f"\n*[ID {product_id}]: {old_name}'s quantity updated from {old_quantity} to {new_quantity} successfully*")

            case 2:
                subtract_quantity = int(input(f"The quantity of {old_name} is currently at {old_quantity}. Input value you'd like to subtract by: ").strip())
                new_quantity = (old_quantity - subtract_quantity)
                sql = f"UPDATE products SET quantity = {new_quantity} WHERE (products_id = {user_product_choice})"
                commit_query(sql)
                print(f"\n*[ID {product_id}]: {old_name}'s quantity updated from {old_quantity} to {new_quantity} successfully*")

            case 3:
                new_quantity = int(input(f"The quantity of {old_name} is currently at {old_quantity}. Input what you would like to update it to: ").strip())
                sql = f"UPDATE products SET quantity = {new_quantity} WHERE (products_id = {user_product_choice})"
                commit_query(sql)
                print(f"\n*[ID {product_id}]: {old_name}'s quantity updated from {old_quantity} to {new_quantity} successfully*")

            case _:
                print(f"ERROR: That number option ({user_input}) does not exist.")
                return

    except ValueError:
        print("ERROR: Quantity must be input with integer value. Decimal or letter values are not accepted.")
    except pymysql.DataError:
        print("ERROR: Product quantity cannot be below 0.")


def export_to_dat(table):
    sql = f"SELECT * FROM {table}"
    data = retrieve_fetchall(sql)
    data_array = []
    for row in data:
        data_array.append(row)
    
    pickle.dump(data_array, open(f"{table}_data.dat", "wb"))
    print(f"{table}'s data saved succesfully to .dat file.")


def commit_query(query):
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()


def retrieve_fetchone(query):
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    return result


def retrieve_fetchall(query):
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results


new_launch = True
while new_launch:
    print(
        "\n*Hello! Follow the instructions to navigate the cafe app*"
    )
    new_launch = False
    sleep(2)

main_menu()

