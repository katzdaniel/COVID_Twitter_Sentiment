import datetime

DATABASE_LOC = ('data/tweets.db')

def init_week_dict():
    week_dict = dict()

    cur_week = datetime.date(2020, 3, 1)
    time_change = datetime.timedelta(days=6)
    week_counter = 1

    while (cur_week + time_change) < datetime.date.today():
        week_dict[week_counter] = (cur_week, cur_week+time_change)
        week_counter += 1
        cur_week += time_change + datetime.timedelta(days=1)

    return week_dict

CITIES = ['new york', 'los angeles', 'chicago', 'houston', 'phoenix',
          'san antonio', 'philadelphia', 'san diego', 'dallas', 'san jose',
          'austin', 'jacksonville', 'fort worth', 'san francisco', 'charlotte',
          'columbus', 'indianapolis', 'seattle', 'denver', 'washington']

C_TO_COORDS = {'new york': (40.71, -74.00),
               'los angeles': (34.05, -118.24),
               'chicago': (41.87, -87.62),
               'houston': (29.76, -95.36),
               'phoenix': (33.44, -112.07),
               'san antonio': (29.42, -98.49),
               'philadelphia': (39.95, -75.16),
               'san diego': (32.71, -117.16),
               'dallas': (32.77, -96.79),
               'san jose': (37.33, -121.88),
               'austin': (30.26, -97.74),
               'jacksonville': (30.33, -81.65),
               'fort worth': (32.75, -97.33),
               'san francisco': (37.77, -122.41),
               'charlotte': (35.22, -80.84),
               'columbus': (39.96, -82.99),
               'indianapolis': (39.76, -86.15),
               'seattle': (47.60, -122.33),
               'denver': (39.73, -104.99),
               'washington': (38.90, -77.03)}

C_TO_COUNTY = {'new york': ('New York City', 'New York'),
               'los angeles': ('Los Angeles', 'California'),
               'chicago': ('Cook', 'Illinois'),
               'houston': ('Harris', 'Texas'),
               'phoenix': ('Maricopa', 'Arizona'),
               'san antonio': ('Bexar', 'Texas'),
               'philadelphia': ('Philadelphia', 'Pennsylvania'),
               'san diego': ('San Diego', 'California'),
               'dallas': ('Dallas', 'Texas'),
               'san jose': ('Santa Clara', 'California'),
               'austin': ('Austin', 'Texas'),
               'jacksonville': ('Duval', 'Florida'),
               'fort worth': ('Tarrant', 'Texas'),
               'san francisco': ('San Francisco', 'California'),
               'charlotte': ('Mecklenburg', 'North Carolina'),
               'columbus': ('Franklin', 'Ohio'),
               'indianapolis': ('Marion', 'Ohio'),
               'seattle': ('King', 'Washington'),
               'denver': ('Denver', 'Colorado'),
               'washington': ('District of Columbia', 'District of Columbia')}