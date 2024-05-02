import sqlite3, os
file_names = os.listdir("images/")
conn = sqlite3.connect('neodinbot.db')
cursor = conn.cursor()
"""for file in file_names:
    with open("images/"+file, "rb") as image_file:
        image_data = image_file.read()
    print(file)
    cursor.execute("INSERT INTO MEMES (NAME, IMAGE) VALUES (?, ?)", (file, image_data))
    conn.commit()"""
"""with open("photo_2023-06-30_20-34-15.jpg", "rb") as image_file:
    image_data = image_file.read()

cursor.execute("UPDATE MEMES SET IMAGE = ? WHERE ID = 1", (image_data,))
conn.commit()
conn.close()"""
"""
cursor.execute('''
                CREATE TABLE MEMES 
               (ID INTEGER PRIMARY KEY,
               NAME VARCHAR(255),
               IMAGE BLOB)
               ''')
"""
"""cursor.execute("INSERT INTO MEMES (NAME, IMAGE) VALUES (?, ?)", ("user_photo.jpg", image_data))
conn.commit()"""
cursor.execute("SELECT ID FROM MEMES", ())
id_list = [el[0] for el in cursor.fetchall()]
print(id_list)

conn.close()
