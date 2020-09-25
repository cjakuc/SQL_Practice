This is a quick python project that I threw together to get some more hands on experience doing complex queries in SQL. It is very much a work in progress.

I locally hosted sample data from [here](https://www.postgresqltutorial.com/postgresql-sample-database/).

results.txt will contain the questions I seek to answer, the queries I used, and their results. printable-postgresql-sample-database-diagram is the entity-relationship diagram

exploration.txt contains the results of my exploratory queries

Queries are located in the questions folder

## Local Setup (after hosting the database locally)
* Clone this repo and cd into the directory
* `pipenv install` to create the pip enviroment
* `pipenv shell` to enter the pip enviroment
* `python connect.py` to test your connection to the local database
* `python main.py` to run main.py and create the txt files

## Thought Process:
* Follow my natural curiosities about the data to learn more about the relationships and what the characteristics are. These answers are in exploration.txt.
* Brainstorm complex questions that I would like to know the answers to. In other words, put myself in the shoes of a stakeholder who wants to know the answers to specific questions.
* Answer these specific questions with SQL queries. These answers are in results.txt.

## Some specific questions I want to answer:
* What are the 5 cities with the most rentals of Zoolander and how many rentals did they have?
    * 
