from doc_prepr import table

#for i in table.columns[1:]:
#    for j in table['хар-ка\тариф']:
#        print('тариф: ', i, '\nхарактеристика: ', j, '\nзначение: ', table[i][table['хар-ка\тариф'] == j].values[0], '\n________\n')

def get_tariff_features(tariff, bank): #TODO исправь этот быдлокод, pandas может лучше
    for i in range(len(table.columns)):
        if table.iloc[0, i] == bank and table.columns[i] == tariff:
            return(table.iloc[1:, i])

def features_to_dict(tariff, bank):
    features_dict = {}
    features = get_tariff_features(tariff, bank)
    for i in range(len(features)):
        features_dict[list(table['хар-ка\тариф'])[i]] = list(features)[i]
    return(features_dict)

def compare_tariffs(first_tariff, second_tariff):
    common_features = {}
    different_features = {}
    for i in first_tariff:
        if first_tariff[i] == second_tariff[i]:
            common_features[i] = first_tariff[i]
        else: different_features[i] = (first_tariff[i], second_tariff[i])
    return(common_features, different_features)