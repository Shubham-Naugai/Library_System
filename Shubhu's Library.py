import pandas as pd
import sqlalchemy
import cx_Oracle
import datetime
import re
from tabulate import tabulate


print("\033[1;36;40madmin \nstudent")
x = int(input("press 1 for sign in\n"
              "press 2 for sign up\n"))


class user_logs:
    def __init__(self, username, user_password):
        self.username = username
        self.password = user_password

    def func(self):
        connection = cx_Oracle.connect('c##shubham/123456@localhost:1521/orcl')
        cursor1 = connection.cursor()
        cursor2 = connection.cursor()
        cursor3 = connection.cursor()
        cursor4 = connection.cursor()
        cursor5 = connection.cursor()
        cursor1.execute("select user_name, user_password from user_details")
        list1 = cursor1.fetchall()
        cursor2.execute(f"select user_name, user_password from user_details where user_name = '{self.username.lower()}' and user_password = '{self.password}'")
        list2 = cursor2.fetchall()
        for detail in list2:
            for details in list1:
                if detail == details:
                    print("login successful")
                    return 0
            break
        else:
            print("Invalid username or password")
            print('forgot password', end='')
            fp = input('[y/n]: ')
            if fp.lower() == 'y':
                print('Enter Your Username, Phone, Email and DOB')
                user_name = input("Username: ")
                contact = input('Contact no.: +91')
                email_id = input('Email ID: ')
                date = input('DOB(dd/mm/yyyy): ')
                cursor3.execute("select user_name, contact, email_id, dob from user_details")
                list3 = cursor3.fetchall()
                cursor4.execute(f"select user_name, contact, email_id, dob from user_details where user_name = '{user_name.lower()}' and contact = '+91{contact}' and email_id = '{email_id.lower()}' and dob = TO_DATE('{date}', 'DD/MM/YYYY')")
                list4 = cursor4.fetchall()
                for individuals_data in list4:
                    for data in list3:
                        if individuals_data == data:
                            cursor5.execute(f"select user_password from user_details where user_name = '{user_name.lower()}' and contact = '+91{contact}' and email_id = '{email_id.lower()}' and dob = TO_DATE('{date}', 'DD/MM/YYYY')")
                            list5 = cursor5.fetchall()
                            secret_password = list(*list5)
                            print('Your password is:', *secret_password)
                    break
                else:
                    print('please enter correct details')
            else:
                pass
            return 1


if x == 1:
    name = input("username: ")
    up = input("password: ")
    user = user_logs(name, up)
    val = user.func()
    if val == 1:
        c = 0
        while True:
            if c < 2:
                name = input("username: ")
                up = input("password: ")
                user = user_logs(name, up)
                val = user.func()
                if val == 0:
                    break
            else:
                print("Try again later")
                exit()
            c += 1

if x == 2:
    while True:
        name = input("Username: ")
        password = input("Password: ")
        phone = input('Contact no.: +91')
        email = input('Email ID: ')
        dob = input('DOB(dd/mm/yyyy): ')
        try:
            match = re.match(r'(\d{2})[/.-](\d{2})[/.-](\d{4})$', dob)
            if match is not None:
                datetime.datetime(*(map(int, match.groups()[-1::-1])))
        except Exception as e:
            print(e)
            print('Invalid date of birth!')
            continue
        finally:
            try:
                day, month, year = map(int, dob.split('/'))
            except Exception as e:
                print(e)
                print('Invalid date of birth!')
                continue
        gender = input('Gender: (m/f)')
        if name == '' or password == '' or phone == '' or email == '' or dob == '' or gender == '':
            print('Enter correct details!')
            continue
        for i in name:
            if name[0] == ' ':
                print('enter valid username')
                break
        else:
            break

    try:
        con = cx_Oracle.connect('c##shubham/123456@localhost:1521/orcl')
        cur = con.cursor()
        cur.execute(f"insert into user_details values('{name.lower()}', '{password}', '+91{phone}', '{email.lower()}', TO_DATE('{dob}', 'DD/MM/YYYY'), '{gender.lower()}')")
        con.commit()
        print("Account successfully created")
    except Exception as error:
        print(error)


class Library:
    def __init__(self, lst, person_name, no_of_books):
        self.book_list = lst
        self.no_of_books = no_of_books
        self.name = person_name
        self.lend_dict = {}

    @staticmethod
    def display_Library():
        try:
            engine = sqlalchemy.create_engine("oracle+cx_oracle://c##shubham:123456@localhost:1521/orcl", arraysize=1000)
            orders_sql = """SELECT * FROM Library_database"""
            df_orders = pd.read_sql(orders_sql, engine)
            df_orders.columns = [z.upper() for z in df_orders.columns]
            df_orders.columns = df_orders.columns.str.replace('_', ' ')
            print(tabulate(df_orders, showindex=True, headers=df_orders.columns))
        except Exception as error1:
            print(error1)

    @staticmethod
    def lend_book(book_dict, user, book):
        try:
            for k in book_dict:
                if k == book:
                    if book_dict[book] != 0:
                        book_dict[book] -= 1
                        df = pd.read_json(r"D:\pandas\Lend_book_data.json")
                        df.fillna('0', inplace=True)
                        if user not in df:
                            df1 = pd.DataFrame({user: book}, index=[0])
                            df2 = pd.concat([df, df1])
                            df2.index = [x for x in range(1, len(df2.values) + 1)]
                            df2.to_json(r"D:\pandas\Lend_book_data.json")
                            new_df1 = pd.DataFrame(book_dict, index=[0])
                            new_df1.to_json(r"D:\pandas\book_data.json")
                            print("Lender-book database has been updated. You can take the book now")
                            return 0
                        else:
                            df1 = df.to_dict(orient='records')
                            new_list = []
                            for z in range(len(df1)):
                                new_list.append(df1[z][user])
                            if any(book in word for word in new_list):
                                print('You can take only one book of a type!')
                                return 0
                            else:
                                df1 = pd.DataFrame({user: book}, index=[0])
                                df2 = df.append(df1, ignore_index=True)
                                df2.to_json(r"D:\pandas\Lend_book_data.json")
                                new_frame = pd.DataFrame(book_dict, index=[0])
                                new_frame.to_json(r"D:\pandas\book_data.json")
                                print("Lender-book database has been updated. You can take the book now")
                                return 0
                    else:
                        print("All book are already being taken")
                        return 0
                else:
                    continue
            print("book is not in library")
        except Exception as E:
            print(E)

    @staticmethod
    def return_book(book_dict, user, book):
        try:
            for k in book_dict.keys():
                if k == book:
                    book_dict[book] += 1
                    df = pd.read_json(r"D:\pandas\Lend_book_data.json")
                    df.fillna('0', inplace=True)
                    if user in df:
                        df1 = df.to_dict(orient='records')
                        new_list = []
                        for z in range(len(df1)):
                            new_list.append(df1[z][user])
                        if any(book in word for word in new_list):
                            df1[z][user] = None
                            new_lb_df = pd.DataFrame(df1)
                            new_lb_df.to_json(r"D:\pandas\Lend_book_data.json")
                            new_frame = pd.DataFrame(book_dict, index=[0])
                            new_frame.to_json(r"D:\pandas\book_data.json")
                            print("Lender-book database has been updated. Book returned.")
                            return 0
                        else:
                            print("You haven't issued this book.")
                            return 0
                    else:
                        exit()
                else:
                    continue
            print("book is not in library")
        except Exception as err:
            print(err)

    @staticmethod
    def display_my_book(user):
        df = pd.read_json(r"D:\pandas\Lend_book_data.json")
        df.fillna('0', inplace=True)
        new_list = []
        df1 = df.to_dict(orient='records')
        if user in df:
            for z in range(len(df1)):
                if df1[z][user] != "0":
                    new_list.append(df1[z][user])
            if len(new_list) == 0:
                print("You have not issue any book.")
            else:
                print("You issued following books", new_list)
        else:
            print("You have not issue any book yet.")


if __name__ == '__main__':
    connection = cx_Oracle.connect('c##shubham/123456@localhost:1521/orcl')
    cursor_obj = connection.cursor()
    cursor_obj1 = connection.cursor()
    cursor_obj.execute("SELECT book_name FROM Library_database")
    cursor_obj1.execute("SELECT no_of_books FROM Library_database")
    lst = cursor_obj.fetchall()
    book_lst = cursor_obj1.fetchall()
    test_keys = []
    test_values = []
    for i in lst:
        test_keys.append(*i)
    for j in book_lst:
        test_values.append(*j)
    shubham = Library(test_values, "Shubhu", test_keys)
    books = {test_keys[i]: test_values[i] for i in range(len(test_keys))}
    new_df = pd.read_json(r"D:\pandas\book_data.json")
    dict1 = new_df.to_dict(orient='records')
    dict1 = dict1[0]
    while True:
        print(f"Welcome to {shubham.name.upper()}'s LIBRARY. Enter your choice to continue")
        print("1. Display Books in Library")
        print("2. Lend a Book")
        print("3. Return a Book")
        print("4. Display Books you issued")
        user_choice = input()
        if user_choice not in ['1', '2', '3', '4']:
            print("Please enter a valid option")
            continue

        else:
            user_choice = int(user_choice)

        if user_choice == 1:
            shubham.display_Library()

        elif user_choice == 2:
            book = input("Enter the name of the book you want to lend: ")
            shubham.lend_book(dict1, name, book)

        elif user_choice == 3:
            book = input("Enter the name of the book you want to return: ")
            shubham.return_book(dict1, name, book)

        elif user_choice == 4:
            shubham.display_my_book(name)

        else:
            print("Not a valid option")

        print("Press q to quit and c to continue")
        user_choice2 = ""
        while user_choice2 != "c" and user_choice2 != "q":
            user_choice2 = input()
            if user_choice2 == "q":
                print(f"Thank You for visiting {shubham.name.upper()}'s LIBRARY.")
                exit()

            elif user_choice2 == "c":
                continue
