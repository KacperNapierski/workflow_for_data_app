import pandas as pd
import psycopg

def migrate_csv_to_postgres(csv_file_path):
    # Read CSV into DataFrame
    df = pd.read_csv(csv_file_path)

    # Clean column names (remove spaces, convert to lowercase)
    df.columns = [col.strip().replace(" ", "_").lower() for col in df.columns]

    # Convert boolean-like columns to actual boolean
    bool_columns = [
        "smoking", "yellow_fingers", "anxiety", "peer_pressure",
        "chronic_disease", "fatigue", "allergy", "wheezing",
        "alcohol_consuming", "coughing", "shortness_of_breath",
        "swallowing_difficulty", "chest_pain", "lung_cancer"
    ]
    for col in bool_columns:
        df[col] = df[col].astype(bool)

    # Connect to PostgreSQL
    connection = psycopg.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    
    cursor = connection.cursor()

    # Prepare the insert query
    insert_query = """
        INSERT INTO lung_cancer (
            gender, age, smoking, yellow_fingers, anxiety, peer_pressure,
            chronic_disease, fatigue, allergy, wheezing, alcohol_consuming,
            coughing, shortness_of_breath, swallowing_difficulty, chest_pain, lung_cancer
        )
        VALUES (
            %(gender)s, %(age)s, %(smoking)s, %(yellow_fingers)s, %(anxiety)s, %(peer_pressure)s,
            %(chronic_disease)s, %(fatigue)s, %(allergy)s, %(wheezing)s, %(alcohol_consuming)s,
            %(coughing)s, %(shortness_of_breath)s, %(swallowing_difficulty)s, %(chest_pain)s, %(lung_cancer)s
        )
    """

    # Insert each row into the table
    for _, row in df.iterrows():
        cursor.execute(insert_query, row.to_dict())

    # Commit changes and close connection
    connection.commit()
    cursor.close()
    connection.close()
    print("Data migration completed successfully!")

# Example usage
if __name__ == "__main__":
    csv_path = "/home/Weles/Documents/Code/workflow_for_data_app/database/survey lung cancer.csv"  # replace with your CSV path
    migrate_csv_to_postgres(csv_path)