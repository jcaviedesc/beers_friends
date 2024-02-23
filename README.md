# Beer Friends

## Description

This is a FastAPI application for managing beer orders among friends.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management. To install the dependencies, run:

```bash
poetry install
```

## Usage

### Running the Server

To start the FastAPI server, run:

```bash
poetry run uvicorn beer_friends.main:app --reload
```

Endpoints
The application has the following endpoints:

- `GET /beers`: Lists all available beers.
- `POST /order`: Receives an order. The order should be a list of beers.
- `GET /bill`: Gets the total bill.
- `POST /pay`: Pay order.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

This README includes sections for the project title, installation instructions, how to run the server, a list of endpoints, a note on contributing, and the license. You can customize this to fit your project's needs.

This README includes sections for the project title, installation instructions, how to run the server, a list of endpoints, a note on contributing, and the license. You can customize this to fit your project's needs.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

This README includes sections for the project title, installation instructions, how to run the server, a list of endpoints, a note on contributing, and the license. You can customize this to fit your project's needs.

This README includes sections for the project title, installation instructions, how to run the server, a list of endpoints, a note on contributing, and the license. You can customize this to fit your project's needs.
