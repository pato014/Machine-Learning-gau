import json

urls = []
with open('urls') as file:
    data = file.readlines()
    for i in data:
        i.replace("\n","")
        urls.append(i)

with open("mercedes.json", 'w') as outfile:
    outfile.write(json.dumps(urls))