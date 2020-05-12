import pandas as pd
import queries_source

# Candidate info functions

def extract_data_candidate(tables):
    '''
    Extracts neede BQ table from candidate email events and characteristics
    The tables in this function are fixed.
    @ tables: list of tables to be extracted
    '''
    print('Extracting data from BQ...')

    try:
        for table in tables:
            print("Collecting {} data.".format(table))
            query_name = 'query_' + table
            globals()[table] = pd.read_gbq(
                getattr(queries_source, query_name),
                project_id='merlin-pro',
                dialect="standard")

        return sendgrid_events, sent_events, clicked_events

    except:
        print('Error extracting BQ data!')
