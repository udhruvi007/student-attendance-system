import json
import os
from datetime import date

# ─────────────────────────────────────────
#  FILE PATHS
# ─────────────────────────────────────────
STUDENTS_FILE = "students.json"
ATTENDANCE_FILE = "attendance.json"


# ─────────────────────────────────────────
#  HELPER: Load / Save JSON
# ─────────────────────────────────────────
def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return {}


def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)


# ─────────────────────────────────────────
#  1. ADD STUDENT
# ─────────────────────────────────────────
def add_student():
    students = load_json(STUDENTS_FILE)

    print("\n--- Add New Student ---")
    roll = input("Enter Roll Number: ").strip()

    if roll in students:
        print(f"⚠ Student with Roll No '{roll}' already exists!")
        return

    if not roll.isdigit():
        print("⚠ Roll Number must contain only digits.")
        return

    name = input("Enter Student Name: ").strip()

    if not name:
        print("⚠ Name cannot be empty.")
        return

    students[roll] = name
    save_json(STUDENTS_FILE, students)

    print(f"✅ Student '{name}' (Roll: {roll}) added successfully!")


# ─────────────────────────────────────────
#  2. VIEW ALL STUDENTS
# ─────────────────────────────────────────
def view_students():
    students = load_json(STUDENTS_FILE)

    print("\n--- All Students ---")

    if not students:
        print("No students found. Please add students first.")
        return

    print(f"{'Roll No':<12} {'Name'}")
    print("-" * 30)

    for roll, name in sorted(students.items()):
        print(f"{roll:<12} {name}")


# ─────────────────────────────────────────
#  3. MARK ATTENDANCE
# ─────────────────────────────────────────
def mark_attendance():
    students = load_json(STUDENTS_FILE)

    if not students:
        print("\n⚠ No students found. Please add students first.")
        return

    attendance = load_json(ATTENDANCE_FILE)

    today = str(date.today())

    if today in attendance:
        print(f"\n⚠ Attendance for {today} is already marked!")
        return

    print(f"\n--- Mark Attendance for {today} ---")
    print("Enter 'P' for Present, 'A' for Absent\n")

    daily_record = {}

    for roll, name in sorted(students.items()):
        while True:
            status = input(f"{name} (Roll {roll}) [P/A]: ").strip().upper()

            if status in ("P", "A"):
                daily_record[roll] = status
                break
            else:
                print("⚠ Please enter only P or A.")

    attendance[today] = daily_record

    save_json(ATTENDANCE_FILE, attendance)

    print(f"\n✅ Attendance for {today} saved successfully!")


# ─────────────────────────────────────────
#  4. VIEW ATTENDANCE BY DATE
# ─────────────────────────────────────────
def view_attendance_by_date():
    attendance = load_json(ATTENDANCE_FILE)
    students = load_json(STUDENTS_FILE)

    if not attendance:
        print("\n⚠ No attendance records found.")
        return

    print("\n--- View Attendance by Date ---")
    print("Available dates:", ", ".join(sorted(attendance.keys())))

    selected_date = input("Enter date (YYYY-MM-DD): ").strip()

    if selected_date not in attendance:
        print(f"⚠ No attendance record found for '{selected_date}'.")
        return

    print(f"\nAttendance on {selected_date}:")
    print(f"{'Roll No':<12} {'Name':<20} {'Status'}")
    print("-" * 42)

    daily = attendance[selected_date]

    present = 0
    absent = 0

    for roll, status in sorted(daily.items()):
        name = students.get(roll, "Unknown")

        label = "Present ✅" if status == "P" else "Absent ❌"

        print(f"{roll:<12} {name:<20} {label}")

        if status == "P":
            present += 1
        else:
            absent += 1

    print("-" * 42)
    print(f"Total Present: {present} | Total Absent: {absent}")


# ─────────────────────────────────────────
#  5. ATTENDANCE REPORT
# ─────────────────────────────────────────
def attendance_report():
    students = load_json(STUDENTS_FILE)
    attendance = load_json(ATTENDANCE_FILE)

    if not students:
        print("\n⚠ No students found.")
        return

    if not attendance:
        print("\n⚠ No attendance records found.")
        return

    total_days = len(attendance)

    print(f"\n--- Attendance Report (Total Days: {total_days}) ---")
    print(f"{'Roll':<8} {'Name':<20} {'Present':<10} {'Absent':<10} {'Percentage'}")
    print("-" * 60)

    highest_percentage = 0
    topper = ""

    for roll, name in sorted(students.items()):

        present = sum(
            1 for day in attendance.values()
            if day.get(roll) == "P"
        )

        absent = total_days - present

        percentage = (present / total_days * 100) if total_days > 0 else 0

        if percentage > highest_percentage:
            highest_percentage = percentage
            topper = name

        flag = " ⚠ LOW" if percentage < 75 else ""

        print(
            f"{roll:<8} {name:<20} {present:<10} "
            f"{absent:<10} {percentage:.1f}%{flag}"
        )

    print("-" * 60)

    print(f"🏆 Highest Attendance: {topper} ({highest_percentage:.1f}%)")
    print("⚠ LOW = Below 75% attendance")


# ─────────────────────────────────────────
#  6. DELETE STUDENT
# ─────────────────────────────────────────
def delete_student():
    students = load_json(STUDENTS_FILE)

    if not students:
        print("\n⚠ No students found.")
        return

    print("\n--- Delete Student ---")

    view_students()

    roll = input("\nEnter Roll Number to delete: ").strip()

    if roll not in students:
        print(f"⚠ No student found with Roll No '{roll}'.")
        return

    confirm = input(
        f"Are you sure you want to delete '{students[roll]}'? (yes/no): "
    ).strip().lower()

    if confirm == "yes":
        removed_name = students.pop(roll)

        save_json(STUDENTS_FILE, students)

        print(f"✅ Student '{removed_name}' deleted successfully.")
    else:
        print("Deletion cancelled.")


# ─────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────
def main():

    print("=" * 50)
    print("🎓 Student Attendance Management System")
    print("=" * 50)

    while True:

        print("\n📋 MENU")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Mark Attendance")
        print("4. View Attendance by Date")
        print("5. Attendance Report")
        print("6. Delete Student")
        print("0. Exit")
        print("-" * 30)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            mark_attendance()

        elif choice == "4":
            view_attendance_by_date()

        elif choice == "5":
            attendance_report()

        elif choice == "6":
            delete_student()

        elif choice == "0":
            print("\n👋 Thank you! Exiting the system.\n")
            break

        else:
            print("⚠ Invalid choice! Please enter a valid menu option.")


# ─────────────────────────────────────────
if __name__ == "__main__":
    main()