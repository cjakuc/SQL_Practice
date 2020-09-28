import psycopg2
from config import config, text_path
import os.path
from questions.questions_helper import write_questions_queries_results

def further():
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

    # What are the cities of each customer?
    questions.append("What are the cities of each customer?")
    cust_city = """
    SELECT CONCAT (cust.first_name, ' ', cust.last_name) as full_name, city.city
    FROM customer as cust
    LEFT JOIN address USING (address_id)
    LEFT JOIN city USING (city_id)
    LIMIT 5
    """
    queries.append(cust_city)
    cust_city_results = exec_query(cust_city)
    final_results.append(cust_city_results)

    # What are the top 5 customers with the most rentals, and how many rentals are there?
    questions.append("What are the top 5 customers with the most rentals, and how many rentals are there?")
    city_rentals = """
    SELECT CONCAT (c.first_name, ' ', c.last_name) as full_name, COUNT(r.rental_id)
    FROM rental as r
    LEFT JOIN customer as c USING (customer_id)
    GROUP BY
        full_name
    ORDER BY
        COUNT(r.rental_id) DESC
    LIMIT 5
    """
    queries.append(city_rentals)
    city_rentals_results = exec_query(city_rentals)
    final_results.append(city_rentals_results)
    # What are all the movies that the person with the most rentals rented?
    questions.append("What are all the movies that the person with the most rentals rented?")
    most_rentals = """
    SELECT f.title
    FROM film as f
    RIGHT JOIN inventory USING (film_id)
    LEFT JOIN rental USING (inventory_id)
    LEFT JOIN customer USING (customer_id)
    WHERE
        rental.customer_id = (
            SELECT c.customer_id
            FROM rental as r
            LEFT JOIN customer as c USING (customer_id)
            GROUP BY
                c.customer_id
            ORDER BY
                COUNT(r.rental_id) DESC
            LIMIT 1
        );
    """
    queries.append(most_rentals)
    most_rentals_results = exec_query(most_rentals)
    final_results.append(most_rentals_results)


    name_of_file = "exploration.txt"
    complete_name = os.path.join(text_path, name_of_file)
    f = open(complete_name, "a")
    f.write(f"\nFurther Questions\n")
    f.write(f"The names and cities of 5 customers are: {cust_city_results}\n")
    f.write(f"Here are the 5 customers with the most rentals and their number of rentals: {city_rentals_results}\n")
    f.write(f"The person with the most rentals rented these title: {[x[0] for x in most_rentals_results]}\n")
    f.write(f"\n")

    f.close()

    write_questions_queries_results(questions,queries,final_results,filename="Further Questions")

    return