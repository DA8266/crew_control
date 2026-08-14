# Crew Control

A lightweight, command-line employee management system built in Python. **Crew Control** allows HR administrators or team leads to manage employee records, perform targeted multi-criteria filtering, visualize demographic data, and safely persist records to a CSV storage file.

---

## Features

* **CRUD Operations**: Add new employees with auto-incrementing IDs, edit details, and perform soft or hard deletions.
* **Advanced Data Filtering**: Filter active roster by ID, name (first, last, or full name), age, department, salary, or tenure using comparison operators (`>`, `>=`, `<`, `<=`, `=`).
* **Data Visualization**: Generate clean charts powered by Matplotlib:
  * Department Headcount (Bar Chart)
  * Salary Distribution (Histogram)
  * Employee Age Demographics (Histogram)
  * Retention Ratio (Active vs. Inactive Pie Chart)
* **Formatted Console Output**: Display data tables cleanly in terminal using `tabulate`.
* **Automated Unit Testing**: Complete test coverage for data insertion and filtering logic using `pytest`.

---

## Tech Stack

* **Language**: Python 3.10+
* **Libraries & Packages**:
  * **Pandas**: Data manipulation, filtering, and CSV handling
  * **Matplotlib**: Data visualization and custom charts
  * **Tabulate**: Fancy grid formatting for console output
  * **Pytest**: Automated unit testing

