import json


#заменяем символ для распознавания списка
#group_info_test.json
with open('C:\projects\ProjectInsta\ProjectInsta_TR\src\database\group_info.json') as js_file:
    mylist= js_file.read().replace('][',',')
    data=json.loads(mylist)

#читаемый текст в командную строку
#for element in data:
#    for key, value in element.items():
#        print("{}: {}".format(key, value))
   


#записываем изменение в файл
#fmt_group_info_test.json'
with open('fmt_group_info.json', 'w') as f:
    json.dump(data, f)


#проверяю типы данных, записанных в файл, количество записей и ключи
#fmt_group_info_test.json'
with open('fmt_group_info.json') as file:
    check=json.load(file)
    print(type(check))
    print(len(check))
    print(type(check[1]))
    print(check[1].keys())
    
