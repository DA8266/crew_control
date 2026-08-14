import pandas as pd
import textwrap
import matplotlib.pyplot as plt
import time
from datetime import datetime
import os
from tabulate import tabulate

filename = "crew_data.csv"

def load_roster():
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        print("Welcome back! Roster loaded.")
    else:
        COLUMNS = ['emp_id', 'first_n', 'last_n', 'age', 'salary', 'dept', 'hire_date', 'status']
        df = pd.DataFrame(columns=COLUMNS)
        print("Welcome to Crew Control!")

    return df

def addEmp(df_input, first_n, last_n, age, salary, dept, hire_date, status="Active"):
    """
    Adds a new employee to the dataframe and handles ID generation.

    Args:
        df_input (pd.DataFrame): The current employee roster.
        first_n (str): The employee's first name.
        last_n (str): The employee's last name.
        age (int): The employee's age in years.
        salary (float): The employee's annual salary.
        dept (str): The department name.
        hire_date (str): Date of hiring in 'YYYY-MM-DD' format.
        status (str, optional): Employment status. Defaults to 'Active'.

    Returns:
        pd.DataFrame: The updated dataframe containing the new employee.
    """

    new_id = 100 if df_input.empty else df_input['emp_id'].max() + 1
    new_data = {
        'emp_id': [new_id],
        'first_n': [first_n],
        'last_n': [last_n],
        'age': [age],
        'salary': [salary],
        'dept': [dept],
        'hire_date': [hire_date],
        'status': [status]
    }
    new_row_df = pd.DataFrame(new_data)
    return pd.concat([df_input, new_row_df], ignore_index=True)

def filter_data(df_input, column, value, operator="contains"):
    """
    Allows the user to filter the data by selecting desired column to filter.

    Args:
        df_input (pd.DataFrame): The data to be filtered.
        column (str): The column to filter.
        value (str | int): The user's input to filter by. 
        operator (str, optional): Defaults to "contains", otherwise the user's desired operator is used.

    Returns:
        pd.DataFrame: The rows that are in the filter criteria.
    """

    if isinstance(column, str):
        if column not in df_input.columns:
            return pd.DataFrame()
        target_seris = df_input[column]
    else:
        target_seris = column
    if operator == "contains":
        mask = target_seris.astype(str).str.contains(str(value), case=False, na=False)
        return df_input[mask]
    
    try:
        series_as_num = pd.to_numeric(target_seris)
        val_num = float(value)
        if operator == ">": 
            return df_input[series_as_num > val_num]
        elif operator == ">=":
            return df_input[series_as_num >= val_num]
        elif operator == "<": 
            return df_input[series_as_num < val_num]
        elif operator == "<=": 
            return df_input[series_as_num <= val_num]        
        elif operator == "=": 
            return df_input[series_as_num == val_num]        
    except ValueError:
        print(f"Error: {column} cannot be compared using math.")
        return pd.DataFrame()

def fmt_df(df):
    return tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False)

if __name__ == "__main__":
    df = load_roster()
    time.sleep(0.5)

    # Menu
    while True:
        menu = '''\
        What would you like to do?
        -[A]dd
        -[R]emove
        -[E]dit
        -[F]ilter
        -[V]isualize
        -[Q]uit
        '''
        print("--- Menu ---")
        print(textwrap.dedent(menu))
        action = input("Selection: ").lower().strip()
        match action:

            # Add
            case 'a' | 'add':
                print("--- Add Mode ---")
                first_n = input("First Name: ").title()
                last_n = input("Last Name: ").title()
                age = input("Age: ")
                salary = input("Salary: ")
                dept = input("Department: ").title()
                hire_date = input("Date Hired (YYYY-MM-DD): ")
                df = addEmp(df, first_n, last_n, age, salary, dept, hire_date)
                print(f"Success! {first_n} {last_n} has been added.")
                df.to_csv(filename, index=False)

            # Remove
            case 'r' | 'remove':
                print("--- Removal Mode ---")
                emp_id = input("Employee ID: ")
                col = 'emp_id'
                target = filter_data(df, col, emp_id)
                if target.empty:
                    print("Employee not found.")
                else:
                    print("Employee found.")
                    print(target)
                    menu = '''\
                    Removal Type:
                    [S]oft Delete
                    [H]ard Delete
                    [B]ack
                    '''
                    print(textwrap.dedent(menu))
                    action = input("Selection: ").lower()
                    match action:
                        case 's' | 'h':
                            if action == 's':
                                df.loc[df['emp_id'] == int(emp_id), 'status'] = 'Inactive'
                                print("Employee status set to Inactive.")
                            else:
                                df = df[df['emp_id'] != int(emp_id)]
                                print("Employee has been permanently deleted.")
                            df.to_csv(filename, index=False)
                        case 'b':
                            break
                        case _:
                            print("Invalid input!")

            # Edit
            case 'e' | 'edit':
                print("--- Edit Mode ---")
                print(fmt_df(df))

                while True:
                    user_id = int(input("Enter the ID of the person to be edit: "))
                    if user_id in df['emp_id'].values:
                        row = df[df['emp_id'] == user_id]
                        print("User found.")
                        print(fmt_df(row))
                        break
                    else:
                        print("User not found.")

                menu = '''\
                    Edit Menu:
                    [F]irst Name
                    [L]ast Name
                    [S]alary
                    [D]epartment 
                    [B]ack
                    '''
                print(textwrap.dedent(menu))
                action = input("Selection: ")

                match action:
                    case 'f':
                        new_first_name = input("First Name: ")
                        df.loc[df['emp_id'] == user_id, 'first_n'] = new_first_name
                        
                    case 'l':
                        new_last_name = input("Last Name: ")
                        df.loc[df['emp_id'] == user_id, 'last_n'] = new_last_name

                    case 's':
                        new_salary = input("Salary: ")
                        df.loc[df['emp_id'] == user_id, 'salary'] = new_salary

                    case 'd':
                        new_dept = input("Department: ")
                        df.loc[df['emp_id'] == user_id, 'dept'] = new_dept

                    case 'b':
                        break

                print("Updated table:")
                print(fmt_df(df))

            # Filter  
            case 'f' | 'filter':
                while True:
                    print("--- Filter Mode ---")
                    menu = '''\
                    Filter by:
                    -[I]D
                    -[N]ame
                    -[A]ge
                    -[S]alary
                    -[D]epartment
                    -[Y]ears Working
                    -[B]ack
                    '''
                    print(textwrap.dedent(menu))
                    filter = input("Selection: ").lower()
                    match filter:
                        case 'i' | 'd':
                            if filter == 'i':
                                val = input("Employee ID: ")
                                col = 'emp_id'
                            else:
                                val = input("Department: ").title()
                                col = 'dept'
                            print(fmt_df(filter_data(df, col, val)))
                        case 'n':
                            while True:
                                menu = '''
                                -[F]irst Name
                                -[L]ast Name
                                -[A]ll (full name)
                                -[B]ack
                                '''
                                print(textwrap.dedent(menu))
                                action = input("Selection: ").lower()
                                match action:
                                    case 'f':
                                        first_n = input("First Name: ")
                                        print(fmt_df(filter_data(df, 'first_n', first_n )))
                                    case 'l':
                                        last_n = input("Last Name: ")
                                        print(fmt_df(filter_data(df, 'last_n', last_n)))
                                    case 'a':
                                        full_names = df['first_n'].astype(str) + " " + df['last_n'].astype(str)
                                        full_n = input("Full Name: ")
                                        print(fmt_df(filter_data(df, full_names, full_n)))
                                    case 'b':
                                        break
                                    case _:
                                        print("Invalid input!\n")
                        case 'a' | 's' | 'y':
                            while True:
                                menu = '''
                                Choose an operator:
                                -[1] >
                                -[2] >=
                                -[3] <
                                -[4] <=
                                -[5] =
                                -[B]ack
                                '''
                                print(textwrap.dedent(menu))
                                action = input("Selection: ").lower()
                                if action == 'b':
                                    break

                                if action in ['1', '2', '3', '4', '5']:
                                    if filter == 'a':
                                        val = input("Age: ")
                                        col = 'age'

                                    elif filter == 's':
                                        val = input("Salary: ")
                                        col = 'salary'

                                    elif filter == 'y':
                                        val = input("Years Working: ")
                                        hire_dates = pd.to_datetime(df['hire_date'], errors='coerce')
                                        col = datetime.now().year - hire_dates.dt.year.fillna(0)

                                    else:
                                        print("Invalid input!")
                                
                                    match action:
                                        case '1' : op = '>'
                                        case '2' : op = '>='
                                        case '3' : op = '<'
                                        case '4' : op = '<='
                                        case '5' : op = '='
                                    result = filter_data(df, col, val, op)
                                    print(result if not result.empty else "No data found.")
                                else:
                                    print("Invalid input!")
                        case 'b':
                            print()
                            break
                        case _:
                            print("Invalid input!")

            # Visualize
            case 'v' | 'visualize':
                while True:
                    print("--- Visualization Mode ---")
                    menu = '''\
                    -[D]epartment Headcount 
                    -[S]alary Distribution
                    -[E]mployee Age Demographics 
                    -[R]etention Ratio
                    -[B]ack
                    '''
                    print(textwrap.dedent(menu))
                    action = input("Selection: ").lower().strip()

                    match action:

                        # Count by department (bar chart)
                        case 'd':
                            counts = df['dept'].value_counts()
                            plt.figure(figsize=(8, 5))
                            plt.bar(counts.index, counts.values, color='skyblue', edgecolor='black')
                            plt.title("Employee Count by Department", fontsize=14, fontweight='bold')
                            plt.xlabel("Department", fontsize=12)
                            plt.ylabel("Number of Employees", fontsize=12)
                            plt.xticks(rotation=45, ha='right')
                            plt.grid(axis='y', linestyle='--', alpha=0.7)
                            plt.tight_layout()
                            plt.show()
                            
                        # Salary distribution (histogram)
                        case 's':
                            salaries = pd.to_numeric(df['salary'], errors='coerce').dropna()

                            if salaries.empty:
                                print("No numeric salary data available.")
                                continue

                            plt.figure(figsize=(8, 5))
                            plt.hist(salaries, bins=10, color='mediumseagreen', edgecolor='black', alpha=0.8,)

                            plt.title("Salary Distribution across Roster", fontsize=14, fontweight='bold')

                            plt.xlabel("Salary ($)", fontsize=12)
                            plt.ylabel("Frequency", fontsize=12)
                            plt.grid(axis='y', linestyle='--', alpha=0.7)
                            plt.tight_layout()
                            plt.show()
                            
                        # Employee age demographics (histogram)
                        case 'e':
                            ages = pd.to_numeric(df['age'], errors='coerce').dropna()

                            if ages.empty:
                                print("No numeric age data available.")
                                continue

                            plt.figure(figsize=(8, 5))
                            plt.hist(ages, bins=8, color='coral', edgecolor='black', alpha=0.85)
                            plt.title("Employee Age Demographics", fontsize=14, fontweight='bold')
                            plt.xlabel("Age", fontsize=12)
                            plt.ylabel("Employee Count", fontsize=12)
                            plt.grid(axis='y', linestyle='--', alpha=0.7)
                            plt.tight_layout()
                            plt.show()

                        # Retention ratio (pie chart)
                        case 'r':
                            status_counts = df['status'].value_counts()

                            plt.figure(figsize=(6, 6))
                            colors = ['g' if str(s).lower() == 'active' else 'r' for s in status_counts.index]

                            plt.pie(
                                status_counts,
                                labels=status_counts.index,
                                autopct='%1.1f%%',
                                startangle=140,
                                colors=colors,
                                wedgeprops={'edgecolor': 'white', 'linewidth': 2},
                            )

                            plt.title("Employee Retention Ratio (Active vs. Inactive)", fontsize=14, fontweight='bold')
                            plt.tight_layout()
                            plt.show()
                            
                        case 'b':
                            break

                        case _:
                            print("Invalid selection! Please choose a valid option.")
                    
            case 'q' | 'quit':
                break
            case _:
                print("Invalid input!\n")
        
  

