# Python CLI ORM

Python CLI ORM is a powerful command-line interface tool for managing guest and hotel information. It provides a user-friendly interface for creating, updating, and deleting guest and hotel records, as well as searching and displaying information from a database. Leveraging the capabilities of an Object-Relational Mapping (ORM) framework, this project offers seamless integration with various database backends for efficient data management.

## Features

- **Guest Management:**

  - Create, update, and delete guest records.
  - Search for guests by name or other criteria.
  - Display information about specific guests.

- **Hotel Management:**

  - Create, update, and delete hotel records.
  - Search for hotels by name or location.
  - Display information about specific hotels.

- **Command-Line Interface:**

  - User-friendly interface with clear and concise menu options.

- **ORM Integration:**
  - Seamlessly integrates with an ORM framework for database interaction.
  - Supports multiple database backends for flexibility and scalability.
  - Ensures efficient data management and retrieval.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/LueDev/Python-CLI-ORM.git
```

2. Navigate to the project directory:

```bash
cd Python-CLI-ORM
```

3. Install dependencies (if any) using pip:

```bash
pip install -r requirements.txt
```

4. Run the CLI tool:

```bash
./cli.py menu
```

## Usage

- **Create a new hotel:**

```bash
  ./cli.py create-hotel
```

- **Update an existing hotel:**

```bash
./cli.py update-hotel
```

- **Delete an existing hotel:**

```bash
./cli.py delete-hotel
```

- **Search for an existing hotel by name:**

```bash
./cli.py update-hotel
```

- **Search for an existing hotel by ID:**

```bash
./cli.py update-hotel
```
