# Antonia Ritter and Luisa Escosteguy
# Jan 22, 2021
# Converts the raw CSV files (athlete_events.csv and noc_regions.csv) 
# into CSV files matching the tables in database-schema.sql

import csv
from collections import defaultdict
 
def read_csvs():
    """
    Reads athlete_events.csv and noc_regions.csv. Returns lists.
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

    return(athlete_events[1:], noc_regions[1:]) 


def add_athlete_ids(athlete_events):
    """
    Add athlete_id as a column to athlete_events. 
    """
    # Key is athlete name, value is id 
    id_dict = defaultdict(int)

    id_counter = 0
    for athlete in athlete_events:
        name = athlete[1] 
        if not id_dict[name]:
            id_dict[name] = id_counter
            id_counter += 1
        
    athlete_events_updated = []
    for athlete in athlete_events:
        row = athlete + [id_dict[athlete[1]]] 
        athlete_events_updated.append(row) 

    return athlete_events_updated


def add_committee_ids(athlete_events):
    """
    Add committee_id as a column to athlete_events. 
    """
    # Key is noc abbreviation, value is id
    id_dict = defaultdict(int)

    id_counter = 0
    for athlete in athlete_events:
        noc = athlete[7] 
        if not id_dict[noc]:
            id_dict[noc] = id_counter
            id_counter += 1
        
    athlete_events_updated = []
    for athlete in athlete_events:
        row = athlete + [id_dict[athlete[7]]] 
        athlete_events_updated.append(row) 

    return athlete_events_updated


def add_competition_ids(athlete_events):
    """
    Add competition_id as a column to athlete_events. 
    """
    # Key is game, value is id 
    id_dict = defaultdict(int)

    id_counter = 0
    for athlete in athlete_events:
        game = athlete[8] 
        if not id_dict[game]:
            id_dict[game] = id_counter
            id_counter += 1
        
    athlete_events_updated = []
    for athlete in athlete_events:
        row = athlete + [id_dict[athlete[8]]] 
        athlete_events_updated.append(row) 

    return athlete_events_updated


def add_event_ids(athlete_events):
    """
    Add event_id as a column to athlete_events. 
    """
    # Key is event name, value is id 
    id_dict = defaultdict(int)

    id_counter = 0
    for athlete in athlete_events:
        event = athlete[13] 
        if not id_dict[event]:
            id_dict[event] = id_counter
            id_counter += 1
        
    athlete_events_updated = []
    for athlete in athlete_events:
        row = athlete + [id_dict[athlete[13]]] 
        athlete_events_updated.append(row) 

    return athlete_events_updated


def add_athlete_competition_ids(athlete_events):
    """
    Add athlete_competition_id as a column to athlete_events. 
    """
    # Key is (athlete_id, committee_id, competition_id) value is id 
    athlete_comp_dict = defaultdict(int) 

    id_counter = 0

    for athlete in athlete_events:
        athlete_id = athlete[15] 
        committee_id = athlete[16]
        competition_id = athlete[17]
        if not athlete_comp_dict[(athlete_id, committee_id, competition_id)]:
            athlete_comp_dict[(athlete_id, committee_id, competition_id)] = id_counter
            id_counter += 1 

    athlete_events_updated = []
    for athlete in athlete_events:
        athlete_id = athlete[15] 
        committee_id = athlete[16]
        competition_id = athlete[17]
        athlete_comp_id = athlete_comp_dict[(athlete_id, committee_id, competition_id)]
        row = athlete + [athlete_comp_id] 
        athlete_events_updated.append(row) 

    return athlete_events_updated


def add_all_ids(athlete_events):
    """
    Calls all the functions to add ids as a column to athlete_events
    """
    athlete_events = add_athlete_ids(athlete_events)
    athlete_events = add_committee_ids(athlete_events)
    athlete_events = add_competition_ids(athlete_events)
    athlete_events = add_event_ids(athlete_events)
    athlete_events = add_athlete_competition_ids(athlete_events)
    return athlete_events 


def create_athlete_csv(athlete_events):
    """
	Creates the file athlete.csv matching table athlete
	"""
    athlete_dict = defaultdict(list)
    for athlete in athlete_events: 
        # An athlete is a list: 
        # ["ID","Name","Sex","Age","Height","Weight","Team","NOC","Games","Year","Season","City","Sport","Event","Medal", athlete_id, committee_id, competition_id, event_id, athlete_competition_id]
        athlete_id = athlete[15] 
        name = athlete[1] 
        sex = athlete[2]
        age = athlete[3] if athlete[3] != "NA" else "NULL"
        height = athlete[4] if athlete[4] != "NA" else "NULL"
        weight = athlete[5] if athlete[5] != "NA" else "NULL"
        athlete_dict[athlete_id] = [athlete_id, name, age, height, weight, sex]

    with open("csvs/athlete.csv", "w") as csvfile: 
        csvWriter = csv.writer(csvfile) 
        for athlete in athlete_dict.keys():
            csvWriter.writerow(athlete_dict[athlete]) 


def create_committee_csv(athlete_events, noc_regions):
    """
	Creates the file committee.csv matching table committee
	"""
    # Key is committee abbreviation, value is committee_id
    noc_id_dict = defaultdict(int)
    for athlete in athlete_events:
        noc_id_dict[athlete[7]] = athlete[18]

    noc_dict = defaultdict(list) 
    for noc in noc_regions:
        # Noc fields:
        # [noc, region, notes]
        abbreviation = noc[0]
        committee_id = noc_id_dict[abbreviation]
        region = noc[1]
        notes = noc[2] 
        noc_dict[committee_id] = [committee_id, region, abbreviation, notes]

    with open("csvs/committee.csv", "w") as csvfile: 
        csvWriter = csv.writer(csvfile)
        for noc in noc_dict.keys():
            csvWriter.writerow(noc_dict[noc])


def create_competition_csv(athlete_events):
    """
    Creates the file competition.csv matching table competition 
    """
    competition_dict = defaultdict(list) 
    for athlete in athlete_events:
        competition_id = athlete[17]
        year = athlete[9]
        season = athlete[10]
        city = athlete[11] 
        competition_name = athlete[8]
        competition_dict[competition_id] = [competition_id, year, season, city, competition_name]    
        
    with open("csvs/competition.csv", "w") as csvfile: 
        csvWriter = csv.writer(csvfile)
        for comp in competition_dict.keys():
            csvWriter.writerow(competition_dict[comp])


def create_event_csv(athlete_events):
    """
	Creates the file event.csv matching table event 
	"""
    event_dict = defaultdict(list) 
    for athlete in athlete_events:
        # athlete fields: 
        #["ID","Name","Sex","Age","Height","Weight","Team","NOC","Games","Year","Season","City","Sport","Event","Medal", athlete_id, committee_id, competition_id, event_id, athlete_competition_id]
        event_id = athlete[18]
        event_name = athlete[13]
        sport = athlete[12] 
        event_dict[event_id] = [event_id, event_name, sport] 

    with open("csvs/event.csv", "w") as csvfile: 
        csvWriter = csv.writer(csvfile)

        for event in sorted(event_dict.keys()):
            row = event_dict[event] 
            csvWriter.writerow(row)


def create_athlete_competition_csv(athlete_events):
    """
	Creates the file athlete_competition.csv matching table athlete_competition 
	"""
    # key is athlete_competition_id 
    # value is [athlete_competition_id, athlete_id, competition_id, committee_id]
    #["ID","Name","Sex","Age","Height","Weight","Team","NOC","Games","Year","Season","City","Sport","Event","Medal", athlete_id, committee_id, competition_id, event_id, athlete_competition_id]
    athlete_comp_dict = defaultdict(list) 

    for athlete in athlete_events:
        athlete_id = athlete[15] 
        committee_id = athlete[16]
        competition_id = athlete[17]
        athlete_competition_id = athlete[19]
        athlete_comp_dict[athlete_competition_id] = [athlete_competition_id, athlete_id, competition_id, committee_id] 
        
    with open("csvs/athlete_competition.csv", "w") as csvfile: 
        csvWriter = csv.writer(csvfile)
        for athlete_comp_id in athlete_comp_dict.keys():
            csvWriter.writerow(athlete_comp_dict[athlete_comp_id])


def create_athlete_competition_event_csv(athlete_events):
    """
	Creates the file athlete_competition_event.csv matching table athlete_competition_event
	"""
    # key is (athlete_competition_id, event_id)
    # value is [athlete_competition_id, event_id, medal]
    ace_dict = defaultdict() #a.c.e = athlete_competition_event 

    for athlete in athlete_events:
        athlete_competition_id = athlete[19]
        event_id = athlete[18]
        medal = athlete[14] if athlete[14] != "NA" else "NULL"
        ace_dict[(athlete_competition_id, event_id)] = [athlete_competition_id, event_id, medal] 

    with open("csvs/athlete_competition_event.csv", "w") as csvfile: 
        csvWriter = csv.writer(csvfile)
        for ace_id in ace_dict.keys():
            csvWriter.writerow(ace_dict[ace_id])


def main():
    athlete_events, noc_regions = read_csvs() 
    athlete_events = add_all_ids(athlete_events)

    create_athlete_csv(athlete_events)
    create_committee_csv(athlete_events, noc_regions)
    create_competition_csv(athlete_events)
    create_event_csv(athlete_events)
    create_athlete_competition_csv(athlete_events)
    create_athlete_competition_event_csv(athlete_events)

if __name__ == '__main__':
    main()