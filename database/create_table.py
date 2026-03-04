import psycopg

try:
    # Connect to PostgreSQL
    connection = psycopg.connect(
        dbname="postgres", 
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    cursor = connection.cursor()

    # Create table
    create_table_query = '''
    CREATE TABLE lung_cancer (
    id SERIAL PRIMARY KEY,
    gender VARCHAR(10),
    age INT,
    smoking BOOLEAN,
    yellow_fingers BOOLEAN,
    anxiety BOOLEAN,
    peer_pressure BOOLEAN,
    chronic_disease BOOLEAN,
    fatigue BOOLEAN,
    allergy BOOLEAN,
    wheezing BOOLEAN,
    alcohol_consuming BOOLEAN,
    coughing BOOLEAN,
    shortness_of_breath BOOLEAN,
    swallowing_difficulty BOOLEAN,
    chest_pain BOOLEAN,
    lung_cancer BOOLEAN
);
    '''
    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully.")

except (Exception, psycopg.DatabaseError) as error:
    print("Error:", error)

finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed.")