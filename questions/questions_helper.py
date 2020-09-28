from config import text_path
import os.path

def write_questions_queries_results(questions: list, queries: list, results: list, filename: str):
    """Writes all the questions, queries, and results to everything.txt in a clean format

    Parameters
    ----------
    questions : list
        List of all the questions asked in a file as strings
    queries : list
        List of all the queries asked in a file as strings
    results : list
        List of all the results asked in a file as strings
    filename : string
        Name of the file verything else is coming from
    """
    if not (len(questions) == len(queries) == len(results)):
        print(f"Questions, queries, results list are not an equal size in the {filename} file: {len(questions)}, {len(queries)}, {len(results)}")
        return
    
    name_of_file = "everything.txt"
    complete_name = os.path.join(text_path, name_of_file)
    # Recreate everything.txt every time main.py is run
    if filename == "Film Questions":
        f = open(complete_name, "w")
    else:
        f = open(complete_name, "a")
    f.write(f"The following items come from the {filename} file\n")
    for i in range(len(questions)):
        f.write(f"\n    Question: {questions[i]}\n")
        f.write(f"  {queries[i]}\n")
        f.write(f"      {results[i]}\n")
    f.write(3*"\n")
    f.close()
    return