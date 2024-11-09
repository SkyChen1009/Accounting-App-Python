# Accounting CLI App

This is a simple command-line accounting application in Python. It allows users to manage personal financial records by adding, viewing, deleting, and searching records of income and expenses. The application saves records to a file for persistence.

## Features

- **Add Record**: Add income or expense records with a category, description, and amount.
- **View Records**: View a list of all records, including the current balance.
- **Delete Record**: Remove a record from the list by selecting it by index.
- **View Categories**: Display a hierarchical list of all supported categories.
- **Find Records by Category**: Search for records by category, including subcategories, and view the total for the selected category.
- **Persistence**: Records are saved to a file (`records.txt`) and reloaded upon restarting the app.

## Getting Started

### Prerequisites

- Python 3.x

### Installation

1. Clone this repository or download the code.
2. Open a terminal and navigate to the code's directory.

### Usage

Run the application by executing:

```bash
python accounting_app.py
```

## Example
### Add Records
```sql
What do you want to do (add / view / delete / view categories / find / exit)? add
Add some expense or income records with category, description, and amount:
meal lunch -50
```

### Viewing Records
```sql
What do you want to do (add / view / delete / view categories / find / exit)? view
Category        Description     Amount
=============== =============== ======
meal            lunch           -50
=============== =============== ======
Now you have X dollars.
```

### Deleting Records
```sql
What do you want to do (add / view / delete / view categories / find / exit)? delete
List of records
1. meal lunch -50
Which record do you want to delete? 1
Deleted record: meal lunch -50
```

### Viewing Categories
```sql
What do you want to do (add / view / delete / view categories / find / exit)? view categories
    - expense
        - food
            - meal
            - breakfast
            ...
        - transportation
            - bus
            ...
    - income
        - salary
        - bonus
        ...
```

### Finding Records by Category
```sql
What do you want to do (add / view / delete / view categories / find / exit)? find
Which category do you want to find? meal
Here's your expense and income records under category: meal
Category        Description     Amount
=============== =============== ======
meal            lunch           -50
======================================
The total amount for meal above is: -50
```

## Data Persistence
Records are saved in records.txt in the format:
```sql
balance
category, description, amount
...
```
