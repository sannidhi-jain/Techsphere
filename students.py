from storage import load_data, save_data

FILE = "students.json"

def get_students():
    return load_data(FILE)

def register_student(student_id, name, contact):
    students = get_students()
    if any(s["student_id"] == student_id for s in students):
        return False, "A student with this ID already exists."
    students.append({
        "student_id": student_id,
        "name": name,
        "contact": contact
    })
    save_data(FILE, students)
    return True, "Student registered successfully."

def list_students():
    return get_students()

def search_student(student_id):
    return next(
        (s for s in get_students() if s["student_id"] == student_id),
        None
    )

def delete_student(student_id):
    students = get_students()
    student = next((s for s in students if s["student_id"] == student_id), None)
    if student is None:
        return False, "Student not found."

    transactions = load_data("transactions.json")
    if any(t["student_id"] == student_id and t["status"] == "Issued"
           for t in transactions):
        return False, "Cannot delete: this student has an unreturned book."

    students.remove(student)
    save_data(FILE, students)
    return True, "Student deleted successfully."
