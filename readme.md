 sudo -u postgres psql                  to start reading psql commands
CREATE DATABASE books;           to create the db beforehand
\q                                      to quit the psql queiries

uvicorn main:app --reload --port 8001   to run fastapi





1)project created using fastapi with 4 apis
2)converted db from sqlite to postgre
3)proper foldering structure