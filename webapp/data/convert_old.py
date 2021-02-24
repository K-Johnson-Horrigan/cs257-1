# Kai Johnson and Antonia Ritter
# Feb 21 2021
# convertine crops csv to sql 
# SIDELINED because the data has unique ids 

import csv
from collections import defaultdict

filename = "Production_Crops_E_All_Data_NOFLAG.csv"

def read_csv():

    #format: [area code, area, item code]
    original_data = []
    with open(filename, mode = "r") as file: 
        csvFile = csv.reader(file, delimiter=",") 
        for line in csvFile: 
            crops.append(line)

    return crops


def make_crops_dict(original_data);

    crops_dict = defaultdict(int)

    for row in original_data:
        

    return make_crops_dict


def make_countries_dict():

    # blah 

    return make_countries_dict


def make_crops_csv(crops_dict):


def make_countries_csv(countries_dict):


def make_country_crop_csv(crops_dict, countries_dict):



def main():
    original_data = read_csv()
    crops_dict = make_crops_dict()
    countries_dict = make_countries_dict()
    make_crops_csv(crops_dict)
    make_countries_csv(countries_csv)
    make_country_crop_csv(crops_dict, countries_dict)



if __name__ == '__main__':
    main()