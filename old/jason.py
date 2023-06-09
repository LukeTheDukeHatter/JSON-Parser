from supports import *

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
		if data[i] == '"' and (data[i-1 if i > 0 else i] != '\\'):
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
				temp_closing_index = get_closing_index(data,i)
				c_val = parse_object(data[i:temp_closing_index+1])
				i = temp_closing_index
				if isinstance(c_obj,dict):
					if c_key_waiting:
						c_obj[c_key] = c_val

						c_key = None
						c_val = None
						c_key_waiting = False
				elif isinstance(c_obj,list):
					c_obj.append(c_val)
					c_val = None
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
				if c_val == None:
					c_val = ''
				c_val += data[i]
			else:
				raise Exception('JSON Syntax Error')
		
		i += 1
		
	return c_obj







def parse_json(data):
	clean_data = clean_whitespace(data)


	result = parse_object(clean_data)
	return result




valid_json = """ { "a": ["b", "c","  d e",{"a":"b"}]  , " b ":"c"} """
print(parse_json(valid_json))