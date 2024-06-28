# Import necessary modules from the Flask package
from flask import Flask, render_template, request, redirect, url_for

# Create an instance of the Flask class representing the application
app = Flask(__name__)

# Initialize an empty list to store expenses
expenses = []

"""
Add a new expense to the tracker
Parameters:
- description (str): The description of the expense
- amount (float): The amount of the expense
- date (str): The date of the expense
Result: Appends the expense to the expenses list and prints "added expense"
"""
def add_expense(description, amount, date):
    expense_id = len(expenses) + 1
    expense = {
        'id': expense_id,
        'description': description,
        'amount': amount,
        'date': date
    }
    expenses.append(expense)
    print(f"Added expense: {description}, {amount}, {date}")

"""
Display all expenses in the tracker
Return: A list of expenses
"""
def view_expenses():
    if not expenses:
        return []
    return expenses

"""
Delete an expense from the tracker by its ID
Parameters:
- expense_id (int): The ID of the expense to delete
"""
def delete_expense(expense_id):
    global expenses
    expenses = [expense for expense in expenses if expense['id'] != expense_id]
    print(f"Deleted expense with ID: {expense_id}")

"""
Display a summary of the total 'amount' of expenses
Return: The total amount of all expenses
"""
def view_summary():
    total_amount = sum(expense['amount'] for expense in expenses)
    return total_amount

"""
Render the main page
Return: Renders the 'index.html' template
"""
@app.route('/')
def index():
    return render_template('index.html')

"""
Render the about page
Return: Renders the 'about.html' template
"""
@app.route('/about')
def about():
    return render_template('about.html')

"""
Handle the addition of a new expense
Methods: GET and POST
GET: Render the 'post_message.html' template
POST: Add the new expense and redirect to the view expenses page
"""
@app.route('/post_message', methods=['GET', 'POST'])
def post_message():
    if request.method == 'POST':
        description = request.form['description']
        amount = float(request.form['amount'])
        date = request.form['date']
        add_expense(description, amount, date)
        return redirect(url_for('view_expenses_route'))
    return render_template('post_message.html')

"""
Render the view expenses page
Return: Renders the 'main.html' template with the list of expenses
"""
@app.route('/view_expenses')
def view_expenses_route():
    expenses_list = view_expenses()
    return render_template('main.html', expenses=expenses_list)

"""
Handle the deletion of an expense
Methods: POST
POST: Delete the specified expense and redirect to the view expenses page
"""
@app.route('/delete_expense', methods=['POST'])
def delete_expense_route():
    expense_id = int(request.form['expense_id'])
    delete_expense(expense_id)
    return redirect(url_for('view_expenses_route'))

"""
Display a summary of the total expenses
Return: A string showing the total amount of expenses
"""
@app.route('/summary')
def summary():
    total_amount = view_summary()
    return f"Total expenses: {total_amount}"

# This checks if the script is being run directly (as the main program)
# and not being imported as a module
if __name__ == '__main__':
    # Run the Flask application
    app.run(host='0.0.0.0', port=8080)
