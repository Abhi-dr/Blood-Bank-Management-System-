import mysql.connector as connector

bb = connector.connect(host="localhost", user="root", passwd="papaji-0987", database="bloodbank")
mycursor = bb.cursor()

line = "\n<" + "-" * 30 + " RESTART " + "-" * 30 + ">"

id = mycursor.execute("select max(id) from donation;")
id = list(mycursor.fetchall()[0])[0] + 1

id_accept = mycursor.execute("select max(id) from accept;")
id_accept = list(mycursor.fetchall()[0])[0] + 1

bld_dict_qnty = {"a_neg": "A-", "a_pos": "A+", "b_pos": "B+", "o_neg": "O-",
                 "b_neg": "B-", "o_pos": "O+", "ab_pos": "AB+", "ab_neg": "AB-"}

bld_dict_accept = {"A-": "a_neg", "A+": "a_pos", "B+": "b_pos", "O-": "o_neg", "B-": "b_neg", "O+": "o_pos",
                   "AB+": "ab_pos", "AB-": "ab_neg"}

price_dict = {"A-": 100, "A+": 150, "B+": 120, "O-": 3000, "B-": 200, "O+": 500, "AB+": 2500, "AB-": 5000}


def condition(blood_group2, quantity2):
    if blood_group2 == "AB+":
        command = f"insert into quantity (ab_pos) values ({quantity2})"
        mycursor.execute(command)
        bb.commit()

    elif blood_group2 == "AB-":
        command = f"insert into quantity (ab_neg) values ({quantity2})"
        mycursor.execute(command)
        bb.commit()

    elif blood_group2 == "A+":
        command = f"insert into quantity (a_pos) values ({quantity2})"
        mycursor.execute(command)
        bb.commit()

    elif blood_group2 == "A-":
        command = f"insert into quantity (a_neg) values ({quantity2})"
        mycursor.execute(command)
        bb.commit()

    elif blood_group2 == "B-":
        command = f"insert into quantity (b_neg) values ({quantity2})"
        mycursor.execute(command)
        bb.commit()

    elif blood_group2 == "B+":
        command = f"insert into quantity (b_pos) values ({quantity2})"
        mycursor.execute(command)
        bb.commit()

    elif blood_group2 == "O-":
        command = f"insert into quantity (o_neg) values ({quantity2})"
        mycursor.execute(command)
        bb.commit()

    elif blood_group2 == "O+":
        command = f"insert into quantity (o_pos) values ({quantity2})"
        mycursor.execute(command)
        bb.commit()


class BloodBank:

    def donation(name, blood_group, quantity, phone_no):
        command = f"insert into donation (id, name, bld_grp, qnty, ph_no) values ('{id}', '{name}', '{blood_group}', '{quantity}', '{phone_no}')"

        condition(blood_group, quantity)

        mycursor.execute(command)
        bb.commit()
        print("\n\t\t\t\t\t\t\t\t\tYour Data has been saved Successfully!")

    def acception(name, blood_group, quantity, phone_no):
        mycursor.execute(f"select sum({bld_dict_accept.get(blood_group)}) from quantity;")
        availability = list(mycursor.fetchone())[0]

        if availability >= quantity:
            command = f"insert into accept (id, name, bld_grp, qnty, ph_no) values ('{id_accept}', '{name}', '{blood_group}', '{quantity}', '{phone_no}')"
            mycursor.execute(command)
            bb.commit()
            mycursor.execute(f"insert into quantity ({bld_dict_accept.get(blood_group)}) values ({-(quantity)});")
            bb.commit()

            print(f"Amount Payable:- Rs. {quantity * price_dict.get(blood_group)}/- ")
            print("\n\t\t\t\t\t\t\t\t\t\tThanks For Coming... We Hope The Patient Will Get Well Soon!... ")

        else:
            print("Sorry... We Do Not Have Enough Quantity Of Blood To Fulfill Your Requirement... ")

    def quantity():

        for blood in bld_dict_qnty.keys():
            mycursor.execute(f"select sum({blood}) from quantity;")
            data = mycursor.fetchone()

            if data == (None,):
                print(f"{bld_dict_qnty.get(blood)} = {0} L")

            else:
                print(f"{bld_dict_qnty.get(blood)} = {round(list(data)[0], 2)} L")


while True:

    user = str(input("Enter your choice:- \n1. Donate Blood\n2. Accept Blood\n3. Quantity Details\n4. Exit\n-> "))

    if user == '1':

        name = str(input("Name: "))
        blood_group = str(input("Blood Group: "))
        quantity = float(input("Quantity: "))
        phone_no = int(input("Phone Number: "))

        BloodBank.donation(name, blood_group, quantity, phone_no)
        print(line)

    elif user == '2':

        name = str(input("Name: "))
        blood_group = str(input("Blood Group: "))
        quantity = float(input("Quantity: "))
        phone_no = int(input("Phone Number: "))

        BloodBank.acception(name, blood_group, quantity, phone_no)
        print(line)

    elif user == '3':
        BloodBank.quantity()
        print(line)

    elif user == '4':
        print("\t\t\t\t\t\t\t\t\t\tThanks For Visiting...")
        print("\t\t\t\t\t\t\t\t\t\t\tVisit Again...")
        break

    else:
        print("Invalid Input!... Try Again!...", line)