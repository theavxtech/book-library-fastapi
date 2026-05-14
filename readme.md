 sudo -u postgres psql                  to start reading psql commands
CREATE DATABASE book_library;           to create the db beforehand
\q                                      to quit the psql queiries

uvicorn main:app --reload --port 8001   to run fastapi