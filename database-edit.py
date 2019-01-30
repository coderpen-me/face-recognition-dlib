import sqlite3

value = int(input("Enter Your Choice : \n 1) Enter A New Person \n 2) Compile Whole Directory \n 3) Exit"))

cursor = cursor.execute("SELECT name, id, start, end from FACE_DATA")

if( vaule == 1):
   cursor = sqlite3.connect('database.db')
   cursor = cursor.execute("SELECT name,id from FACE_DATA")

   for row in cursor:
      if(row[1] == s) :
         print("Name of Person : ", row[0])
         imagePaths = list(paths.list_files('dataset/'+str(row[1])))
   print ("Operation done successfully")
   cursor.close()