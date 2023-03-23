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

