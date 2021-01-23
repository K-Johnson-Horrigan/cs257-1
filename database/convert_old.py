# Antonia Ritter and Luisa Escosteguy
# Jan 22, 2021
# Converts the raw CSV files (athlete_events.csv and noc_regions.csv) 
# into CSV files matching the tables in database-schema.sql

import csv
from collections import defaultdict
 

def read_csvs():
    """
    Reads...
    Returns lists, athlete_events and noc_regions 
    """
    athlete_events = []
    noc_regions = [] 

    with open("athlete_events.csv", mode = "r") as file: 
        csvFile = csv.reader(file, delimiter=",") 
        for line in csvFile: 
            athlete_events.append(line)

    with open("noc_regions.csv", mode = "r") as file: 
        csvFile = csv.reader(file, delimiter=",") 
        for line in csvFile: 
            noc_regions.append(line)

    # don't include row 0 (fields) 
    return(athlete_events[1:], noc_regions[1:]) 


def create_athlete_dict(athlete_events):
    """

    """
    athlete_dict = defaultdict(list)
    for athlete in athlete_events: 
        # an athlete is a list: 
        # ["ID","Name","Sex","Age","Height","Weight","Team","NOC","Games","Year","Season","City","Sport","Event","Medal"]
        name = athlete[1] 
        sex = athlete[2]
        age = athlete[3]
        height = athlete[4]
        weight = athlete[5] 
        athlete_dict[name] = [name, age, height, weight, sex]
    return athlete_dict 


def create_athlete_csv(athlete_events):
    """
	Creates the file athlete.csv matching table athlete
	"""
    athlete_dict = create_athlete_dict(athlete_events)
    with open("csvs/athlete.csv", "w") as csvfile: 
        csvWriter = csv.writer(csvfile) 
        athlete_id = 0
        for athlete in sorted(athlete_dict.keys()):
            row = [athlete_id] + athlete_dict[athlete]
            athlete_id += 1 
            csvWriter.writerow(row)


def create_committee_dict(noc_regions):
    noc_dict = defaultdict(list) 
    # create a dictionary where keys are unique nocs 
    for noc in noc_regions:
        # noc fields:
        # [noc, region, notes]
        abbreviation = noc[0]
        region = noc[1]
        notes = noc[2] 
        noc_dict[abbreviation] = [region, abbreviation, notes]
    return noc_dict 


def create_committee_csv(noc_regions):
    """
	Creates the file olympic_committee.csv matching table olympic_committee
	"""
    noc_dict = create_committee_dict(noc_regions)
    with open("csvs/committee.csv", "w") as csvfile: 
        csvWriter = csv.writer(csvfile)
        noc_id = 0
        for noc in sorted(noc_dict.keys()):
            row = [noc_id] +  noc_dict[noc] 
            noc_id += 1 
            csvWriter.writerow(row)


def create_competition_dict(athlete_events):
    competition_dict = defaultdict(list) 
    for athlete in athlete_events:
        # athlete fields: 
        # ["ID","Name","Sex","Age","Height","Weight","Team","NOC","Games","Year","Season","City","Sport","Event","Medal"]
        year = athlete[9]
        season = athlete[10]
        city = athlete[11] 
        competition_name = athlete[8] #"games"
        competition_dict[competition_name] = [year, season, city, competition_name]
    return competition_dict


def create_competetion_csv(athlete_events):
    """
    Creates... 
    """
    competition_dict = create_competition_dict(athlete_events)
    with open("csvs/competition.csv", "w") as csvfile: 
        csvWriter = csv.writer(csvfile)
        comp_id = 0
        for comp in sorted(competition_dict.keys()):
            row = [comp_id] +  competition_dict[comp] 
            comp_id += 1 
            csvWriter.writerow(row)



def create_event_dict(athlete_events):
    event_dict = defaultdict(list) 
    for athlete in athlete_events:
        # athlete fields: 
        # ["ID","Name","Sex","Age","Height","Weight","Team","NOC","Games","Year","Season","City","Sport","Event","Medal"]
        event_name = athlete[13]
        sport = athlete[12] 
        event_dict[event_name] = [event_name, sport] 
    return event_dict


def create_event_csv(athlete_events):
    """
	Creates... 
	"""
    event_dict = create_event_dict(athlete_events)
    with open("csvs/event.csv", "w") as csvfile: 
        csvWriter = csv.writer(csvfile)

        event_id = 0
        for event in sorted(event_dict.keys()):
            row = [event_id] +  event_dict[event] 
            event_id += 1 
            csvWriter.writerow(row)





def create_athlete_competition_csv(athlete_events):
    """
    Creates...
    """

    # loop through athlete_events 
    # create dictionary by athlete+competition 
    # add unique athlete+competition ids to athlete_events 

    # # load committee.csv 
    # committee_list = []
    # with open("csvs/committee.csv", mode = "r") as file: 
    #     csvFile = csv.reader(file, delimiter=",") 
    #     for line in csvFile: 
    #         committee_list.append(line)

    # # load athlete.csv
    # athlete_list = []
    # with open("csvs/athlete.csv", mode = "r") as file: 
    #     csvFile = csv.reader(file, delimiter=",") 
    #     for line in csvFile: 
    #         athlete_list.append(line)

    # # load competition.csv 
    # competition_list = []
    # with open("csvs/competition.csv", mode = "r") as file: 
    #     csvFile = csv.reader(file, delimiter=",") 
    #     for line in csvFile: 
    #         competition_list.append(line)

    athlete_dict = create_athlete_dict(athlete_events) 


    athlete_competition_dict = defaultdict(list) 
    # keys are combinations of athlete and competition: 
    # {"Mike Phelps, Summer 2012" : [...] }

    # loop through athlete_events.csv 
    for athlete in athlete_events:
        # for each athlete, find ids in committee, athlete, and competition 
        name = athlete[1]
        athlete_id = sorted(athlete_dict.keys()).index() 

        athlete_competition_dict[]


    with open("csvs/athlete_competition.csv", "w") as csvfile: 
        csvWriter = csv.writer(csvfile)
        for event in sorted(event_dict.keys()):
            row = [event_id] +  event_dict[event] 
            event_id += 1 
            csvWriter.writerow(row)




def main():
    athlete_events, noc_regions = read_csvs() 

    create_athlete_csv(athlete_events)
    create_committee_csv(noc_regions)
    create_competetion_csv(athlete_events)
    create_event_csv(athlete_events)

if __name__ == '__main__':
	main()