import mysql.connector

def save_translation(original_text, translated_text, source_language, target_language, file_name):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='brokenpotato',  # replace with your actual password
            database='ocr_translation'
        )
        cursor = conn.cursor()

        query = """
            INSERT INTO translations (original_text, translated_text, source_language, target_language, file_name)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (original_text, translated_text, source_language, target_language, file_name)

        cursor.execute(query, values)
        conn.commit()

        print(f"Saved to database: {original_text[:30]}... ➝ {translated_text[:30]}...")

    except mysql.connector.Error as err:
        print("MySQL Error:", err)

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
