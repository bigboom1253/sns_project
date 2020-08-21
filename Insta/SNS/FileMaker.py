import json

def write_file(obj, file_name, data):
    obj.file = open(file_name, 'w')
    obj.file.write('[\n' + json.dumps(data))
    obj.file.close()

def add_data(obj, file_name, data):
    obj.file = open(file_name, 'a')
    obj.file.write(',\n' + json.dumps(data))
    obj.file.close()

def close_file(obj):
    obj.file.write('\n]')
    obj.file.close()
