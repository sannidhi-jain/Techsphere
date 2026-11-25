from books import list_books
from students import list_students
from transactions import transaction_history, active_issues

def get_library_report():
    books = list_books()
    students = list_students()
    history = transaction_history()
    issued = active_issues()

    return {
        "different_books": len(books),
        "total_copies": sum(b["quantity"] for b in books),
        "available_copies": sum(b["available"] for b in books),
        "registered_students": len(students),
        "total_transactions": len(history),
        "currently_issued": len(issued)
    }

def display_report():
    report = get_library_report()
    print("\n========== LIBRARY REPORT ==========")
    for label, value in report.items():
        print(f"{label.replace('_', ' ').title():25}: {value}")
    print("====================================")
