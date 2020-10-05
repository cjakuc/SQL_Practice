import psycopg2
from config import config, text_path
import os.path
from questions.questions_helper import write_questions_queries_results
import plotly
import pandas as pd

# Reference for embedding plotly figures into Markdown: http://www.kellieottoboni.com/posts/2017/08/plotly-markup/

def report():
    # read connection parameters
    params = config()
    # connect to the PostgreSQL server
    conn = psycopg2.connect(**params)
    # create a cursor
    cur = conn.cursor()

    # Function to execute a query and return all of the results (list)
    def exec_query(query: str):
        cur.execute(query)
        return cur.fetchall()

    # Instantiate lists for the questions, queries, and results
    # questions = []
    # queries = []
    # final_results = []

    # Which films are most costly to replace and why?
    costly_films = """
    SELECT *
    FROM film
    """
    costly_df = pd.read_sql_query(costly_films, conn)
    costly_df.to_csv(path_or_buf=r"C:\Users\Chris\Desktop\Career\ComplexPGSQL\sample_complex\report_CSVs\costly_df.csv")
    

    # Over time, how popular are the different ratings and categories of films?
    popular_films = """
    SELECT film.title, category.name, film.rating, film.rental_duration, film.rental_rate, film.length, film.replacement_cost, film.special_features, rental.rental_date
    FROM rental
        LEFT JOIN inventory USING (inventory_id)
        LEFT JOIN film USING (film_id)
        LEFT JOIN film_category USING (film_id)
        LEFT JOIN category USING (category_id)
    """
    popular_df = pd.read_sql_query(popular_films, conn)
    popular_df.to_csv(path_or_buf=r"C:\Users\Chris\Desktop\Career\ComplexPGSQL\sample_complex\report_CSVs\popular_df.csv")


    # Over time, how has the performance of our stores changed? If there is change, is it related to location?
    # questions.append("Over time, how has the performance of our stores changed? If there is change, is it related to location?")
    # stores = """

    # """
    # queries.append(stores)
    # stores_results = exec_query(stores)
    # final_results.append(stores_results)


    # What is the current total outstanding balance of all of our customers?
    # questions.append("What is the current total outstanding balance of all of our customers?")
    # balance = """

    # """
    # queries.append(balance)
    # balance_results = exec_query(balance)
    # final_results.append(balance_results)


    # name_of_file = "report.txt"
    # complete_name = os.path.join(text_path, name_of_file)
    # f = open(complete_name, "w")
    # f.write(f"\Report Questions\n")
    # for i in range(len(questions)):
    #     f.write(f"\n    Question: {questions[i]}\n")
    #     f.write(f"  {queries[i]}\n")
    #     f.write(f"      {final_results[i]}\n")
    # f.write(f"\n")

    # f.close()

    # write_questions_queries_results(questions,queries,final_results,filename="Report Questions")

    return