import psycopg2
from config import config, text_path
import os.path
from questions.questions_helper import write_questions_queries_results
import plotly
import pandas as pd

# Reference for embedding plotly figures into Markdown: http://www.kellieottoboni.com/posts/2017/08/plotly-markup/

def report():
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
    # questions = []
    # queries = []
    # final_results = []

    # Which films are most costly to replace and why?
    costly_films = """
    SELECT *
    FROM film
    """
    costly_df = pd.read_sql_query(costly_films, conn)
    costly_df.to_csv(path_or_buf=r"C:\Users\Chris\Desktop\Career\ComplexPGSQL\sample_complex\report_CSVs\costly_df.csv")
    

    # Over time, how popular are the different ratings and categories of films?
    popular_films = """
    SELECT film.title, category.name, film.rating, film.rental_duration, film.rental_rate, film.length, film.replacement_cost, film.special_features, rental.rental_date
    FROM rental
        LEFT JOIN inventory USING (inventory_id)
        LEFT JOIN film USING (film_id)
        LEFT JOIN film_category USING (film_id)
        LEFT JOIN category USING (category_id)
    """
    popular_df = pd.read_sql_query(popular_films, conn)
    popular_df.to_csv(path_or_buf=r"C:\Users\Chris\Desktop\Career\ComplexPGSQL\sample_complex\report_CSVs\popular_df.csv")
    # How many films in inventory are in each category/rating?
    inventory = """
    SELECT i.inventory_id, f.title, f.rating, c.name as category
    FROM inventory as i
        LEFT JOIN film as f USING(film_id)
        LEFT JOIN film_category USING(film_id)
        LEFT JOIN category as c USING(category_id)
    """
    inventory_df = pd.read_sql_query(inventory, conn)
    inventory_df.to_csv(path_or_buf=r"C:\Users\Chris\Desktop\Career\ComplexPGSQL\sample_complex\report_CSVs\inventory_df.csv")


    # Over time, how do the performances of the different stores compare?
    stores = """
    SELECT rental.rental_id, rental.rental_date, customer.store_id, city.city, address.district
    FROM rental
        LEFT JOIN customer USING(customer_id)
        LEFT JOIN address USING(address_id)
        LEFT JOIN city USING(city_id)
    """
    stores_df = pd.read_sql_query(stores, conn)
    stores_df.to_csv(path_or_buf=r"C:\Users\Chris\Desktop\Career\ComplexPGSQL\sample_complex\report_CSVs\stores_df.csv")

    stores_inventory = """
    SELECT inventory.inventory_id, customer.store_id, city.city, address.district
    FROM inventory
        LEFT JOIN rental USING(inventory_id)
        LEFT JOIN customer USING(customer_id)
        LEFT JOIN address USING(address_id)
        LEFT JOIN city USING(city_id)
    """
    stores_inventory_df = pd.read_sql_query(stores_inventory, conn)
    stores_inventory_df.to_csv(path_or_buf=r"C:\Users\Chris\Desktop\Career\ComplexPGSQL\sample_complex\report_CSVs\stores_inventory_df.csv")


    # What is the current total outstanding balance of all of our customers?
    
    # There are customers w/ unique IDs 1-599
    ## We can use the built-in get_customer_balance(customer_id, timestamp without time zone) function for each customer to get each customer's balance

    # We first need to get the timestamp of the most recent payment in the payment table
    date_query = """
    SELECT p.payment_date
    FROM payment as p
    ORDER BY p.payment_date DESC
    LIMIT 1
    """
    payment_date = exec_query(date_query)[0][0]
    # print(payment_date.strftime("%m/%d/%Y, %H:%M:%S"))

    cust_balances = {}
    for i in range(1,600):
        # bal_query = f"""
        # SELECT get_customer_balance({i}, ((SELECT p.payment_date FROM payment as p WHERE p.customer_id = {i} ORDER BY p.payment_date DESC LIMIT 1)))
        # """
        bal_query = f"""
        SELECT get_customer_balance({i}, '{payment_date.strftime("%m/%d/%Y, %H:%M:%S")}'::timestamp without time zone)
        """
        # SELECT get_customer_balance(1::integer, (SELECT p.payment_date::timestamp without time zone FROM payment as p WHERE p.customer_id = 1 ORDER BY p.payment_date DESC LIMIT 1))
        # print(exec_query(bal_query)) # Check that the query is only returning the final calculation: it is
        cust_balances[i] = exec_query(bal_query)[0][0]
        # This is calculated as of the last time a customer MADE A PAYMENT, should probably calculate it on the last day that the payment table was updated overall
        ## FIXED and it didn't change anything ¯\_(ツ)_/¯
    
    balances_df = pd.DataFrame.from_dict(cust_balances, orient='index', columns=['Balance'])
    balances_df.reset_index(inplace=True)
    balances_df['Customer_ID'] = balances_df['index']
    balances_df.drop('index', axis=1, inplace=True)
    balances_df.to_csv(path_or_buf=r"C:\Users\Chris\Desktop\Career\ComplexPGSQL\sample_complex\report_CSVs\balances_df.csv")
    return


# The SQL for the function that returns a customer's balance
## The part I had to fix is the querying of v_overfees
### It originally used a COALESCE(SUM(IF())) statement that broke on the IF statement

# -- FUNCTION: public.get_customer_balance(integer, timestamp without time zone)

# -- DROP FUNCTION public.get_customer_balance(integer, timestamp without time zone);

# CREATE OR REPLACE FUNCTION public.get_customer_balance(
# 	p_customer_id integer,
# 	p_effective_date timestamp without time zone)
#     RETURNS numeric
#     LANGUAGE 'plpgsql'

#     COST 100
#     VOLATILE 
# AS $BODY$
#        --#OK, WE NEED TO CALCULATE THE CURRENT BALANCE GIVEN A CUSTOMER_ID AND A DATE
#        --#THAT WE WANT THE BALANCE TO BE EFFECTIVE FOR. THE BALANCE IS:
#        --#   1) RENTAL FEES FOR ALL PREVIOUS RENTALS
#        --#   2) ONE DOLLAR FOR EVERY DAY THE PREVIOUS RENTALS ARE OVERDUE
#        --#   3) IF A FILM IS MORE THAN RENTAL_DURATION * 2 OVERDUE, CHARGE THE REPLACEMENT_COST
#        --#   4) SUBTRACT ALL PAYMENTS MADE BEFORE THE DATE SPECIFIED
# DECLARE
#     v_rentfees DECIMAL(5,2); --#FEES PAID TO RENT THE VIDEOS INITIALLY
#     v_overfees INTEGER;      --#LATE FEES FOR PRIOR RENTALS
#     v_payments DECIMAL(5,2); --#SUM OF PAYMENTS MADE PREVIOUSLY
# BEGIN
#     SELECT COALESCE(SUM(film.rental_rate),0) INTO v_rentfees
#     FROM film, inventory, rental
#     WHERE film.film_id = inventory.film_id
#       AND inventory.inventory_id = rental.inventory_id
#       AND rental.rental_date <= p_effective_date
#       AND rental.customer_id = p_customer_id;

#     SELECT SUM(
# 		CASE
# 			WHEN ((rental.return_date - rental.rental_date) > (film.rental_duration * '1 day'::interval))
# 				AND ((rental.return_date - rental.rental_date) > ((film.rental_duration * '1 day'::interval)*2)) THEN (EXTRACT(epoch FROM (((rental.return_date - rental.rental_date) - (film.rental_duration * '1 day'::interval))))::integer/86400 + film.replacement_cost)
# 			WHEN ((rental.return_date - rental.rental_date) > (film.rental_duration * '1 day'::interval)) THEN (EXTRACT(epoch FROM ((rental.return_date - rental.rental_date) - (film.rental_duration * '1 day'::interval))))::integer/86400
# 				ELSE 0
# 		END) INTO v_overfees
# 	FROM rental, inventory, film
#     WHERE film.film_id = inventory.film_id
#       AND inventory.inventory_id = rental.inventory_id
#       AND rental.rental_date <= p_effective_date
#       AND rental.customer_id = p_customer_id;

#     SELECT COALESCE(SUM(payment.amount),0) INTO v_payments
#     FROM payment
#     WHERE payment.payment_date <= p_effective_date
#     AND payment.customer_id = p_customer_id;

#     RETURN v_payments - v_rentfees - v_overfees;
# END
# $BODY$;

# ALTER FUNCTION public.get_customer_balance(integer, timestamp without time zone)
#     OWNER TO postgres;
