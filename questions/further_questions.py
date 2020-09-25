import psycopg2
from config import config, text_path
import os.path

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

    # What are the cities of each customer?
    cust_city = """
    SELECT CONCAT (cust.first_name, ' ', cust.last_name) as full_name, city.city
    FROM customer as cust
    LEFT JOIN address USING (address_id)
    LEFT JOIN city USING (city_id)
    LIMIT 5
    """
    cust_city_results = exec_query(cust_city)

    # What are the top 5 customers with the most rentals, and how many rentals are there?
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
    city_rentals_results = exec_query(city_rentals)


    name_of_file = "exploration.txt"
    complete_name = os.path.join(text_path, name_of_file)
    f = open(complete_name, "a")
    f.write(f"\nFurther Questions\n")
    f.write(f"The names and cities of 5 customers are: {cust_city_results}\n")
    f.write(f"Here are the 5 customers with the most rentals and their number of rentals: {city_rentals_results}\n")
    f.write(f"\n")

    f.close()
    return