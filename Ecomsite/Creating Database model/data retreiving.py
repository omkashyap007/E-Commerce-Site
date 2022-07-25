import pymysql as psql
import os
connection = psql.connect(
    user = "root" , 
    password = os.environ.get("MYSQL_PASSWORD") , 
    database = "college" ,    
)
cursor = connection.cursor()
cursor.execute("select * from student") ;
data_text_file = open("Creating Database model/text_data.txt" , "w")

for row in cursor :
    temp_string = ""
    for data in row :
        temp_string+= "{} ".format(str(data)) 
    data_text_file.write(temp_string+"\n")
data_text_file.close()