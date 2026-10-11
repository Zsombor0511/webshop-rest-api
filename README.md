# Webshop REST API

University Python course project (ELTE): a small REST API for a webshop, built with FastAPI. It manages users, shopping baskets and basket items, and stores the data in a JSON file.

> The API messages and the documentation are in Hungarian (course assignment), this README is in English.

## Features

- 11 endpoints for users, baskets and items: add, update, delete, query, and basket total price
- Input validation with Pydantic (non-negative numbers, e-mail format)
- Error handling with `HTTPException` and proper HTTP status codes (201, 400, 404, 422)
- Backup and restore endpoints for the data file (`/save`, `/reload`)
- Documentation with test cases for every endpoint (successful and error scenarios): [docs/documentation.pdf](docs/documentation.pdf)

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Welcome message |
| POST | `/adduser` | Add a new user |
| POST | `/addshoppingbag` | Create an empty basket for a user |
| POST | `/additem` | Add an item to a user's basket |
| PUT | `/updateitem` | Update an item in a user's basket |
| DELETE | `/deleteitem` | Delete an item from a user's basket |
| GET | `/user` | Get a user by id |
| GET | `/users` | List all users |
| GET | `/shoppingbag` | List the items in a user's basket |
| GET | `/getusertotal` | Total price of a user's basket |
| POST | `/save` | Copy the data file to a backup file |
| POST | `/reload` | Restore the data file from a backup file |

## How to run

```
pip install -r requirements.txt
uvicorn main:app --reload --port 9000
```

- The API runs at `http://127.0.0.1:9000`
- Interactive Swagger UI: `http://127.0.0.1:9000/docs`
- Alternative documentation: `http://127.0.0.1:9000/redoc`

## Project structure

```
main.py              # application entry point
routers/routes.py    # endpoints and error handling
schemas/schema.py    # Pydantic models (User, Basket, Item) with validation
data/filehandler.py  # writing to the JSON data file
data/filereader.py   # reading from the JSON data file
data/data.json       # sample data
docs/                # documentation with test cases (PDF)
```

## Tech

Python, FastAPI, Uvicorn, Pydantic

## Known limitations

This is a course project, not production code:

- Data is stored in a JSON file, without locking, so it is not safe for concurrent use
- The `/save` and `/reload` endpoints accept file names from the client without restricting them to the data folder; a production version should only allow a fixed list of backup files
- There is no authentication
