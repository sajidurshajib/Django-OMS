# 📦 Order Management System API

This project demonstrates a well-structured Django project for assessment purposes.


## ⚙️ Setup & Run

1. Create your environment file:
	```sh
	cp .env.example .env
	# Edit .env as needed
	```

2. Build and run the project with Docker:
	```sh
	make build
	make run
	```

That's it! The project will be running in Docker containers.


## 🚀 Features

- User authentication (JWT & session-based)
- User registration, profile, password update, and customer report (total spent)
- Superuser and owner-based permissions for sensitive actions
- Product Variant management (CRUD, decimal price fields)
- Order management: create, update, delete orders and order items
- Add or remove items from orders (with quantity and price auto-calculation)
- CustomerProfile model with auto-updated total_spent using Django signals
- API documentation with Swagger (drf-yasg)
- PostgreSQL database support
- Dockerized setup with Nginx and Gunicorn for production
- Static file handling and CORS support


## 📜 Formatter

This project uses [ruff](https://github.com/astral-sh/ruff) for code formatting and linting.

To automatically format and fix all code style issues, run:

```sh
make ruff-all
```

