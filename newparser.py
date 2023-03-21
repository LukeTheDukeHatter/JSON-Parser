# Constant Values

SET_VALUES = ['false','true','null']
VALID_WHITESPACE = [' ',' ',' ',' ']
NUMBER_REGEX = r"-?[0-9]+(\.[0-9]+)?((e|E)(\+|-)?[0-9]+)?"

# Parsing Functions

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



def parse_object(data_big):
	data = data_big[1:-1]
	stack = []
	c_obj = {}
	c_val = None
	c_key = None
	c_key_waiting = False
	c_InString = False
	c_temp = None
	
	i = 0
	
	while (i < len(data)):
		if data[i] == '"':
			if c_InString:
				if c_key_waiting and isinstance(c_obj,dict):
					c_obj[c_key] = c_val

					c_key = None
					c_key_waiting = False
					c_val = None
				elif isinstance(c_obj,list):
					c_obj.append(c_val)
					
					c_val = None
			c_InString = not c_InString
		elif data[i] == ':':
			if not c_InString:
				c_key = c_val
				c_key_waiting = True
				c_val = None
		elif data[i] == ',':
			if not c_InString:
				if c_val != None:
					c_obj.append(c_val)
					c_val = None
		elif data[i] == '{':
			if not c_InString:
				temp_closing_index = get_closer_index(data,i,'{')
				c_val = parse_object(data[i:temp_closing_index+1])
				i = temp_closing_index
		elif data[i] == '[':
			if not c_InString:
				stack.append(c_obj)
				c_obj = []
		elif data[i] == ']':
			if not c_InString:
				c_val = c_obj
				c_obj = stack.pop()
				if isinstance(c_obj,dict):
					if c_key_waiting:
						c_obj[c_key] = c_val

						c_key = None
						c_val = None
						c_key_waiting = False
					else:
						raise Exception('JSON Syntax Error')
				elif isinstance(c_obj,list):
					c_obj.append(c_val)
					c_val = None
		elif data[i] == '}':
			if not c_InString:
				break
		else:
			if c_InString:
				# += NoneType and str
				c_val += data[i]
			else:
				raise Exception('JSON Syntax Error')
		
		i += 1
		
	return c_obj







def parse_json(data):
    clean_data = clean_whitespace(data)
    found_markers, marker_pairs = get_all_markers(clean_data)
    marker_list = list(''.join([i[0] for i in found_markers]).replace('""','#'))

    string_literals = [clean_data[marker_pair[0]+1:marker_pair[1]] for marker_pair in marker_pairs['"']]
    found_markers = [i for i in found_markers if i[0] != '"']

    # for i in string_literals: marker_list[marker_list.index('#')] = i

    # print(f"found_markers: {found_markers}")
    # print(f"marker_list: {marker_list}")
    # print(f"string_literals: {string_literals}")


    
    result = parse_object(clean_data)

    return result




valid_json = """ { "a": ["b", "c","  d e",{"a":"b"}]  , " b ":"c"} """

print(parse_json(valid_json))