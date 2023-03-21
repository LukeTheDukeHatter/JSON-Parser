# Rules:
# https://www.ietf.org/rfc/rfc4627.txt


# Constants for the JSON parser

SET_VALUES = ['false','true','null']
VALID_WHITESPACE = [' ',' ',' ',' ']

# Get index of closing bracket

def clean_whitespace(data):
    toremove = []
    in_string = False
    # Clean up whitespace
    for i in range(0, len(data)):
        if data[i] == '"' and data[i-1] != '\\':
            in_string = not in_string
        
        if (data[i] in VALID_WHITESPACE) and not in_string:
            toremove.append(i)

    clean_data = list(data)
    for i in reversed(toremove): del clean_data[i]
    clean_data = ''.join(clean_data)
    return clean_data


def get_closer_index(data, start_index, open_type):
    opposite = {
        '[': ']',
        '{': '}',
        '"': '"'
    }
    in_string = False
    bracket_count = 0
    for i in range(start_index, len(data)):
        if data[i] == open_type and not in_string:
            bracket_count += 1
        elif data[i] == opposite[open_type] and not in_string:
            bracket_count -= 1
        elif data[i] == '"' and data[i-1] != '\\':
            in_string = not in_string

        if bracket_count == 0:
            return i

def get_all_markers(data):
    new_markers = "[]{}\",:"
    in_string = False

    found_markers = []
    stack = {
        '{':[],
        '[':[],
        '"':[]
    }
    marker_pairs = {
        '{':[],
        '[':[],
        '"':[]
    }

    for i in range(0, len(data)):
        key = data[i]
        if key == '"' and data[i-1] != '\\':
            in_string = not in_string

            found_markers.append((key,i))
            stack[key].append(i)

        if key in new_markers and not in_string and key != '"':

            found_markers.append((key,i))

            if key in stack.keys():
                stack[key].append(i)

    for i in stack['{']: marker_pairs['{'].append((i,get_closer_index(data, i, '{')))
    for i in stack['[']: marker_pairs['['].append((i,get_closer_index(data, i, '[')))
    for i in range(0,len(stack['"']),2): marker_pairs['"'].append((stack['"'][i], stack['"'][i+1])) 

    return (found_markers, marker_pairs)

def parse_object(marker_list, string_literals):
    obj = {}
    while True:
        # Consume opening brace or comma
        if marker_list[0] == '{':
            marker_list.pop(0)
        elif marker_list[0] == ',':
            marker_list.pop(0)

        # Consume key
        key_idx = marker_list.index(':')
        key_literal_idx = marker_list[key_idx+1]
        key = string_literals[key_literal_idx]
        marker_list = marker_list[key_idx+2:]

        # Consume value
        value = parse_value(marker_list, string_literals)

        # Assign key-value pair to object
        obj[key] = value

        # Consume closing brace or comma
        if marker_list[0] == '}':
            marker_list.pop(0)
            break
        elif marker_list[0] == ',':
            marker_list.pop(0)

    return obj

# Helper function to parse a JSON array
def parse_array(marker_list, string_literals):
    arr = []
    while True:
        # Consume opening bracket or comma
        if marker_list[0] == '[':
            marker_list.pop(0)
        elif marker_list[0] == ',':
            marker_list.pop(0)

        # Consume value
        value = parse_value(marker_list, string_literals)
        arr.append(value)

        # Consume closing bracket or comma
        if marker_list[0] == ']':
            marker_list.pop(0)
            break
        elif marker_list[0] == ',':
            marker_list.pop(0)

    return arr

# Helper function to parse a JSON value
def parse_value(marker_list, string_literals):
    if marker_list[0] == '{':
        return parse_object(marker_list, string_literals)
    elif marker_list[0] == '[':
        return parse_array(marker_list, string_literals)
    else:
        value = string_literals[marker_list[1]]
        marker_list = marker_list[2:]
        return value


def parse_json(data):
    clean_data = clean_whitespace(data)
    found_markers, marker_pairs = get_all_markers(clean_data)
    marker_list = list(''.join([i[0] for i in found_markers]).replace('""','#'))

    string_literals = [clean_data[marker_pair[0]+1:marker_pair[1]] for marker_pair in marker_pairs['"']]


    result = {}
    c_key = None
    current_item = None

    print(string_literals)

    result = parse_value(marker_list, string_literals)

    return result






valid_json = """ { "a": ["b", "c","  d e"]  , " b ":"c"} """

# print(get_all_markers(clean_whitespace(valid_json))[1])
print(parse_json(valid_json))