import psycopg2
from config import config, text_path
import os.path
from questions.questions_helper import write_questions_queries_results

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

    # Instantiate lists for the questions, queries, and results
    questions = []
    queries = []
    final_results = []

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
    questions.append("How many unique film titles are there?")
    unique_titles = """
    SELECT COUNT(DISTINCT f.title)
    FROM film as f
    """
    queries.append(unique_titles)
    unique_titles_results = exec_query(unique_titles)
    final_results.append(unique_titles_results)

    # What is the title of the film (inventory ID = 1489, most common i.ID in rental)?
    ## Flying Hook
    questions.append("What is the title of the film (inventory ID = 1489, most common i.ID in rental)?")
    title_i1489 = """
    SELECT f.title
    FROM film as f
    LEFT JOIN inventory USING (film_id)
    WHERE
        inventory.inventory_id = 1489
    """
    queries.append(title_i1489)
    title_i1489_results = exec_query(title_i1489)
    final_results.append(title_i1489_results)
    # How many times was Flying Hook rented?

    # Combine the most common rental ID query with the query to get it's title
    questions.append("Combine the most common rental ID query with the query to get it's title")
    combo_fh = """
    SELECT f.title
    FROM film as f
    LEFT JOIN inventory USING (film_id)
    WHERE
        inventory.inventory_id = (
            SELECT r.inventory_id
            FROM rental as r
            GROUP BY
                r.inventory_id
            ORDER BY
                count(*) DESC
            LIMIT 1
        )
    """
    queries.append(combo_fh)
    combo_fh_results = exec_query(combo_fh)
    final_results.append(combo_fh_results)

    # Who are the customers that rented Flying Hook?
    questions.append("Who are the customers that rented Flying Hook?")
    flying_hook = """
    SELECT CONCAT (c.first_name, ' ', c.last_name)
    FROM customer as c
    FULL OUTER JOIN rental as r USING (customer_id)
    WHERE
        r.inventory_id = 1489
    """
    queries.append(flying_hook)
    flying_hook_results = exec_query(flying_hook)
    final_results.append(flying_hook_results)
    # How often did they rent Flying Hook?
    questions.append("How often did they rent Flying Hook?")
    count_flying_hook = """
    SELECT CONCAT (c.first_name, ' ', c.last_name) as full_name, COUNT(*)
    FROM customer as c
    FULL OUTER JOIN rental as r USING (customer_id)
    WHERE
        r.inventory_id = 1489
    GROUP BY
        full_name
    """
    queries.append(count_flying_hook)
    count_flying_hook_results = exec_query(count_flying_hook)
    final_results.append(count_flying_hook_results)
    # The same thing but with the WHERE clause as a subquery to find the most popular rental ID
    questions.append("The same thing but with the WHERE clause as a subquery to find the most popular rental ID")
    count_flying_hook_combo = """
    SELECT CONCAT (c.first_name, ' ', c.last_name) as full_name, COUNT(*)
    FROM customer as c
    FULL OUTER JOIN rental as r USING (customer_id)
    WHERE
        r.inventory_id = (
            SELECT r.inventory_id
            FROM rental as r
            GROUP BY
                r.inventory_id
            ORDER BY
                count(*) DESC
            LIMIT 1
        )
    GROUP BY
        full_name
    """
    queries.append(count_flying_hook_combo)
    count_flying_hook_combo_results = exec_query(count_flying_hook_combo)
    final_results.append(count_flying_hook_combo_results)

    # What title is associated with the most rentals?
    questions.append("What title is associated with the most rentals?")
    top_rental = """
    SELECT film.title, COUNT(*)
    FROM rental
    LEFT JOIN inventory USING (inventory_id)
    LEFT JOIN film USING (film_id)
    GROUP BY
        film.film_id
    ORDER BY
        COUNT(*) DESC
    LIMIT 1
    """
    queries.append(top_rental)
    top_rental_results = exec_query(top_rental)
    final_results.append(top_rental_results)
    # What are top 5 titles associated with the most rentals?
    questions.append("What are top 5 titles associated with the most rentals?")
    top_rentals = """
    SELECT film.title, COUNT(*)
    FROM rental
    LEFT JOIN inventory USING (inventory_id)
    LEFT JOIN film USING (film_id)
    GROUP BY
        film.film_id
    ORDER BY
        COUNT(*) DESC
    LIMIT 5
    """
    queries.append(top_rentals)
    top_rentals_results = exec_query(top_rentals)
    final_results.append(top_rentals_results)


    name_of_file = "exploration.txt"
    complete_name = os.path.join(text_path, name_of_file)
    f = open(complete_name, "w")
    f.write("Film Table Questions\n")
    f.write(f"There are {unique_titles_results[0][0]} unique film titles in the film table\n")
    f.write(f"The title of the most common inventory ID in the rental table (inv ID = 1489) is {title_i1489_results[0][0]}\n")
    f.write(f"  The same things as above but a single query to get it without knowing the inv ID: {combo_fh_results[0][0]}\n")
    f.write(f"The customers who rented Flying Hook are named: {flying_hook_results}\n")
    f.write(f"  Here are the customers who rented Flying Hook and how many times they rented it: {count_flying_hook_results}\n")
    f.write(f"      The same thing with a sub-query instead of a hard coded value: {count_flying_hook_combo_results}\n")
    f.write(f"The film with the most rentals is titled: {top_rental_results[0][0]}. It has {top_rental_results[0][1]} rentals\n")
    f.write(f"  The top 5 films with the most rentals are titled: {[film[0] for film in top_rentals_results]}. They have {[film[1] for film in top_rentals_results]} rentals\n")

    f.write("\n")
    f.close()

    write_questions_queries_results(questions,queries,final_results,filename="Film Questions")

    return