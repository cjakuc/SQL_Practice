import psycopg2
from config import config, text_path
import os.path

def rental():
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

    # How many rental IDs are there?
    total_rentals = """
    SELECT COUNT(r.rental_id)
    FROM rental as r
    """
    total_rentals_results = exec_query(total_rentals)
    # How many rental IDs are unique?
    unique_rentals = """
    SELECT COUNT(DISTINCT r.rental_id)
    FROM rental as r
    """
    unique_rentals_results = exec_query(unique_rentals)
    # Makes sense that total rentals == unique rentals because it's the primary key of rental table

    # How many total inventory IDs are there in the rental table?
    inventory_rental = """
    SELECT COUNT(r.inventory_id)
    FROM rental as r
    """
    inventory_rental_results = exec_query(inventory_rental)
    # How many unique inventory IDs are in the rental table? Are all the inventory IDs unique for each rental ID?
    ## No (there are 4580 inventory IDs in the rental table), it looks like multiple movies can be rented under the same rental or rental ID
    unique_inventory_rental = """
    SELECT COUNT(DISTINCT r.inventory_id)
    FROM rental as r
    """
    unique_inventory_rental_results = exec_query(unique_inventory_rental)

    # What is the most common inventory ID in the rental table? How many times does it show up?
    mode_inventory_rental = """
    SELECT r.inventory_id, count(*)
    FROM rental as r
    GROUP BY
        r.inventory_id
    ORDER BY
        count(*) DESC
    LIMIT 1;
    """
    mode_inventory_rental_results = exec_query(mode_inventory_rental)


    name_of_file = "exploration.txt"
    complete_name = os.path.join(text_path, name_of_file)
    f = open(complete_name, "w")
    f.write("Rental Table Questions\n")
    f.write(f"There are {total_rentals_results[0][0]} total rental IDs in the rental table\n")
    f.write(f"There are {inventory_rental_results[0][0]} total inventory IDs and {unique_rentals_results[0][0]} unique rental IDs in the rental table\n")
    f.write(f"There are {unique_inventory_rental_results[0][0]} unique inventory IDs in the rental table\n")
    f.write(f"The most common inventory ID in the rental table is {mode_inventory_rental_results[0][0]} with {mode_inventory_rental_results[0][1]} occurences\n")

    return