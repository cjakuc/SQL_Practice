import psycopg2
from config import config, text_path
import os.path
from questions.questions_helper import write_questions_queries_results

def final():
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
    questions = []
    queries = []
    final_results = []

    # What are the 5 cities with the most rentals of Bucket Brotherhood and how many rentals did they have?
    questions.append("What are the 5 cities with the most rentals of Bucket Brotherhood and how many rentals did they have?")
    cities_fh = """
    SELECT city.city, COUNT(*)
    FROM rental as r
    LEFT JOIN inventory USING (inventory_id)
    LEFT JOIN customer USING (customer_id)
    LEFT JOIN address USING (address_id)
    LEFT JOIN city USING (city_id)
    WHERE
        inventory.film_id = (
            SELECT film.film_id
            FROM film
            WHERE
                film.title = 'Bucket Brotherhood'
        )
    GROUP BY
        city.city
    ORDER BY
        COUNT(*) DESC
    LIMIT 5
    """
    queries.append(cities_fh)
    cities_fh_results = exec_query(cities_fh)
    final_results.append(cities_fh_results)




    name_of_file = "results.txt"
    complete_name = os.path.join(text_path, name_of_file)
    f = open(complete_name, "w")
    f.write(f"\nFinal Questions\n")
    f.write(f"The 5 cities with the most rentals of Flying Hook and their rental counts are: {cities_fh_results}\n")
    f.write(f"\n")

    f.close()

    write_questions_queries_results(questions,queries,final_results,filename="Final Questions")

    return