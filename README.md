# Overview


The shopping_tickets program is a program written in python that implements the Fire Store cloud database. When you run the program, it will allow you to interact with the main menu to choose from 1 of six options.
- Option 1: Add Ticket- Creates a ticket that is stored in the database
- Option 2: Display all tickets- Prints out a list of all the tickets and all their information
- Option 3: Delete a ticket- This deletes a ticket by ticket number
- Option 4: Daily Sales- Provides and creates a daily report on all tickets created separating each by the date
- Option 5: Quit- Exits out of the program

This program was written to keep track of the amount of inventory that leaves a store. It also provides an automatic daily report. 


[Software Demo Video](https://youtu.be/AlcRVNi2wDQ)

# Cloud Database

Cloud Fire Store

The Database consists of two tables. The first table stores all the tickets in it, and each ticket stores the ticket information which is sorted by its ticket number. The second table holds the Daily Reports. The daily reports are organized by its date and stores the number of items sold, total sales, total tickets.

# Development Environment

Visual Studio Code

Programming Language: Python
Libraries: time,  datetime, firebase_admin

# Useful Websites


- [Firebase Firestore](https://firebase.google.com/docs/firestore/)
- [Python Firebase SDK Integration With Real Time Database](https://www.youtube.com/watch?v=EiddkXBK0-o&t=120s)

# Future Work

- Create a monthly report
- Create and implement a better GUI
- Make it so you can add more than one item per ticket.
