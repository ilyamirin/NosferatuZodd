from doc_prepr import table
import xml.etree.ElementTree as ET
import imgkit
from os import name as os
from pyvirtualdisplay import Display
print(os)

#for Windows, add wkhtmltopdf
if os == 'nt':
    path_wkhtmltoimage = r"wkhtmltopdf\bin\wkhtmltoimage.exe"
    img_config = imgkit.config(wkhtmltoimage = path_wkhtmltoimage)
if os == 'posix':
    display = Display(size = (800,600), visible = False)
    display.start()

def get_tariff_features(tariff, bank): #TODO исправь этот быдлокод, pandas может лучше
    for i in range(len(table.columns)):
        if table.iloc[0, i] == bank and table.columns[i] == tariff:
            return(table.iloc[:, i])

def features_to_dict(tariff, bank):
    features_dict = {}
    features = get_tariff_features(tariff, bank)
    for i in range(len(features)):
        features_dict[list(table['хар-ка\тариф'])[i]] = list(features)[i]
    return(features_dict)

def compare_tariffs(first_tariff, first_bank, second_tariff, second_bank):
    common_features = {}
    different_features = {}
    first_tariff_dict = features_to_dict(first_tariff, first_bank)
    second_tariff_dict = features_to_dict(second_tariff, second_bank)
    for i in first_tariff_dict:
        if first_tariff_dict[i] == second_tariff_dict[i]:
            common_features[i] = first_tariff_dict[i]
        else: different_features[i] = (first_tariff_dict[i], second_tariff_dict[i])
    return(common_features, different_features)

#for html table generation
def make_table(first_tariff, first_bank, second_tariff, second_bank):
    first_tariff_dict = features_to_dict(first_tariff, first_bank)
    second_tariff_dict = features_to_dict(second_tariff, second_bank)
    html_table = ET.Element('table')
    html_table.attrib['border'] = ''
    tr_header = ET.SubElement(html_table, 'tr')
    for i in 'хар-ка', first_tariff, second_tariff:
        ET.SubElement(tr_header, 'th').text = i
    for i in first_tariff_dict.keys():
        tr_el = ET.SubElement(html_table, 'tr')
        for j in i, first_tariff_dict[i], second_tariff_dict[i]:
            ET.SubElement(tr_el, 'td').text = j
    table = ET.tostring(html_table).decode('UTF-8')
    return(table)

def make_img_from_html(first_tariff, first_bank, second_tariff, second_bank):
    html_table = make_table(first_tariff, first_bank, second_tariff, second_bank)

    if os == 'nt':
        image = imgkit.from_string(html_table, False, config=img_config)
    if os == 'posix':
        image = imgkit.from_string(html_table, False)
    return(image)

client = {
    'first_bank': 'Альфа-Банк',
    'second_bank' : 'МТС Банк',
    'first_tariff' : 'Просто 1%',
    'second_tariff' : 'Проще простого'
}

print(compare_tariffs(client['first_tariff'], client['first_bank'],
                 client['second_tariff'], client['second_bank']))

