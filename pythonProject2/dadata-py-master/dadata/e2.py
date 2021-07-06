import json

#with open('file.txt', 'r') as file:
#    data = file.read()
#    info = json.loads(data)
#print(info)


f = open('file.json', 'r')
red = f.read()
info = json.load(f)
print(info)