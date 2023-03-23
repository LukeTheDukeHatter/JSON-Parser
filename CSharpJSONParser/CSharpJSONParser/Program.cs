Dictionary<string, object> SET_VALUES = new Dictionary<string, object>(){ {"false", false}, {"true", true}, {"null", null} };
char[] VALID_WHITESPACE = { ' ', ' ', ' ', ' ' };
string VALID_CHARS = "[]{}\":,trufasnl+-e.0123456789";
string[] POSSIBLE_MISSED = { ",:", ":,", ",,", "[]", "[,", ",]", ":}", "{:" };

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

int get_closing_index(data, start_index) {
    char open_type = data[start_index];
    Dictionary<char,char> = new Dictionary<char,char>() {{'[',']'}, {'{','}'}, {'"','"'} };
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

        if (bracket_count) == 0 {
            return i;
        }
    }
}

List<KeyValuePair<char,int>> get_all_markers(data) {
    string new_markers = "[]{}\",:";
    bool in_string = false;
    List<KeyValuePair<char,int>> found_markers = new List<KeyValuePair<char,int>>();

    for (int i = 0; i < data.Length; i++) {
        char key = data[i];
        if (key == '"' && data[i > 0 ? i-1 : i] != '\\') {
            in_string = !in_string;
            found_markers.Append(new KeyValuePair<char,int>() {key, i});
        }
        if (new_markers.Contains(key) && !in_string && key != '"') {
            found_markers.Append(new KeyValuePair<char,int>() {key, i});
        }

        Dictionary<char,int> mc = new Dictionary<char,int>() { {'{', 0}, {'[', 0}, {'"', 0} };

        foreach (KeyValuePair<char,int> in found_markers) {
            
        }
    }
}