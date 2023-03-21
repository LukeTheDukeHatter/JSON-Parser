import jsonparser

if __name__ == '__main__':
    with open('input.json','r') as rf:
        data = rf.read()
        
    print(jsonparser.parse(data))