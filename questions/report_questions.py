from config import config, text_path
import os.path
from questions.questions_helper import write_questions_queries_results
import plotly

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
    questions = []
    queries = []
    final_results = []

    # Which films are most costly to replace and why?
    questions.append("Which films are most costly to replace and why?")
    

    # Which are the films with the highest rental rate and is rental rate related to their characteristics at all?
    questions.append("Which are the films with the highest rental rate and is rental rate related to their characteristics at all?")


    # Over time, how popular are the different ratings and categories of films?
    questions.append("Over time, how popular are the different ratings and categories of films?")


    # Over time, how has the performance of our stores changed? If there is change, is it related to location?
    questions.append("Over time, how has the performance of our stores changed? If there is change, is it related to location?")


    # What is the current total outstanding balance of all of our customers?
    questions.append("What is the current total outstanding balance of all of our customers?")


    name_of_file = "report.txt"
    complete_name = os.path.join(text_path, name_of_file)
    f = open(complete_name, "w")
    f.write(f"\Report Questions\n")
    for i in range(len(questions)):
        f.write(f"\n    Question: {questions[i]}\n")
        f.write(f"  {queries[i]}\n")
        f.write(f"      {final_results[i]}\n")
    f.write(f"\n")

    f.close()

    write_questions_queries_results(questions,queries,final_results,filename="Report Questions")

    return