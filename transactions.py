from datetime import date
from storage import load_data, save_data
from books import get_books
from students import search_student

FILE = "transactions.json"

def get_transactions():
    return load_data(FILE)

def issue_book(student_id, book_id):
    student = search_student(student_id)
    if student is None:
        return False, "Student ID is not registered."

    books = get_books()
    book = next((b for b in books if b["book_id"] == book_id), None)
    if book is None:
        return False, "Book not found."
    if book["available"] < 1:
        return False, "No copies of this book are currently available."

    transactions = get_transactions()
    transaction_id = f"T{len(transactions) + 1:04d}"
    transactions.append({
        "transaction_id": transaction_id,
        "student_id": student_id,
        "book_id": book_id,
        "issue_date": date.today().isoformat(),
        "return_date": None,
        "status": "Issued"
    })

    book["available"] -= 1
    save_data("books.json", books)
    save_data(FILE, transactions)
    return True, f"Book issued successfully. Transaction ID: {transaction_id}"

def return_book(transaction_id):
    transactions = get_transactions()
    transaction = next(
        (t for t in transactions
         if t["transaction_id"] == transaction_id and t["status"] == "Issued"),
        None
    )
    if transaction is None:
        return False, "Active transaction not found."

    books = get_books()
    book = next((b for b in books if b["book_id"] == transaction["book_id"]), None)
    if book is None:
        return False, "Book record is missing. Please contact the administrator."

    transaction["status"] = "Returned"
    transaction["return_date"] = date.today().isoformat()
    book["available"] += 1

    save_data("books.json", books)
    save_data(FILE, transactions)
    return True, "Book returned successfully."

def active_issues():
    return [t for t in get_transactions() if t["status"] == "Issued"]

def transaction_history():
    return get_transactions()
