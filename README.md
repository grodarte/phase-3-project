# Personal Earnings Tracker (Phase 3 Project)

## Overview

This is a command-line application that helps shift workers like servers or bartenders track hours worked, tips earned, and pay over time. The app uses a local SQLite database. Users interact with the database entirely via a custom CLI interface that supports viewing, creating, updating, and deleting shift records and pay periods.

---

## `cli.py` – The Command-Line Interface

This file contains the core user experience of the app. When run, it prompts the user to select actions like:

- **Add a Shift:** Record clock-in and clock-out times, tip amounts, and assign to the selected pay period.
- **View Shifts by Pay Period:** Select a pay period to view all related shifts.
- **Edit a Shift:** Update an existing record’s times, or tips.
- **Delete a Shift:** Remove a shift from the database.
- **Create/Delete/Update Pay Periods:** Manage pay periods independently.
- **View Pay Period Summaries:** View earnings per period such as total tips, hourly and overtime wages, and expected gross pay.

The CLI guides users with prompts, input validation, and clear feedback. It acts as the app’s main navigation layer and is the entry point of the program.

---

## `helpers.py` – CLI Utility Functions

This file contains all the support functions that keep the CLI clean and readable. It handles all input prompts, data formatting, and helper logic. Notable functions include:

### Pay Period Helpers
* `get_payperiods()` fetches all existing pay periods from the database.

* `enumerate_payperiods()` displays a numbered list of all pay periods with readable dates to help the user choose one.

* `create_payperiod()` prompts the user for a start and end date (month, day, year) and creates a new pay period entry.

* `update_payperiod()` allows the user to select a pay period and update its dates.

* `delete_payperiod()` allows the user to select a pay period and delete it from the database after confirmation, along with any shifts associated with that pay period.

* `calculate_payperiod_earnings(pay_period)` computes and prints a summary of total tips, hours worked, hourly and overtime wages, and expected gross pay for a given pay period.

### Shift Helpers
* `get_shifts()` retrieves all shifts from the database, sorted by pay period.

* `enumerate_shifts(shifts)` displays a numbered list of shift dates for the user to browse or select from.

* `display_shift_details(shift)` prints detailed information for a single shift, including date, hours worked, and tip amount.

* `create_shift()` guides the user through entering a new shift: clock-in/out time, tip amount, and assigning it to a pay period.

* `update_shift()` lets the user select and modify an existing shift's date, time, and tips.

* `delete_shift()` deletes a selected shift from the database after confirmation.

This file helps separate interface logic from the main CLI flow and keeps `cli.py` focused on structure rather than input/output logic.

---

## `models/payperiod.py` – The `PayPeriod` Model

This file defines the `PayPeriod` class, which models a single earnings period with a defined start and end date. Each instance is stored in a local dictionary and persisted in a SQLite database. It is linked to multiple `Shift` instances via a foreign key relationship, enabling the user to analyze and group shifts across date ranges. Like `Shift`, this class includes property setters that enforce valid date inputs and prevent malformed data from entering the system.

### Attributes:
- `id` – Unique identifier (primary key).
- `smonth`, `sday`, `syear` – Start date (month, day, year).
- `emonth`, `eday`, `eyear` – End date (month, day, year).

### Properties:
Each date component (e.g., `smonth`, `eday`, etc.) includes a property with validation logic that ensures input values are within acceptable ranges. For example, years must be between 2000–2026, and months must be 1–12.

### Methods:

#### Database Management
- **`create_table()`** – Creates the `payperiods` table in the database with columns for start and end date values.
- **`drop_table()`** – Deletes the `payperiods` table entirely.
- **`save()`** – Inserts the current pay period into the database and assigns its `id`.
- **`create()`** – Class method that initializes and saves a new `PayPeriod` instance in one step.
- **`update()`** – Updates the table row for the current instance with any new start/end date changes.
- **`delete()`** – Deletes the row corresponding to the instance and removes it from the class-level dictionary.

#### Record Access
- **`instance_from_db(row)`** – Returns a `PayPeriod` instance from a database row. If the instance already exists in memory, it returns the existing object instead of creating a new one.
- **`get_all()`** – Retrieves and returns a list of all pay periods in the database.
- **`find_by_id(id)`** – Looks up a pay period by its `id` and returns the corresponding instance, or `None` if not found.

#### Relationship to Shifts
- **`shifts()`** – Returns all `Shift` instances from the database that are associated with this pay period (via `payperiod_id`). This supports earnings summaries and grouping logic in the CLI.

The `PayPeriod` class is an essential part of the data model, acting as the organizing unit for all shifts and enabling historical earnings tracking by date range. It plays a key role in filtering and summarizing data throughout the app.

---

## `models/shift.py` – The Shift Model
This file defines the Shift class, which represents a single work shift in the database. Each shift includes the date, clock-in and clock-out times, credit card and cash tips, and a foreign key linking it to a pay period. The class includes custom validation logic through Python properties and uses SQLite for data persistence. It also stores all instances in a class-level dictionary (Shift.all) keyed by their database ID for quick access and lookup.

### Attributes:
* `id` – Unique identifier for the shift (automatically assigned).

* `month`, `day`, `year` – Components of the shift date.

* `clock_in`, `clock_out` – Time strings in "HH:MM" 24-hour format.

* `cc_tip`, `cash_tip` – Tip amounts from credit card and cash, respectively.

* `payperiod_id` – Links the shift to a specific pay period.

### Methods:
#### Initialization and Validation
* `__init__` – Initializes a Shift instance with full validation of dates, times, and tip amounts.

* `_validate_time(time_str)` – Ensures that time strings follow "HH:MM" 24-hour format.

* `_validate_tip(tip)` – Ensures that tips are non-negative floats rounded to two decimal places.

* Properties for `month`, `day`, `year`, `clock_in`, `clock_out`, `cc_tip`, `cash_tip`, and `payperiod_id` – Each has a custom setter that validates inputs and raises errors for incorrect formats or values.

#### Database Interaction
* `create_table()` – Creates the `shifts` table if it doesn’t already exist, with columns for date, time, tips, and pay period association.

* `drop_table()` – Deletes the `shifts` table from the database.

* `save()` – Inserts a new shift into the database and stores the instance in the `Shift.all` dictionary.

* `create()` – Class method to create and immediately save a new `Shift` instance.

* `update()` – Updates the corresponding database row with the instance’s current attribute values.

* `delete()` – Removes the shift from both the database and the in-memory `Shift.all` dictionary.

#### Fetching and Finding
* `get_all()` – Returns a list of all shift instances from the database.

* `find_by_id(id)` – Returns the shift instance with the matching `id`, or `None` if not found.

* `instance_from_db(row)` – Internal method that converts a database row into a Shift instance, avoiding duplicate objects by checking the Shift.all dictionary first.

This class is a foundational part of the app. It not only holds detailed data for every work shift, but also performs input validation, manages database persistence, and powers the calculations used in CLI summaries.

---

## `debug.py` – Development and Testing Setup

This script is used for seeding the database with test data and interactively debugging the app during development. It imports the app, opens a database session, and pre-populates tables with sample shifts and pay periods so features can be tested without entering data manually every time.

Not required for the user, but helpful for developers during testing.

---

## `models/__init__.py` – ORM Setup and Models

This file initializes the SQLite database connection used across the app.

`sqlite3.connect('earnings.db')`
Connects to (or creates) a local SQLite database file called `earnings.db`.

`CONN` and `CURSOR`
These are globally accessible objects used to execute raw SQL statements throughout the program, such as creating tables or running queries.

This setup allows the CLI and helper functions to interact with the database directly using SQL commands. While some parts of the app use an ORM-like structure, this file keeps the core connection simple and direct using Python’s built-in `sqlite3` module.

---

## Summary

This project is a fully functional CLI application for tracking personal earnings over time. It is built using Python and SQLite, with a focus on:

- Clean, modular code separated across multiple files
- Robust input validation to prevent errors and maintain data integrity
- Persistent storage via a relational database
- A user-friendly interface with clear prompts and summaries
- A one-to-many relationship between `PayPeriod` and `Shift`, modeled using foreign keys

The CLI allows users to manage shifts and pay periods, analyze tips and hours worked, and correct mistakes by editing or deleting entries. All logic is abstracted into helper functions and model methods to keep the application organized and extensible.

This app is useful for service industry workers (like servers or bartenders) to gain insight into their pay patterns and track progress over time.

---

## Future Improvements
* Export data to CSV

* Add analytics like best earning days/hours

* Implement user authentication for multiple users

---

## Author

Gabrielle Rodarte – [grodarte](https://github.com/grodarte)