import sqlite3, csv
from statistics import fmean
from utils import *

# This file makes both the aggregate csv for the map and the individual tweet data for the distribution hisograms. 

connection = sqlite3.connect(DATABASE_LOC)
cursor = connection.cursor()

def write_aggregate_csv(week_dict):
    with open('data/aggregate_data.csv', mode='w') as file:

        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Week', 'City', 'Longitude', 'Latitude', 'Polarity_Mean', 'Subjectivity_Mean', 'Number_of_Tweets'])

        for week in week_dict.keys():
            for city in CITIES:
                get_data_command = f'Select * FROM tweets WHERE week={int(week)} AND city="{city}"'
                cursor.execute(get_data_command)
                data = cursor.fetchall()

                if(len(data) < 10): continue
                
                p_mean = fmean([data[i][-2] for i in range(len(data))])
                s_mean = fmean([data[i][-1] for i in range(len(data))])

                p_mean = str(round(p_mean, 3))
                s_mean = str(round(s_mean, 3))

                lon = str(C_TO_COORDS[city][1])
                lat = str(C_TO_COORDS[city][0])

                writer.writerow([str(week), city, lon, lat, p_mean, s_mean, str(len(data))])


def write_tweet_csv(week_dict):
    with open('data/tweet_data.csv', mode='w') as file:

        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Week', 'City', 'Longitude', 'Latitude', 'Polarity', 'Subjectivity'])

        for week in week_dict.keys():
            for city in CITIES:
                get_data_command = f'Select * FROM tweets WHERE week={int(week)} AND city="{city}"'
                cursor.execute(get_data_command)
                data = cursor.fetchall()

                lon = str(C_TO_COORDS[city][1])
                lat = str(C_TO_COORDS[city][0])

                for row in data:
                    
                    p_score = str(round(row[-2], 3))
                    s_score = str(round(row[-1], 3))

                    writer.writerow([str(week), city, lon, lat, p_score, s_score])


def main():
    week_dict = init_week_dict()
    write_aggregate_csv(week_dict)
    write_tweet_csv(week_dict)

if __name__=="__main__": 
    main()