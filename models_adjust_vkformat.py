import json
import pprint


string_to_be_replaced=']['
string_to=','

json_data = open('group_info_test.json').read()
json_str=json.dumps(json_data)
line=str(json_str)
print(type(line))


changed_data=line.replace(string_to_be_replaced,string_to)
updated_data=changed_data
pprint.pprint(updated_data)

print(type(updated_data))

#не получается записать изменение в файл, на выходе абракадабра
with open ('new_group_info_test.json','w') as file:
    file.write(json.dumps(updated_data,ensure_ascii = False, indent=0))


