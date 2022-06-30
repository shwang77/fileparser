import sys
import json
import pandas as pd
import xml.etree.ElementTree as et

def parse_XML(xml_file, df_cols):
    """Parse the input XML file and store the result in a pandas
    DataFrame with the given columns.

    The first element of df_cols is supposed to be the identifier
    variable, which is an attribute of each node element in the
    XML data; other features will be parsed from the text content
    of each sub-element.
    """

    xtree = et.parse(xml_file)
    xroot = xtree.getroot()
    rows = []

    for node in xroot:
        res = []
        res.append(node.attrib.get(df_cols[0]))
        for el in df_cols[1:]:
            if node is not None and node.find(el) is not None:
                res.append(node.find(el).text)
            else:
                res.append(None)
        rows.append({df_cols[i]: res[i]
                     for i, _ in enumerate(df_cols)})

    out_df = pd.DataFrame(rows, columns=df_cols)

    return out_df

def parse_JSON(json_file):
    with open(json_file) as f:
        json_file = json.load(f)
    out_df = pd.json_normalize(json_file, record_path =['issues'], meta=['pk', 'source'])
    return out_df

def parse_TXT(txt_file):
    out_df = pd.read_csv(txt_file)
    return out_df

def main():

    filetype = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    df = pd.DataFrame()
    if(filetype == 'json'):
       df = parse_JSON(input_file)
    if (filetype == 'txt'):
        df = parse_TXT(input_file)
    if(filetype == 'xml'):
       xml_fields = ["name", "email", "grade", "age"]
       df = parse_XML(input_file, xml_fields)

    df.to_csv(output_file, '\t', index=False)

if __name__ == '__main__':
    main()
