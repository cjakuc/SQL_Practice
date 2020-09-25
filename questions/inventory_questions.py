import psycopg2
from config import config, text_path
import os.path

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

    # Are there duplicate films in the inventory table?
    ## Yes, there are 4581 total film IDs and 958 unique film IDs
    ### That means some of the films are in multiple locations but some of the films in the system are not in inventory at all (1000 > 958)
    films_inventory = """
    SELECT COUNT(i.film_id), COUNT(DISTINCT i.film_id)
    FROM inventory as i
    """
    films_inventory_results = exec_query(films_inventory)


    name_of_file = "exploration.txt"
    complete_name = os.path.join(text_path, name_of_file)
    f = open(complete_name, "a")
    f.write(f"\nInventory Table Questions\n")
    f.write(f"In the inventory table, there are {films_inventory_results[0][0]} film IDs and {films_inventory_results[0][1]} unique film IDs\n")

    f.close()
    return