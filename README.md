This is a quick python project that I threw together to get some more hands on experience doing complex queries in SQL. It is very much a work in progress. I locally hosted sample data from [here](https://www.postgresqltutorial.com/postgresql-sample-database/).

`results.txt` will the questions I seek to answer, the queries I used, and their results

`printable-postgresql-sample-database-diagram` is the entity-relationship diagram

`exploration.txt` contains the results of my exploratory queries

Queries are located in the questions folder

`everything.txt` has **all** of the questions, queries, and results

**everything.txt contains ALL of the questions, queries, and results in one place**

**To view the final report, you can download the file `SQL_Practice_Report.html` and open it in a web browser, or view it directly on my portfolio page [here](https://cjakuc.github.io/PDFs/SQL_Practice_Report.html)** _If the link is saying that the page does not exist, come back in a half hour or so. It's hosted on my portfolio site and that can sometimes be slow to update and cause this error._

To view the Google Colaboratory notebooks where I did my exploratory data analysis and initially created all the visualizations, check out [this folder on my Google Drive](https://drive.google.com/drive/folders/103dp6GVmZI4ARcWXNXe5Pljn6O9ATq2r?usp=sharing).

## Local Setup (after hosting the database locally)
* Clone this repo and cd into the directory
* Edit the value of `text_path` in `config.py` to be the absolute path to my_text_files (it's probably better practice to use relative pathing)
* `pipenv install` to create the pip enviroment
* `pipenv shell` to enter the pip enviroment
* `python connect.py` to test your connection to the local database
* `python main.py` to run main.py and create the txt files in the folder `my_text_files`

## Thought Process:
* Follow my natural curiosities about the data to learn more about the relationships and what the characteristics are. These answers are in `exploration.txt`.
* Brainstorm complex questions that I would like to know the answers to. In other words, put myself in the shoes of a stakeholder who wants to know the answers to specific questions.
* Answer these specific questions with SQL queries. These answers are in `results.txt`.
* Brainstorm some more business-focused questions that the hypothetical stakeholder would want answered
* Answer the questions in a [report](https://cjakuc.github.io/PDFs/SQL_Practice_Report.html) with text and visualizations

## Some specific questions I want to answer:
* What are the 5 cities with the most rentals of Bucket Brotherhood and how many rentals did they have?
* What are the most common ratings and most common categories of the films rented by the 5 most active customers?
   * Who are the top actors in the films rented by the 5 most active customers?
* What are the average lengths of films rented in the 5 cities with the most rentals?

## Report Questions to Answer:
* Which films are most costly to replace and why?
* Over time, how popular are the different ratings and categories of films?
* Over time, how has the performance of our stores changed? If there is change, is it related to location?
* What is the current total outstanding balance of all of our customers?
