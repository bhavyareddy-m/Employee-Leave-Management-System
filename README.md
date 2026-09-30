# Employee Leave Management System

A simple Employee Leave Management System developed using Python and SQLite.

## Project Description

This project is a console-based application that helps manage employee information and leave requests.

The system allows users to:

- Add employees
- View employee details
- Apply for leave
- Check leave balance
- View leave records
- Approve or reject leave requests
- Update leave balance automatically

## Technologies Used

- Python
- SQLite
- SQL

## Features

### 1. Add Employee
Allows the user to add an employee with their name and department.

### 2. View Employees
Displays employee ID, name, department, and available leave balance.

### 3. Apply Leave
Employees can apply for leave by entering their employee ID, number of leave days, and reason.

### 4. Leave Balance Validation
The system checks whether the employee has sufficient leave balance before accepting the request.

### 5. Approve or Reject Leave
Pending leave requests can be approved or rejected.

### 6. Database Management
Employee and leave information is stored using SQLite.

## Database Tables

### Employees

- employee_id
- name
- department
- leave_balance

### Leaves

- leave_id
- employee_id
- days
- reason
- status

## How to Run

1. Install Python.
2. Download or clone this repository.
3. Open the project folder in VS Code.
4. Open the terminal.
5. Run:

```bash
python main.py