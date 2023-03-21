from supports import *

def parse_object(data_big,r=False):
	list_data_big = list(data_big)
	if r == False:
		
		all_markers = get_all_markers(list_data_big)
		missed_values = []

		for m_index in range(0,len(all_markers)-1):
			if all_markers[m_index][0]+all_markers[m_index+1][0] in POSSIBLE_MISSED:
				start_index = all_markers[m_index][1]
				end_index = all_markers[m_index+1][1]

				missed = value_validator(data_big[start_index+1:end_index])

				missed_values.append({'start':start_index,'end':end_index,'value':missed})

		for missed_item in missed_values[::-1]:
			if missed_item['value']:
				for _ in range(1,len(data_big[missed_item['start']+1:missed_item['end']])):
					del list_data_big[missed_item['start']+1]
				list_data_big[missed_item['start']+1] = missed_item['value']

	data = list_data_big[1:-1]
	
	# Turns the data back into an actual dictionary
	stack = []
	c_obj = {} if data_big[0] == '{' else [] 
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
				c_val = parse_object(data[i:temp_closing_index+1],r=True)
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
						raise Exception('Invalid JSON: Syntax Error')
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
				if isinstance(data[i], Token):
					c_val = data[i].value
					if c_key_waiting and isinstance(c_obj,dict):
						c_obj[c_key] = c_val

						c_key = None
						c_key_waiting = False
						c_val = None
					elif isinstance(c_obj,list):
						c_obj.append(c_val)
						
						c_val = None
				else:
					raise Exception('Invalid JSON: Syntax Error')
		i += 1
	return c_obj


def parse(data):
	clean_data = clean_whitespace(data)
	result = parse_object(clean_data)
	return result
