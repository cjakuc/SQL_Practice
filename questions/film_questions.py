import psycopg2
from config import config, text_path
import os.path

def film():
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

    # Just look at ALL the films to test everything is working and do some exploration
    film_query = """
    SELECT *
    FROM film
    """
    results = exec_query(film_query)
    # print(results)
    # It's a lot
    # Check that it's a list of tuples and looks as expected
    # print(results[:2])


    # Lets get a list of all the films and write it to all_films.txt
    all_film_titles = """
    SELECT title
    FROM film
    """
    all_films_results = exec_query(all_film_titles)

    name_of_file = "all_films.txt"
    complete_name = os.path.join(text_path, name_of_file)
    f = open(complete_name, "w")
    f.write("All the movie titles:\n")
    # Write all the movie titles
    for i, v in enumerate(all_films_results):
        if i == len(all_films_results) - 1:
            f.write(str(v[0]))
        else:
            f.write(f"{v[0]},")
    f.close()

    # How many unique film titles are there?
    ## 1000
    unique_titles = """
    SELECT COUNT(DISTINCT f.title)
    FROM film as f
    """
    unique_titles_results = exec_query(unique_titles)

    # What is the title of the film (inventory ID = 1489, most common i.ID in rental)?
    title_i1489 = """
    SELECT f.title
    FROM film as f
    LEFT JOIN inventory USING (film_id)
    WHERE
        inventory.inventory_id = 1489
    """
    title_i1489_results = exec_query(title_i1489)

    name_of_file = "exploration.txt"
    complete_name = os.path.join(text_path, name_of_file)
    f = open(complete_name, "w")
    f.write("Film Table Questions\n")
    f.write(f"There are {unique_titles_results[0][0]} unique film titles in the film table\n")
    f.write(f"The title of the most common inventory ID in the rental table (inv ID = 1489) is {title_i1489_results}\n")

    f.write("\n")
    f.close()

    return