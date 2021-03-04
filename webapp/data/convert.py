# Kai Johnson and Antonia Ritter
# Feb 21 2021
# convertine crops csv to sql 
# SIDELINED because the data has unique ids 

import csv
from collections import defaultdict

filename = "Production_Crops_E_All_Data_NOFLAG_mod.csv"

def read_csv():

    #format: [area code, area, item code, item...]
    original_data = []
    with open(filename, mode = "r") as file: 
        csvFile = csv.reader(file, delimiter=",") 
        for line in csvFile: 
            original_data.append(line)

    return original_data[1:]


def make_crops_csv(original_data):

    #original data to dict
    crops_dict = defaultdict(int)
    for row in original_data:
        crop = row[3]
        crop_code = row[2]
        crops_dict[crop] = crop_code

    #dict to csv 
    with open("crops.csv", "w") as csvfile: 
        csvWriter = csv.writer(csvfile) 
        for crop in crops_dict.keys():
            csvWriter.writerow([int(crops_dict[crop]), crop])    


def make_countries_csv(original_data):

    #original data to dict
    countries_dict = defaultdict(int)
    for row in original_data:
        country = row[1]
        country_code = row[0]
        countries_dict[country] = country_code

    #dict to csv 
    with open("countries.csv", "w") as csvfile: 
        csvWriter = csv.writer(csvfile) 
        for country in countries_dict.keys():
            csvWriter.writerow([int(countries_dict[country]), country])


def make_country_crop_csv(original_data):
# final csv = [country_id, crop_id, year, production] 
# original data = [area code, area, item code, item, element code, element, unit, Y1961, Y1962, ..., Y2019]

    # get all crops
    crops_set = set()
    for row in original_data:
        crops_set.add(row[2])

    new_csv = []
    countries_and_crops_dict = defaultdict(set)

    year_indices = []
    for i in range(7, 7+59):
        year_indices.append(i)

    for year_index in year_indices: 
        year = year_index + 1954 
        for row in original_data:

            country_code = row[0]
            crop_code = row[2] 
            element = row[5]

            countries_and_crops_dict[country_code].add(crop_code)

            if element == "Production":
                crop_production = row[year_index]
                # if crop_production != '':    # production is not NULL
                #     crop_production = int(crop_production)
                # else: crop_production = null_val # CHANGE ME
                new_csv.append([int(country_code), int(crop_code), int(year), crop_production])

    # get all the country/crop combos that aren't in the data
    for country_code in countries_and_crops_dict.keys():
        missing_crops = (crops_set - countries_and_crops_dict[country_code])
        for crop_code in missing_crops:
            for year in range(1961, 2020):
                new_csv.append([int(country_code), int(crop_code), year, ''])

    with open("country_crop.csv", "w") as csvfile: 
        csvWriter = csv.writer(csvfile) 
        for row in new_csv:
            csvWriter.writerow(row)



def main():
    original_data = read_csv()
    make_crops_csv(original_data)
    make_countries_csv(original_data)
    make_country_crop_csv(original_data)



if __name__ == '__main__':
    main()