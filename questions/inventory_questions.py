import psycopg2
from config import config, text_path
import os.path
from questions.questions_helper import write_questions_queries_results

def inventory():
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

    # Are there duplicate films in the inventory table?
    ## Yes, there are 4581 total film IDs and 958 unique film IDs
    ### That means some of the films are in multiple locations but some of the films in the system are not in inventory at all (1000 > 958)
    questions.append("Are there duplicate films in the inventory table?")
    films_inventory = """
    SELECT COUNT(i.film_id), COUNT(DISTINCT i.film_id)
    FROM inventory as i
    """
    queries.append(films_inventory)
    films_inventory_results = exec_query(films_inventory)
    final_results.append(films_inventory_results)

    # What 5 film IDs occur the most in the inventory table?
    questions.append("What 5 film IDs occur the most in the inventory table?")
    top_film = """
    SELECT i.film_id, COUNT(*)
    FROM inventory as i
    GROUP BY
        i.film_id
    ORDER BY
        COUNT(*) DESC
    LIMIT 5
    """
    queries.append(top_film)
    top_film_results = exec_query(top_film)
    final_results.append(top_film_results)
    # What are the titles of those films?
    titles = []
    for i, film in enumerate(top_film_results):
        questions.append(f"What is the title of the {i}th film?")
        query = f"""
        SELECT f.title
        FROM film as f
        WHERE
            f.film_id = {film[0]}
        """
        queries.append(f"   {query}")
        query_results = exec_query(query)
        titles.append(query_results[0][0])
        final_results.append(f"    {query_results[0][0]}")


    name_of_file = "exploration.txt"
    complete_name = os.path.join(text_path, name_of_file)
    f = open(complete_name, "a")
    f.write(f"\nInventory Table Questions\n")
    f.write(f"In the inventory table, there are {films_inventory_results[0][0]} film IDs and {films_inventory_results[0][1]} unique film IDs\n")
    f.write(f"The film IDs that occur most in the inventory table are: {top_film_results}\n")
    f.write(f"  The titles of those films are: {titles}\n")

    f.close()

    write_questions_queries_results(questions,queries,final_results,filename="Inventory Questions")

    return