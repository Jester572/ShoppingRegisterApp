import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time
from datetime import date

cred = credentials.Certificate("firebase_Key.json")

firebase_admin.initialize_app(cred)
db = firestore.client()

ticket_book = db.collection("Ticket Book")
sales_report = db.collection("Daily Sales")

# test data
# ticket_book.document("3").set({
#         'ticket_num': "3",
#         'date': "2023-04-08",
#         'time': "17:07:30",
#         'item': "Baby Bibs",
#         'quantity': '34',
#         'total_price': "1.50",
#         'notes': "ticket.notes"
#     })
# ticket_book.document("4").set({
#         'ticket_num': "4",
#         'date': "2023-04-08",
#         'time': "17:07:30",
#         'item': "Charging Cords",
#         'quantity': '7',
#         'total_price': "1.50",
#         'notes': "ticket.notes"
#     })
# ticket_book.document("5").set({
#         'ticket_num': "5",
#         'date': "2023-04-08",
#         'time': "17:07:30",
#         'item': "Television",
#         'quantity': '1',
#         'total_price': "1500",
#         'notes': "ticket.notes"
#     })
# ticket_book.document("6").set({
#         'ticket_num': "6",
#         'date': "2023-04-09",
#         'time': "17:07:30",
#         'item': "Picture Fram",
#         'quantity': '16',
#         'total_price': "5",
#         'notes': "ticket.notes"
#     })
# ticket_book.document("7").set({
#         'ticket_num': "7",
#         'date': "2023-04-09",
#         'time': "17:07:30",
#         'item': "Radio",
#         'quantity': '3',
#         'total_price': "25.99",
#         'notes': "ticket.notes"
#     })


class Ticket:
    def __init__(self, item, quantity, notes):
        self.ticket_num = None
        self.date = None
        self.time = None
        self.item = item
        self.quantity = quantity
        self.total_price = None
        self.notes = notes

    def new_ticket(self):
        ticket_data = ticket_book.get()

        self.ticket_num = len(ticket_data)
        while ticket_book.document(str(self.ticket_num)).get().exists:
            self.ticket_num += 1
        if isinstance(self.ticket_num, int):
            self.ticket_num = str(self.ticket_num)
        self.date = str(date.today())
        self.time = str(time.strftime("%H:%M:%S", time.localtime()))
        self.item = input("Enter the item: ")
        self.quantity = input("Enter the Quantity: ")
        price = input("Enter the Price of the item: ")
        self.total_price = "{:.2f}".format(int(self.quantity) * float(price))
        self.notes = input("Enter any notes: ")

    def print_ticket(self):
        print("Ticket Number:", self.ticket_num)
        print("Date:", self.date)
        print("Time:", self.time)
        print("item:", self.item)
        print("Quantity:", self.quantity)
        print("total_price:", self.total_price)
        print("Notes:", self.notes)


def save_ticket(ticket):
    ticket_book.document(ticket.ticket_num).set(
        {
            "ticket_num": ticket.ticket_num,
            "date": ticket.date,
            "time": ticket.time,
            "item": ticket.item,
            "quantity": ticket.quantity,
            "total_price": ticket.total_price,
            "notes": ticket.notes,
        }
    )
    print("Saved successfully")


def edit_ticket():
    number = input("Enter the ticket number: ")

    if ticket_book.document(number).get().exists:
        edit_ticket = ticket_book.document(number).get()
        ticket_data = edit_ticket.to_dict()

        current_item = ticket_data["item"]
        current_quantity = ticket_data["quantity"]
        current_notes = ticket_data["notes"]

        print(f"Current item: {current_item}")
        print(f"Current quantity: {current_quantity}")
        print(f"Current notes: {current_notes}")

        new_item = input("Input desired item: ")
        new_quantity = input("Input desired quantity: ")
        new_notes = input("Input desired notes: ")

        ticket_book.document(number).update(
            {
                "ticket_num": ticket_data["ticket_num"],
                "date": ticket_data["date"],
                "time": ticket_data["time"],
                "item": new_item,
                "quantity": new_quantity,
                "total_price": ticket_data["total_price"],
                "notes": new_notes,
            }
        )

        print(f"Ticket:{ticket_book.document(number).get()} has been updated")
    else:
        print(f"Ticket: {number} does not exist")
        # add stuf


def delete_ticket():
    number = input("Enter the ticket number: ")

    if ticket_book.document(number).get().exists:
        ticket_book.document(number).delete()
        print(f"Ticket:{ticket_book.document(number).get()} has been deleted")
    else:
        print(f"Ticket: {number} does not exist")


def print_tickets():
    data = ticket_book.get()
    print(
        "--------------------------------------------------------------------------------------------------------"
    )
    print(
        "Ticket Number |    Date    |   Time   |  item  | Quantity | Total Price($) |          Notes"
    )
    print(
        "--------------------------------------------------------------------------------------------------------"
    )
    for i in data:
        ticket_data = i.to_dict()
        print(
            "{:^14}| {:<5} | {:<2} | {:<10} | {:^8} | {:<14} | {:<10}".format(
                ticket_data["ticket_num"],
                ticket_data["date"],
                ticket_data["time"],
                ticket_data["item"],
                ticket_data["quantity"],
                ticket_data["total_price"],
                ticket_data["notes"],
            )
        )
        print(
            "--------------------------------------------------------------------------------------------------------"
        )


def daily_sales():
    data = ticket_book.get()
    ticket_date = ""
    total_tickets = 0
    daily_total = 0
    items_sold = 0

    for i in data:
        ticket_data = i.to_dict()
        if ticket_date == "":
            ticket_date = ticket_data["date"]
            daily_total += float(ticket_data["total_price"])
            items_sold += float(ticket_data["quantity"])
            total_tickets += 1

            sales_report.document(ticket_data["date"]).set(
                {
                    "Date": ticket_data["date"],
                    "Number of Sales": total_tickets,
                    "Sales Total": daily_total,
                    "Number of Items Sold": items_sold,
                }
            )

        elif ticket_data["date"] != ticket_date:
            ticket_date = ticket_data["date"]
            total_tickets = 0
            daily_total = 0
            items_sold = 0
            daily_total += float(ticket_data["total_price"])
            items_sold += float(ticket_data["quantity"])
            total_tickets += 1

            sales_report.document(ticket_data["date"]).set(
                {
                    "Date": ticket_data["date"],
                    "Number of Sales": total_tickets,
                    "Sales Total": daily_total,
                    "Number of Items Sold": items_sold,
                }
            )

        else:
            daily_total += float(ticket_data["total_price"])
            items_sold += float(ticket_data["quantity"])
            total_tickets += 1
            sales_report.document(ticket_data["date"]).set(
                {
                    "Date": ticket_data["date"],
                    "Number of Sales": total_tickets,
                    "Sales Total": daily_total,
                    "Number of Items Sold": items_sold,
                }
            )

    print("Daily Sales uploaded")
    print("---------------------------------------------------------------")
    print("    Date    |   # of Sales   |  Sales Total($)  | # Items Sold ")
    print("---------------------------------------------------------------")
    reportData = sales_report.get()
    for i in reportData:
        more_data = i.to_dict()

        print(
            "{:^11} | {:^14} | {:^16} | {:^11}".format(
                more_data["Date"],
                more_data["Number of Sales"],
                more_data["Sales Total"],
                more_data["Number of Items Sold"],
            )
        )
        print("---------------------------------------------------------------")


def main():
    while True:
        # display the menu
        choice = input(
            "Main Menu\n"
            + "1. Add a new ticket\n2. Display all tickets\n3. Edit a ticket\n4. Delete a ticket\n5. Daily Sales\n6. Quit\n"
            + "Enter your selection: "
        )
        if choice == "1":
            cont = Ticket("", "", "")
            cont.new_ticket()
            save_ticket(cont)
        elif choice == "2":
            print_tickets()
        elif choice == "3":
            edit_ticket()
        elif choice == "4":
            delete_ticket()
        elif choice == "5":
            daily_sales()
        elif choice == "6":
            print("\nGoodbye!\n")
            break


if __name__ == "__main__":
    main()
