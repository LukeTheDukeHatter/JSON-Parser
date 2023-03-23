using System.Text.RegularExpressions;

Dictionary<string, object> SET_VALUES = new Dictionary<string, object>(){ {"false", false}, {"true", true}, {"null", null} };
char[] VALID_WHITESPACE = { ' ', ' ', ' ', ' ' };
string VALID_CHARS = "[]{}\":,trufasnl+-e.0123456789";
string[] POSSIBLE_MISSED = { ",:", ":,", ",,", "[]", "[,", ",]", ":}", "{:" };
Regex NUMBER_REGEX = new Regex(@"^-?[0-9]+(\.[0-9]+)?((e|E)(\+|-)?[0-9]+)?$");

string clean_whitespace(string data)
{
    int[] toremove = Array.Empty<int>();
    bool inString = false;

    for (int i = 0; i < data.Length; i++)
    {
        if (data[i] == '"' && data[i - 1] != '\\') { inString = !inString; }
        if (!VALID_CHARS.Contains(data[i]) && !inString) { toremove.Append(i); }
    }
    
    toremove.Reverse();
    
    List<char> clean_data = data.ToList();
    
    foreach (int x in toremove) { clean_data.RemoveAt(x); }
    
    string output = "";
    
    foreach (char c in clean_data) { output += c.ToString(); }

    return output;
}

int get_closing_index(string data,int start_index) {
    char open_type = data[start_index];
    Dictionary<char,char> opposite = new Dictionary<char,char>() {{'[',']'}, {'{','}'}, {'"','"'} };
    bool in_string = false;
    int bracket_count = 0;
    for (int i = start_index; i<data.Length; i++) {
        if (data[i] == open_type && !in_string) {
            bracket_count += 1;
        } else if (data[i] == opposite[open_type] && !in_string) {
            bracket_count -= 1;
        } else if (data[i] == '"' && data[i > 0 ? i-1 : i] != '\\') {
            in_string = !in_string;
        }

        if (bracket_count == 0) {
            return i;
        }
    }
    throw new JSONError("Invalid JSON: Unmatched brackets or quotes");
}

List<KeyValuePair<char,int>> get_all_markers(List<object> data) {
    string new_markers = "[]{}\",:";
    bool in_string = false;
    List<KeyValuePair<char,int>> found_markers = new List<KeyValuePair<char,int>>();

    for (int i = 0; i < data.Count; i++) {
        char key = (char)data[i];
        if (key == '"' && (char)data[i > 0 ? i-1 : i] != '\\') {
            in_string = !in_string;
            found_markers.Append(new KeyValuePair<char,int>(key, i));
        }
        if (new_markers.Contains(key) && !in_string && key != '"') {
            found_markers.Append(new KeyValuePair<char,int>(key, i));
        }
    }

    Dictionary<char,int> mc = new Dictionary<char,int>() { {'{', 0}, {'[', 0}, {'"', 0} };

    foreach (KeyValuePair<char,int> i in found_markers) {
        if (i.Key == '{' || i.Key == '}') {
            mc['{'] += 1;
        } else if (i.Key == '[' || i.Key == ']')
        {
            mc['['] += 1;
        } else if (i.Key == '"')
        {
            mc['"'] += 1;
        }
    }

    if ((mc['{'] % 2 != 0) || (mc['['] % 2 != 0) || (mc['"'] % 2 != 0)) { throw new JSONError("Invalid JSON: Unmatched brackets or quotes"); }

    return found_markers;
}

Token ValueValidator(string value)
{
    if (SET_VALUES.ContainsKey(value))
    {
        return new Token(value, SET_VALUES[value]);
    }
    else if (NUMBER_REGEX.IsMatch(value))
    {
        return new Token("number", float.Parse(value));
    }
    return null;
}

Dictionary<string, object> parse_object(string data_big, bool r = false)
{
    List<object> list_data_big = new List<object>() { };
    foreach (char c in data_big) { list_data_big.Add(c); }

    if (!r)
    {
        List<KeyValuePair<char, int>> all_markers = get_all_markers(list_data_big);
        List<Dictionary<string, object>> missed_values = new List<Dictionary<string, object>>();

        for (int m_index = 0; m_index < all_markers.Count - 1; m_index++)
        {
            if (POSSIBLE_MISSED.Contains(all_markers[m_index].Key.ToString() + all_markers[m_index+1].Key.ToString()))
            {
                int start_index = all_markers[m_index].Value;
                int end_index = all_markers[m_index+1].Value;

                // Token missed = ValueValidator('a');
            }
        }

    }


    return new Dictionary<string, object>() { };
}



class Token
{
    public string Type { get; }
    public object Value { get; }

    public Token(string tokenType, object value = null)
    {
        Type = tokenType;
        Value = value;
    }
}

class JSONError : Exception
{
    public JSONError(string message) : base(message)
    {
    }
}


