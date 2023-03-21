import jsonparser

if __name__ == '__main__':
    with open('input.json','r') as rf:
        data = rf.read()

    # data = '{"a":1,[false,,null]}'

    print(jsonparser.parse(data))