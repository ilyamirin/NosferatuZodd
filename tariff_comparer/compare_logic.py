from doc_prepr import table

#for i in table.columns[1:]:
#    for j in table['хар-ка\тариф']:
#        print('тариф: ', i, '\nхарактеристика: ', j, '\nзначение: ', table[i][table['хар-ка\тариф'] == j].values[0], '\n________\n')

def features_to_dict(tariff):
    features_dict = {}
    for i in range(len(table['хар-ка\тариф'])):
        features_dict[list(table['хар-ка\тариф'])[i]] = list(table[tariff])[i]
    return(features_dict)

def compare_tariffs(first_tariff, second_tariff):
    common_features = {}
    different_features = {}
    for i in first_tariff:
        if first_tariff[i] == second_tariff[i]:
            common_features[i] = first_tariff[i]
        else: different_features[i] = (first_tariff[i], second_tariff[i])
    return(common_features, different_features)


#first_tariff = features_to_dict(client['first_tariff'])
#second_tariff = features_to_dict(client['second_tariff'])

#print(compare_tariffs(first_tariff, second_tariff)[1])