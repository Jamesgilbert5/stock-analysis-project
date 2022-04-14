## Creating database using PostgreSQL

> **Step 1**
> Installing the PostgresSQL app from https://postgresapp.com/
> Once downloaded open the Postgres application which takes you to a MacOS terminal

From here I created a user, database and set the user's permissions on the database created using:

>psql

>CREATE USER james.gilbert [[WITH] [ENCRYPTED] PASSWORD '********'

>CREATE DATABASE stock_analysis

>GRANT ALL PRIVILEGES ON DATABASE stock_analysis TO james.gilbert

#ERD (Positions, Transactions, Instruments):

![Positions_Transactions_Instruments_ERD-Positions_Transactions drawio](https://user-images.githubusercontent.com/10039849/162501807-9285414c-13aa-4ef2-9e8a-d33da1a7efd4.png)
