from data import Data
import glob
from htmlTemplate import HtmlTemplate
from tabulate import tabulate

dataset = []

for json_file in glob.glob('data/*/*.json'):
    print(json_file)
    data = Data(json_file)
    if data.data != None:
        dataset.append(data)
all_info = []
for data in dataset:

    print(data.json_file)
    mydict = data.get_values()
    template = data.get_template()
    date = data.get_date()


    info = []
    for pos, values in mydict.items():
        
        try:
            info.append([template, date, pos, values['A'], values['B'], values['C'], values['D']])
        except KeyError:
            continue
    for i in info:
        all_info.append(i)

headers=['Template key','Dato','Position', 'a', 'b', 'c', 'd']

file_html = open("demo.html", "w")
table = tabulate(all_info, headers=headers, tablefmt='html')
html = HtmlTemplate(table)
file_html.write(html.get_html())