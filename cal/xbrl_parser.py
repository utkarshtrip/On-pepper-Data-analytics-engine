import pandas as pd
from lxml import etree

def parse_xbrl(file):
    tree = etree.parse(file)
    namespaces = {'xbrli': 'http://www.xbrl.org/2003/instance', 'us-gaap': 'http://fasb.org/us-gaap/2021-01-31'}
    elements = tree.xpath('//us-gaap:*', namespaces=namespaces)

    data = []
    for element in elements:
        tag = element.tag.split('}')[1]
        context = element.get('contextRef')
        value = element.text

        data.append([tag, context, value])
    df = pd.DataFrame(data, columns=['Tag', 'Context', 'Value'])
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')  # Convert 'Value' column to numeric
    # print (df)
    return df
