import subprocess, datetime, time, re, math
import sqlite3
from textblob import TextBlob
from utils import *

# This file scrapes Twitter using twint and then adds it to a sqlite database called tweets.db
# The amount of tweets scraped and the search terms used are marked below and can be changed.
# The cities where the location is scraped can be modified in the utils.py file. 

connection = sqlite3.connect(DATABASE_LOC)
cursor = connection.cursor()

def init_db():
    create_db_command = """
    CREATE TABLE IF NOT EXISTS tweets (
    tweet_id INTEGER PRIMARY KEY,
    username TEXT,
    tweet TEXT,
    city TEXT,
    week INTEGER,
    date TEXT,
    time TEXT,
    polarity REAL,
    subjectivity REAL);"""

    cursor.execute(create_db_command)
    connection.commit()


def fill_db(week_dict):
    for key in week_dict.keys():

        check_prev_command = f'Select week FROM tweets WHERE week={key}'
        cursor.execute(check_prev_command)
        existing_week_records = cursor.fetchall()
        if len(existing_week_records) > 0: continue

        for city in CITIES:
            # To change the search terms, modify the below list. 
            for term in ['covid', 'coronavirus']:
                run_twint_and_save(city, week_dict[key][0], week_dict[key][1], key, term)

        connection.commit()
        print('Commited to database')

def run_twint_and_save(city, start_date, end_date, week_num, search_term):
    twint_command = ['twint', 
                     '-s', search_term,
                     '-l', 'en',
                     # To modify the maximum number of tweets searched per twint call, modify the below number.
                     '--limit', '2000',
                     '--near', city,
                     '--since', start_date.isoformat(),
                     '--until', end_date.isoformat()]

    twint_out = subprocess.Popen(twint_command, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)

    while True:
        try:
            line = twint_out.stdout.readline().decode('utf-8').strip()
            if not line: break

            split_line = line.split(' ', 5)


            check_unique_command = f'Select tweet_id FROM tweets WHERE tweet_id={int(split_line[0])}'
            cursor.execute(check_unique_command)
            existing_matching_records = cursor.fetchall()
            if len(existing_matching_records) > 0: continue

            split_line[4] = split_line[4][1:-1].replace('"', '\'')
            
            split_line[5] = filter_tweet(split_line[5])

            blobbed_text = TextBlob(split_line[5])

            if math.isclose(blobbed_text.polarity, 1.0): continue
            if math.isclose(blobbed_text.polarity, 0.0): continue
            if math.isclose(blobbed_text.polarity, -1.0): continue

            if math.isclose(blobbed_text.subjectivity, 1.0): continue
            if math.isclose(blobbed_text.subjectivity, 0.0): continue
            
            
            add_tweet_command = f"""
            INSERT INTO tweets (tweet_id, username, tweet, city,
                                week, date, time, polarity, subjectivity)
            VALUES ({split_line[0]}, "{split_line[4]}", 
                    "{split_line[5]}", "{city}",  {week_num},
                    "{split_line[1]}", "{split_line[2]}",
                    {round(blobbed_text.polarity, 10)}, 
                    {round(blobbed_text.subjectivity, 10)});"""

            cursor.execute(add_tweet_command)
            print('Added to db')
        
        except ValueError:
            print('Timeout occured, waiting 9 minutes')
            time.sleep(540)
            print('Scraping again')

def filter_tweet(tweet):

    f_tweet = re.sub(r'http\S+', '', tweet)

    f_tweet = re.sub(r'pic.twitter\S+', '', f_tweet)

    f_tweet = f_tweet.replace('"', '\'')

    f_tweet = re.sub(r'[^\x00-\x7f]' , '', f_tweet)

    f_tweet = re.sub(r'[@#]', '', f_tweet)

    f_tweet = re.sub(r'/./', '', f_tweet)

    f_tweet = re.sub(r'\.+\.', '', f_tweet)

    f_tweet = ' '.join(f_tweet.split()).strip()

    return f_tweet

def main():
    init_db()
    week_dict = init_week_dict()    
    fill_db(week_dict)

if __name__=="__main__": 
    try:
        main()
    except KeyboardInterrupt:
        connection.commit()
