# Antonia Ritter and Luisa Escosteguy
# Jan 22, 2021
# Converts the raw CSV files (athlete_events.csv and noc_regions.csv) 
# into CSV files matching the tables in database-schema.sql

import csv

def create_athlete_csv(athlete_events):
    """
	Creates the file athlete.csv matching table athlete
	"""

def create_olympic_committee_csv(noc_regions):
    """
	Creates the file olympic_committee.csv matching table olympic_committee
	"""

def main():
    athlete_events = csv.reader(open("athlete_events.csv", "r"), delimiter=",")
    noc_regions = csv.reader(open("noc_regions.csv", "r"), delimiter=",")

    create_athlete_csv(athlete_events)
    create_olympic_committee_csv(noc_regions)
    # Do the same for all others csv files matching tables


if __name__ == '__main__':
	main()