import sys

class Record:
    """
    Represent a record.
    """
    def __init__(self, category, description, amount):
        self._category = category
        self._description = description
        self._amount = amount
        
    # Initialize the attributes from the parameters.
    @property
    def category(self):
        return self._category
    
    @property
    def description(self):
        return self._description
    
    @property
    def amount(self):
        return self._amount

class Categories:
    """
    Maintain the category list and provide some methods.
    """
    def __init__(self):
        #the list of all categories
        self._categories = ['expense', ['food', ['meal', 'breakfast', 'lunch', 'dinner', 'snack', 'drink', 'fruit'], 'transportation', ['bus', 'MRT', 'gas', 'railway'], 'entertainment', ['garments', 'movies', 'travel']], 'income', ['salary', 'bonus', 'lottery']]
    
    def view_categories(self, categories=None, level=0):
        """
        This is to view all the categories.
            Use recursive call to make indent in different level.
            Print categories with proper indent and string.
        """
        if categories is None:
            categories = self._categories
        #Recursively find the category in different level
        if type(categories) in {list, tuple}:
            for child in categories:
                self.view_categories(child, level+1)
        else:
            print(f'{" " * 4 * level} - {categories}')

    def is_category_valid(self, category, categories):
        """
        This is to check if the input category in add function is valid.
            Recursively call the method to check if it is in the categories.
        """
        if type(categories) == list:
            #Recursively check if the category is in the list
            for child in categories:
                if self.is_category_valid(category, child):
                    return True
            return False
        else:
            return category == categories

    def find_subcategories(self, category, categories=None):
        """
        Use generator to check if the input category is in the Records.
            if there is not, return a empty list.
        """
        def find_subcategories_gen(category, categories, found=False):
            if type(categories) == list:
                for index, child in enumerate(categories):
                    yield from find_subcategories_gen(category, child, found)
                    if child == category and index + 1 < len(categories) and type(categories[index + 1]) == list:
                        # When the target category is found,
                        # recursively call this generator on the subcategories
                        # with the flag set as True.
                        yield from find_subcategories_gen(category, categories[index + 1], True)
            else:
                if categories == category or found:
                    yield categories

        if categories is None:
            categories = self._categories

        # create a generator instance
        subcategories_gen = find_subcategories_gen(category, categories)

        # Collect the generator results in a list
        subcategories_list = list(subcategories_gen)

        return subcategories_list

class Records():
    def __init__(self, categories_instance):
        self._records = []
        self._initial_money = 0
        self._categories_instance = categories_instance
        """
        This is to check if the file exist, 
            the first info is number of the deposit, 
            also each expense and income can be written into records.
        Otherwise, raise alert, initialize the deposit to be 0,
            and leave "Welcome Back" as historical usage.
        """
        # check if the file exists
        try:
            with open("records.txt", "r") as file:
                # read and load initial from the existing file
                data = file.readline()
                if len(data) < 1:
                    print("No lines in the file!")
                else:
                    # check if the file has lines
                    try:
                        file.seek(0)
                        self._initial_money = int(file.readline())
                    except ValueError:
                        print("The first line cannot be interpreted as the initial amount of money (i.e., cannot be converted to an integer)")

                    datas = file.readlines()

                    # read data from line to line
                    for line in datas:
                        category, description, amount = line.split(", ")
                        # check if any of the other lines cannot be interpreted as a record
                        try:
                            record = Record(category, description, int(amount))
                            self._records.append(record)
                        except ValueError:
                            sys.stderr.write("Any of the other lines cannot be interpreted as a record")
            print("Welcome back!")

        except FileNotFoundError:
            sys.stderr.write("There is no file.\n")
            # initialize and check for input correctness
            try:
                self._initial_money = int(input("How much money do you have? "))
            except ValueError:
                print("Invalid value for money. Set to 0 by default.")
                self._initial_money = 0

    
    def add(self, new):
        """
        This is to add record into the Records().
            First, check if the new input is valid format (3 string).
            Second, check if the amount is interger.
            Third, check if the input new record is valid. -> Call the is_categories_valid to check if it is in categories.
            Fourth, append them into the Records.
        """
        # check if input a string that does not follow the format
        while True:
            # Convert the string into a Record instance
            new_values = new.split(' ')
            if len(new_values) < 3:
                print("The format of a record should be like this: meal breakfast -50.\nFail to add a record.")
                new = input("Please enter the record again: ")
                continue
            else:
                # check the third string of a record, after splitting, cannot be converted to an integer.
                try:
                    new_values[2] = int(new_values[2])
                except ValueError:
                    print("The third string of a record, after splitting, cannot be converted to an integer.")
                    new = input("Please enter the record again: ")
                    continue
            
            # check if input category valid, if not, restart
            if not self._categories_instance.is_category_valid(new_values[0], self._categories_instance._categories):
                print(f"Invalid category: {new_values[0]}. Please choose a valid category.")
                new = input("Please enter the record again: ")
                continue
            #All valid, append them in Record()
            record = Record(new_values[0], new_values[1], int(new_values[2]))
            self._records.append(record)
            self._initial_money += record.amount
            self.save()
            break

    def view(self):
        """
        Print it in format. 
        Call from Records._records
        """
        print("Category\tDescription\tAmount")
        print("=============== =============== ======")

        # string formatting by zip them horizontally
        for record in self._records:
            print(f'{record.category:<16}{record.description:<16}{record.amount:<8}')
        print("=============== =============== ======")
        # least updated deposit
        print(f'Now you have {self._initial_money} dollars. ')
        # return it as two components, initial and records
        return self._initial_money, (record.category for record in self._records)

    def delete(self, delete_index):
        """
        List all the record in records first, let user choose the index to delete.
            1. Check if the index is in the range of records.
            2. Assign the delete_index as the index of record to delete.
            3. Pop the specified record according to the index.
            4. Print the deleted record.
        """
        delete_index = int(delete_index)
        delete_index -= 1
        if 0 <= delete_index < len(self._records):
            # Get the details of the record to be deleted
            category_to_remove = self._records[delete_index].category
            description_to_remove = self._records[delete_index].description
            amount_to_remove = self._records[delete_index].amount

            # Remove the chosen record
            self._records.pop(delete_index)
            self._initial_money -= amount_to_remove
            self.save()

            print(f"Deleted record: {category_to_remove} {description_to_remove} {amount_to_remove}")
        else:
            print("Invalid index. Please enter a valid index.")

    def find(self, target):
        """
        Find the target category and all its description and amount.
            1. Check the target category is in the categories list.  -> Call from find_subcategories
            2. Use filter method to pick the specified record with the target category.
            3. If not, print no records for the target.
            4. If yes, print in format and sum the amount of the target category.
        """
        # find subcategories for the given category
        subcategories = self._categories_instance.find_subcategories(target)
        
        #if the record of the target doesn't exist in Records
        if not subcategories:
            print(f"No records found for category '{target}'.")
            return 
            
        else:
            # use lambda and filter to find matching records
            filtered_records = filter(lambda rec: rec.category in subcategories, self._records)
            filtered_records = list(filtered_records)
            
            if not filtered_records:
                print(f"No records found for category '{target}'.")
                return
            
            # calculate total amount for the target category
            total_amount = sum(rec.amount for rec in filtered_records)

            # print the filtered records
            print(f"Here's your expense and income records under category : {target}")
            print("Category\tDescription\tAmount")
            print("=============== =============== ======")
            for rec in filtered_records:
                print(f"{rec.category:<16}{rec.description:<16}{rec.amount:<8}")
            print("======================================")
            print(f"The total amount for {target} above is : {total_amount}")
        
    def save(self):
        """
        Write the records into a file with first line : changed deposit.
            Next line: print the record in this format: category, description, amount
        """
        # write to a file
        with open("records.txt", "w") as file:
            file.write(f"{self._initial_money}\n")
            for record in self._records:
                file.write(f"{record.category}, {record.description}, {record.amount}\n")

                
#initialize the __init__ in class method
categories = Categories()
records = Records(categories)

while True:
    """
    This is the main namespace of the Accounting App.
    Command: add -> call the Records attribute -> add method
             view -> call the Records attribute -> view method
             delete -> call the Records attribute -> delete method (print the records with index first to let user choose.)
             view categories -> call the Categories attribute -> view categories
             find -> call the Records attribute -> find method
             exit -> call the Records attribute -> save method
    """
    command = input('\nWhat do you want to do (add / view / delete / view categories / find / exit)? ')
    if command == 'add':
        record = input('Add some expense or income records with category, description, and amount (separate by spaces):\ncat1 desc1 amt1, cat2 desc2 amt2, cat3 desc3 amt3, ...\n')
        #assgin input as Records' method parameter
        records.add(record)

    elif command == 'view':
        records.view()

    elif command == 'delete':
        print("List of records")
        print("="*50)
        for i, record in enumerate(records._records):
            print(f"{i+1}. {record.category} {record.description} {record.amount}")
        delete_index = input("Which record do you want to delete? ")
        #assgin input index as Records' method parameter
        records.delete(delete_index)

    elif command == 'view categories':
        categories.view_categories()

    elif command == 'find':
        target = input('Which category do you want to find? ')
        #assgin target as Records' method parameter
        records.find(target)

    elif command == 'exit':
        records.save()
        break
    
    else:
        sys.stderr.write('Invalid command. Try again.\n')