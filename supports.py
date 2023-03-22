from re import fullmatch,compile

# --== Constants ==--

SET_VALUES = {
	'false': False,
	'true': True,
	'null': None
}
VALID_WHITESPACE = [' ',' ',' ',' ']
VALID_CHARS = '[]{}":,trufasnl+-e.0123456789'
POSSIBLE_MISSED = [
    ',:',
	':,',
    ',,',
    '[]',
    '[,',
    ',]',
    ':}',
    '{:'
]
NUMBER_REGEX = compile(r"-?[0-9]+(\.[0-9]+)?((e|E)(\+|-)?[0-9]+)?")

# --== Functions ==--

def clean_whitespace(data):
	toremove = []
	in_string = False
	# Clean up whitespace
	for i in range(0, len(data)):
		if data[i] == '"' and data[i-1] != '\\':
			in_string = not in_string
		
		if not (data[i] in VALID_CHARS) and not in_string:
			toremove.append(i)

	clean_data = list(data)
	for i in reversed(toremove): del clean_data[i]
	clean_data = ''.join(clean_data)
	return clean_data

def get_closing_index(data, start_index):
	open_type = data[start_index]
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
		elif data[i] == '"' and data[i-1 if i > 0 else i] != '\\':
			in_string = not in_string

		if bracket_count == 0:
			return i
		
def get_all_markers(data):
    new_markers = "[]{}\",:"
    in_string = False
    found_markers = []

    for i in range(0, len(data)):
        key = data[i]
        if key == '"' and data[i-1 if i > 0 else i] != '\\':
            in_string = not in_string
            found_markers.append((key,i))
        if key in new_markers and not in_string and key != '"':
            found_markers.append((key,i))
	    
    mc = {
        '{':0,
        '[':0,
        '"':0
    }

    for i in found_markers:
        if i[0] == '{' or i[0] == '}':
            mc['{'] += 1
        elif i[0] == '[' or i[0] == ']':
            mc['['] += 1
        elif i[0] == '"':
            mc['"'] += 1

    if mc['{'] % 2 != 0 or mc['['] % 2 != 0 or mc['"'] % 2 != 0:
        raise JSONError("Invalid JSON: Unmatched brackets or quotes")

    return found_markers

def value_validator(value):
    if value in SET_VALUES:
        return Token(value,value=SET_VALUES[value])
    elif fullmatch(NUMBER_REGEX, value):
        return Token('number',value=float(value))
    return False

# --== Classes ==--

class Token:
    def __init__(self, token_type, value=None):
        self.type = token_type
        self.value = value
    
class JSONError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)