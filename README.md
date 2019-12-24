# flask-api-practice

Database
- created sql database for users and planets
- commands to create, drop, and seed database

commands
- flask db_create 
- flask db_seed
- flask db_drop 

Routes
- "/register" - register a new user
- "/login" - takes email and password in the body, return access tokens
- "/retreive_password/<email>" - mocked through mailtrap.io
- "/planet/<id>" - returns info about the planet
- "/add_planet" - addes a planet, requires jwt token, and planet info through form
- "/update_planet" - same as above
- "/delete_planet/<id>" - requires jwt token
