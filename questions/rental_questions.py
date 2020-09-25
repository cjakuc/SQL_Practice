import psycopg2
from config import config, text_path
import os.path
from questions.questions_helper import write_questions_queries_results

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

    # Instantiate lists for the questions, queries, and results
    questions = []
    queries = []
    final_results = []

    # How many rental IDs are there?
    questions.append("How many rental IDs are there?")
    total_rentals = """
    SELECT COUNT(r.rental_id)
    FROM rental as r
    """
    queries.append(total_rentals)
    total_rentals_results = exec_query(total_rentals)
    final_results.append(total_rentals_results)
    # How many rental IDs are unique?
    questions.append("How many rental IDs are unique?")
    unique_rentals = """
    SELECT COUNT(DISTINCT r.rental_id)
    FROM rental as r
    """
    queries.append(unique_rentals)
    unique_rentals_results = exec_query(unique_rentals)
    final_results.append(unique_rentals_results)
    # Makes sense that total rentals == unique rentals because it's the primary key of rental table

    # How many total inventory IDs are there in the rental table?
    questions.append("How many total inventory IDs are there in the rental table?")
    inventory_rental = """
    SELECT COUNT(r.inventory_id)
    FROM rental as r
    """
    queries.append(inventory_rental)
    inventory_rental_results = exec_query(inventory_rental)
    final_results.append(inventory_rental_results)
    # How many unique inventory IDs are in the rental table? Are all the inventory IDs unique for each rental ID?
    ## No (there are 4580 inventory IDs in the rental table), it looks like multiple movies can be rented under the same rental or rental ID
    questions.append("How many unique inventory IDs are in the rental table? Are all the inventory IDs unique for each rental ID?")
    unique_inventory_rental = """
    SELECT COUNT(DISTINCT r.inventory_id)
    FROM rental as r
    """
    queries.append(unique_inventory_rental)
    unique_inventory_rental_results = exec_query(unique_inventory_rental)
    final_results.append(unique_inventory_rental_results)

    # What is the most common inventory ID in the rental table? How many times does it show up?
    questions.append("What is the most common inventory ID in the rental table? How many times does it show up?")
    mode_inventory_rental = """
    SELECT r.inventory_id, count(*)
    FROM rental as r
    GROUP BY
        r.inventory_id
    ORDER BY
        count(*) DESC
    LIMIT 1;
    """
    queries.append(mode_inventory_rental)
    mode_inventory_rental_results = exec_query(mode_inventory_rental)
    final_results.append(mode_inventory_rental_results)


    name_of_file = "exploration.txt"
    complete_name = os.path.join(text_path, name_of_file)
    f = open(complete_name, "a")
    f.write("Rental Table Questions\n")
    f.write(f"There are {total_rentals_results[0][0]} total rental IDs in the rental table\n")
    f.write(f"There are {inventory_rental_results[0][0]} total inventory IDs and {unique_rentals_results[0][0]} unique rental IDs in the rental table\n")
    f.write(f"There are {unique_inventory_rental_results[0][0]} unique inventory IDs in the rental table\n")
    f.write(f"The most common inventory ID in the rental table is {mode_inventory_rental_results[0][0]} with {mode_inventory_rental_results[0][1]} occurences\n")

    f.close()

    write_questions_queries_results(questions,queries,final_results,filename="Rental Questions")

    return