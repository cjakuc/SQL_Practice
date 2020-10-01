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

    # What are the most common ratings and most common categories of the films rented by the 5 most active customers?
    questions.append("What are the most common ratings and most common categories of the films rented by the 5 most active customers?")
    # To get the categories, we have to make our own aggregate function
    ## I did this directly in the database, with pgAdmin 4, using these two queries:
    # """
    # CREATE OR REPLACE FUNCTION _final_mode(anyarray)
    # RETURNS anyelement AS
    # $BODY$
    #     SELECT a
    #     FROM unnest($1) a
    #     GROUP BY 1 ORDER BY COUNT(1) DESC
    #     LIMIT 1;
    # $BODY$
    # LANGUAGE 'sql' IMMUTABLE;
    # """
    # """
    # CREATE AGGREGATE mode_value(anyelement) (
    # SFUNC=array_append,
    # STYPE=anyarray,
    # FINALFUNC=_final_mode,
    # INITCOND='{}'
    # );
    # """

    most_active = """
    SELECT CONCAT (customer.first_name, ' ', customer.last_name), mode_value(film.rating), mode_value(category.name), COUNT(rental.rental_id)
    FROM rental
    LEFT JOIN customer USING (customer_id)
    LEFT JOIN inventory USING (inventory_id)
    LEFT JOIN film USING (film_id)
    LEFT JOIN film_category USING (film_id)
    LEFT JOIN category USING (category_id)
    WHERE customer.customer_id IN (
        SELECT customer.customer_id
        FROM rental
        LEFT JOIN customer USING (customer_id)
        INNER JOIN inventory USING (inventory_id)
        INNER JOIN film USING (film_id)
        GROUP BY
            customer.customer_id
        ORDER BY
            COUNT(*) DESC
        LIMIT 5
    )
    GROUP BY
        customer.customer_id
    ORDER BY
        COUNT(rental.rental_id) DESC
    """

    queries.append(most_active)
    most_active_results = exec_query(most_active)
    final_results.append(most_active_results)
    # Who are the top actors in the films rented by the 5 most active customers? (Actor name, Customer name)
    questions.append("Who are the top actors in the films rented by the 5 most active customers? (Actor name, Customer name)")
    actors = """
    SELECT mode_value(CONCAT(actor.first_name, ' ', actor.last_name)), CONCAT (customer.first_name, ' ', customer.last_name)
    FROM rental
        LEFT JOIN customer USING (customer_id)
        LEFT JOIN inventory USING (inventory_id)
        LEFT JOIN film USING (film_id)
        LEFT JOIN film_actor USING (film_id)
        LEFT JOIN actor USING (actor_id)
    WHERE customer.customer_id IN (
        SELECT customer.customer_id
        FROM rental
            LEFT JOIN customer USING (customer_id)
            INNER JOIN inventory USING (inventory_id)
            INNER JOIN film USING (film_id)
        GROUP BY
            customer.customer_id
        ORDER BY
            COUNT(*) DESC
        LIMIT 5
    )
    GROUP BY
        customer.customer_id
    ORDER BY
        COUNT(rental.rental_id) DESC
    """
    queries.append(actors)
    actors_results = exec_query(actors)
    final_results.append(actors_results)
    # There's something wrong with the last 2 queries. The order is slightly different on the top 4th and 5th most active customers.
    ## Potential cause:
    ### 1 rental can = multiple films / inventory_ids
    ### Not sure if I'm accounting for this correctly -> should I be starting in inventory?

    # What are the average lengths of films rented in the 5 cities with the most rentals?
    questions.append("What are the average lengths of films rented in the 5 cities with the most rentals?")
    city_length = """
    SELECT city.city, AVG(film.length), COUNT(city.city)
    FROM inventory
        LEFT JOIN film USING (film_id)
        LEFT JOIN rental USING (inventory_id)
        LEFT JOIN customer USING (customer_id)
        LEFT JOIN address USING (address_id)
        LEFT JOIN city USING (city_id)
    GROUP BY
        city.city_id
    ORDER BY
        COUNT(city.city) DESC
    LIMIT 5
    """
    queries.append(city_length)
    city_length_results = exec_query(city_length)
    final_results.append(city_length_results)

    name_of_file = "results.txt"
    complete_name = os.path.join(text_path, name_of_file)
    f = open(complete_name, "w")
    f.write(f"\nFinal Questions\n")
    for i in range(len(questions)):
        f.write(f"\n    Question: {questions[i]}\n")
        f.write(f"  {queries[i]}\n")
        f.write(f"      {final_results[i]}\n")
    f.close()

    write_questions_queries_results(questions,queries,final_results,filename="Final Questions")

    return