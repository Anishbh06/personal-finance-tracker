from datetime import datetime

date_format = "%d-%m-%Y"
CATEGORIES = {
    "I": "income", 
    "E": "expense"
    }

def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)
    
    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("invalid Date Format. Please enter the date in dd-mm-yyyy format")
        return(prompt,allow_default)


def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <=0:
            raise ValueError("Amount cannot be 0.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()

def get_category():
    category = input("Etner category \n I: inome \n E:Expense").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    
    print("invalid category. Please enter I oe E for icome and expense respectively")
    return get_category



def get_description():
    return input("Enter description: ")
