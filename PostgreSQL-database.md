## Creating database using PostgreSQL

> **Step 1**
> Installing the PostgresSQL app from https://postgresapp.com/
> Once downloaded open the Postgres application which takes you to a MacOS terminal

From here I created a user, database and set the user's permissions on the database created using:

>psql
>James-# CREATE USER james.gilbert [[WITH] [ENCRYPTED] PASSWORD '********'
>James-# CREATE DATABASE stock_analysis
>James-# GRANT ALL PRIVILEGES ON DATABASE stock_analysis TO james.gilbert
