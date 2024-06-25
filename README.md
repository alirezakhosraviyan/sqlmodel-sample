
# Sample Project For SQLModels
# Instructions

## How to use backend ?

### - login

    1. Create a User
    2. Login to application using "authorize" button on top of openapi docs (optionally you can use username: alireza, password: 1234)
    
    note : ( creating user and generating token are public APIs but other APIs are secured and you need to login via "authorize" button on top )


### - adding an issue
    
    (make sure you are logged in)
    1. Create a product first ( if you haven't already created one )
    2. Create an issue
    3. fetch all issues


### - update an issue

    (make sure you are logged in)
    1. Create an issue first ( if you haven't already created one )
    2. you can update fields (status, severity, and assignee)
    3. fetch all issues or retrive issue by ID

    Sample Input Data

    {
      "description": "This is a test issue made by Alireza",
      "severity": "critical", 
      "product": "product1", # product name of an already created product (id could be a better approach but since you mentioned in AC that you want to make create by name)
      "reporter": "alireza"  # username of an already created user
    }

## API Reference

#### Get all issues

```http
  GET /api/v1/issues
```


#### Get issue

```http
  GET /api/v1/issues/${issue_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `issue_id`      | `number` | **Required**. Id of issue to fetch |


#### Post issue

```http
  POST /api/v1/issues
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `description`      | `string` | **Required**|
| `severity`      | `string` | **Required** can be from (critical, medium, low)|
| `product`      | `string` | **Required** product name|
| `reporter`      | `string` | **Required** username of an already created user|


#### Edit issue partially

```http
  PATCH /api/v1/issues/${issue_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `status`      | `string` | **Optional** can be from (new, in_progress, in_review, done)|
| `severity`      | `string` | **Optional** can be from (critical, medium, low)|
| `assignee`      | `string` | **Optional** username of an already created user|



#### Get all products

```http
  GET /api/products/
```


#### Post product

```http
  POST /api/v1/products/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `name`      | `string` | **Required**|


#### Create User

```http
  POST /api/v1/register/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**|
| `password`      | `string` | **Required**|
| `fullname`      | `string` | **Required**|


#### Creating an access token for user

```http
  POST /api/v1/token/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**|
| `password`      | `string` | **Required**|

## Run Locally

Clone the project

```bash
  git clone git@github.com:alirezakhosraviyan/sqlmodel-sample.git
```

Go to the project directory

```bash
  cd sqlmodels
```

Install dependencies (optional, if you don't already have it)

-  Install docker-compose from [here](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04)

Start all servers

```bash
  docker-compose up -d
```

Tear down the containers (Optional)
```bash
  docker-compose down -v
```

Access Servers:

* Backend: http://0.0.0.0:8000/docs
# Technical Notes

- **`Domain-Driven-Design`**: One of the non-functional requirements of the project is scalability, which led me to use Domain-Driven Design for the backend file structure. It makes the project loosely coupled and will be easier to divide into different services. (domains: auth, issues, products)

- **`AsyncIO`** : Since the code is mostly IO-bound and not CPU-bound, using async programming helps the code be faster and more responsive.

- **`Sqlmodel`** : Helps code reusability, supported by fastapi, on top of SQLAlchemy, supports async programming, validation with pydantic

- **`Ruff`** : An extremely fast Python linter and code formatter, written in Rust 🦞, ( instead of : pylint, black, isort, etc)

- **`tests`** : Backend has enough tests (17 tests) to cover all APIs to showcase my skill in creating tests but surely for production ready products we can always have more tests

- **`Gitlab-CI`** : Checks the code quality and tests automatically to ensure the delivery of high-quality code.

## Tech Stack

**Server:** Python, Fastapi, Postgresql, Sqlmodel, Pydantic, Alembic, JWT, Asyncio, Pytest, Ruff (all linters), MyPy, Docker, Docker-Compose, gitlab-ci


