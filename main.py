import sqlite3

# Connect to database
connection = sqlite3.connect("employee_leave.db")
cursor = connection.cursor()


# Create employee table
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    leave_balance INTEGER DEFAULT 12
)
""")


# Create leave table
cursor.execute("""
CREATE TABLE IF NOT EXISTS leaves (
    leave_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    days INTEGER,
    reason TEXT,
    status TEXT DEFAULT 'Applied'
)
""")

connection.commit()


# Add employee
def add_employee():
    name = input("Enter employee name: ")
    department = input("Enter department: ")

    cursor.execute("""
    INSERT INTO employees (name, department)
    VALUES (?, ?)
    """, (name, department))

    connection.commit()

    print("Employee added successfully!")


# View employees
def view_employees():
    cursor.execute("SELECT * FROM employees")

    employees = cursor.fetchall()

    print("\n--- Employee List ---")

    if len(employees) == 0:
        print("No employees found.")
    else:
        for employee in employees:
            print(employee)


# Apply leave
def apply_leave():
    employee_id = int(input("Enter employee ID: "))
    days = int(input("Enter number of leave days: "))
    reason = input("Enter leave reason: ")

    cursor.execute(
        "SELECT leave_balance FROM employees WHERE employee_id = ?",
        (employee_id,)
    )

    employee = cursor.fetchone()

    if employee is None:
        print("Employee not found.")
        return

    leave_balance = employee[0]

    if days <= 0:
        print("Number of leave days must be greater than 0.")
        return

    if days > leave_balance:
        print("Insufficient leave balance.")
        return

    # Store leave application
    cursor.execute("""
    INSERT INTO leaves (employee_id, days, reason)
    VALUES (?, ?, ?)
    """, (employee_id, days, reason))

    # Reduce leave balance
    cursor.execute("""
    UPDATE employees
    SET leave_balance = leave_balance - ?
    WHERE employee_id = ?
    """, (days, employee_id))

    connection.commit()

    print("Leave applied successfully!")


# View leave records
def view_leave_records():
    cursor.execute("SELECT * FROM leaves")

    leaves = cursor.fetchall()

    print("\n--- Leave Records ---")

    if len(leaves) == 0:
        print("No leave records found.")
    else:
        for leave in leaves:
            print(leave)


# Approve or reject leave
def approve_reject_leave():

    cursor.execute("""
    SELECT * FROM leaves
    WHERE status = 'Applied'
    """)

    pending_leaves = cursor.fetchall()

    print("\n--- Pending Leave Requests ---")

    if len(pending_leaves) == 0:
        print("No pending leave requests.")
        return

    for leave in pending_leaves:
        print(leave)

    leave_id = int(input("\nEnter leave ID: "))

    cursor.execute(
        "SELECT employee_id, days, status FROM leaves WHERE leave_id = ?",
        (leave_id,)
    )

    leave = cursor.fetchone()

    if leave is None:
        print("Leave request not found.")
        return

    employee_id = leave[0]
    days = leave[1]
    status = leave[2]

    if status != "Applied":
        print("This leave request has already been processed.")
        return

    decision = input("Enter A to Approve or R to Reject: ").upper()

    if decision == "A":

        cursor.execute("""
        UPDATE leaves
        SET status = 'Approved'
        WHERE leave_id = ?
        """, (leave_id,))

        connection.commit()

        print("Leave approved successfully!")

    elif decision == "R":

        # Restore leave balance because leave was rejected
        cursor.execute("""
        UPDATE employees
        SET leave_balance = leave_balance + ?
        WHERE employee_id = ?
        """, (days, employee_id))

        cursor.execute("""
        UPDATE leaves
        SET status = 'Rejected'
        WHERE leave_id = ?
        """, (leave_id,))

        connection.commit()

        print("Leave rejected and leave balance restored.")

    else:
        print("Invalid choice. Please enter A or R.")


# Main menu
while True:

    print("\n===== EMPLOYEE LEAVE MANAGEMENT SYSTEM =====")
    print("1. Add Employee")
    print("2. View Employees")
    print("3. Apply Leave")
    print("4. View Leave Records")
    print("5. Approve/Reject Leave")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_employee()

    elif choice == "2":
        view_employees()

    elif choice == "3":
        apply_leave()

    elif choice == "4":
        view_leave_records()

    elif choice == "5":
        approve_reject_leave()

    elif choice == "6":
        print("Thank you for using the system!")
        break

    else:
        print("Invalid choice. Please try again.")


# Close database
connection.close()