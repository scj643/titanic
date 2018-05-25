import csv
import re
import os

STRIP_REGEX_PAREN = re.compile(r'[ _\"\'$!.,]|\([^)]*\)')

TEST_NAME = "testmodel.csv"
TRAIN_NAME = "train.csv"
COMPLETE_NAME = "extended_titanic.csv"
TEST_DATA = "test.csv"
PARSED_DATA = 'parsed.csv'


def parse_csv(file_name):
    """
    Turn csv file into a list of dicts
    :param file_name: file to open
    :return: list with dicts
    """
    with open(file_name, "r") as f:
        items = []
        reader = csv.DictReader(f)
        for row in reader:
            items += [dict(row)]
    return items


def match_items(complete, partial, complete_key="name", partial_key="Name"):
    """
    Matches a complete dict list with a partial one
    :param complete: complete list with dicts
    :param partial: partial list with dicts
    :param complete_key: key to use for matching
    :param partial_key: key to use for matching
    :return:
    """
    all_matches = []
    for i in partial:
        matches = [d for d in complete if
                   STRIP_REGEX_PAREN.sub('', i[partial_key]) in STRIP_REGEX_PAREN.sub('', d[complete_key])]
        for v in matches:
            v['match'] = i
        all_matches += [matches]
    return all_matches


def parse_matches(all_matches):
    """
    convert matches to PassengerId and Survived
    :param all_matches:
    :return: list with dicts that contain keys 'Survived' and 'PassengerId'
    """
    parsed_items = []
    total_parsed_matches = 0
    for n in all_matches:
        if len(n) > 1:
            # print("len greater than 1 in {}".format(i))
            pass
        parsed_items += [{'Survived': n[0]['survived'], 'PassengerId': n[0]['match']['PassengerId']}]
    print(total_parsed_matches)
    return parsed_items


def parse_match_accuracy(parsed_data, testmodel):
    """
    Calculate accuracy of testmodel
    :param parsed_data: data that has complete information
    :param testmodel: the test model with data from R
    :return: Number correctly matched
    """
    matches = 0
    if [d['PassengerId'] for d in parsed_data] == [d['PassengerId'] for d in testmodel]:
        # print("Lists match using quicker method")
        for n in range(0, len(parsed_data)):
            if parsed_data[n]['Survived'] == testmodel[n]['Survived']:
                matches += 1
    else:
        # print("Lists don't match using slow method")
        for p in parsed_data:
            for t in testmodel:
                if p['PassengerId'] == t['PassengerId'] and p['Survived'] == t['Survived']:
                    matches += 1
                    break
                else:
                    continue
    return matches


def make_percent(value, round_to=2):
    """
    Make a value a percentage
    :param value: value to make a percent
    :param round_to: Number of decimals to round to
    :return: String representation of the percentage
    """
    return "%{}".format(round(value * 100, round_to))


if __name__ == '__main__':
    test_data = parse_csv(TEST_DATA)
    train = parse_csv(TRAIN_NAME)
    full = parse_csv(COMPLETE_NAME)
    match_list = match_items(full, test_data)
    if PARSED_DATA:
        parsed = parse_csv(PARSED_DATA)
    else:
        parsed = parsed_match_list = parse_matches(match_list)
    models = os.listdir('models')
    models.sort()
    for i in models:
        test = parse_csv('models/'+i)
        total_matches = parse_match_accuracy(parsed, test)
        t = i.strip('.csv')
        # print('Matches for "{}"'.format(i))
        # print('Total matches {}'.format(total_matches))
        # print('Missed matches {}'.format(len(test)-total_matches))
        print("    {}: Accuracy: {}".format(t, make_percent(total_matches/len(test))))
