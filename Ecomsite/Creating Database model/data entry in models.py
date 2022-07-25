with open("Creating Database model/text_data.txt") as f :
    data = f.read()
    
new_data_list = []

data = data.split("\n")
new_data_list = []
for i in data :
    temp_list = i.split(" ")[:-1]
    new_data_list.append(temp_list)
data = new_data_list[:-1]

for i in data :
    student_info = StudentModel(
        first_name = i[1] , 
        last_name = i[2] ,
        age = i[3] ,
        branch = i[4] 
    )
    studnet_info.save()