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

- **Display all hotels:**

```bash
./cli.py display-all-hotels
```

- **Search for an existing hotel by name:**

```bash
./cli.py search-hotel-by-name
```

- **Search for an existing hotel by ID:**

```bash
./cli.py search-hotel-by-id
```

- **Create a new guest:**

```bash
./cli.py create-guest
```

- **Update an existing guest:**

```bash
./cli.py update-guest
```

- **Delete a guest:**

```bash
./cli.py delete-guest
```

- **Search for an existing guest by ID:**

```bash
./cli.py search-for-guest-by-id
```

- **Search for an existing guest by name:**

```bash
./cli.py search-for-guest-by-name
```

- **Display all guests:**

```bash
./cli.py display-all-guests
```

## Configuration

The Python CLI ORM tool is designed to be flexible and customizable. You can configure certain aspects of the tool to suit your specific needs.

## Contributing

Contributions to the Python CLI ORM project are welcome! If you'd like to contribute code, report bugs, or suggest new features, please follow these guidelines:

1. **Fork the Repository**: Fork the project repository on GitHub and clone your fork to your local machine.

2. **Create a Branch**: Create a new branch for your changes and switch to it.

3. **Make Changes**: Make your desired changes to the codebase. Ensure that your changes adhere to the project's coding style and conventions.

4. **Test Changes**: Test your changes thoroughly to ensure they work as expected and don't introduce any regressions.

5. **Submit Pull Request**: Once you're satisfied with your changes, push your branch to your fork on GitHub and submit a pull request to the main project repository.

6. **Follow Up**: Respond to any feedback or review comments promptly and make any necessary revisions to your pull request.

7. **Incorporate into Your Own Business Application**: Feel free to incorporate elements of the Python CLI ORM tool into your own custom business applications. The modular and customizable nature of the tool allows you to adapt and integrate specific features or components to meet your unique requirements.

For more information on contributing, including guidelines for code style, testing, and documentation, refer to the CONTRIBUTING.md file in the project repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
