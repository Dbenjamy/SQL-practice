# Overview

The goal of this personal project is to become more familiar with SQL relational databases by building up query commands in a user friendly way.

In this implementation I used sqlite3 in Python to build and access my database. Before running the program you will need to provide the path to your database. I have only tested it within the same hard drive. When prompted you can choose to manually enter data, import data, delete entries or tables, and make queries. Currently, the query function has not been built. Will update this if I finish it.

SQL is used in many industies to manage large amount of data. Building this seems to me an essential stepping stone as I work towards a career in machine learning and data science.

[Software Demo](https://youtu.be/jSRrxVZq8BM)

# Relational Database

I am using the United States PUMS survey data. It is a collection of a large range
of demographics about people including education, race and ethnicity, and income
to name a few.

The structure of the current tables in the database are just duplicates of the
data from those surveys.

# Development Environment

I created this in Python using the sqlite3 library. I used VSCode as I do with most
programs I write.

# Useful Websites
Aside from some stack overflow, the documentation I found was very informative.
* [SQLite 3 Documentation](https://docs.python.org/3/library/sqlite3.html)

# Future Work
Some bugs to work out:
* Finish query function
* Make creating tables more resilient (you can currently break them on import)
* (Maybe) add functionality to generate charts for quick correlational discovery