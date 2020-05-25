import pickle, csv, datetime
import pandas as pd
import plotly.express as px

from utils import *

# This file makes the pickle files of the covid growth graphs. 

week_dict = init_week_dict()

tweet_df = pd.read_csv('data/tweet_data.csv')
covid_df = pd.read_csv('data/us-counties-covid.csv')


def make_covid_graph_pickle():
    cities_covid_graph_dict = dict()

    max_date = week_dict[tweet_df['Week'].max()][1]

    for c in CITIES:
        county = C_TO_COUNTY[c][0]
        state = C_TO_COUNTY[c][1]

        city_df = covid_df[(covid_df['county'] == county) & (covid_df['state'] == state)]

        city_day_dfs = list()

        cur_day = week_dict[1][0]

        while cur_day <= max_date:

            city_day_dfs.append(city_df[(city_df['date'] == cur_day.isoformat())])

            cur_day += datetime.timedelta(days=1)
    
        city_covid_df = pd.concat(city_day_dfs)

        city_covid_fig = px.area(city_covid_df, x='date', y='cases')

        city_covid_fig.update_layout(
            title={
                'text': f'Confirmed COVID Cases in {c.title()}',
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },

            xaxis_title='Date',
            yaxis_title='Cases'
        )

        cities_covid_graph_dict[c] = city_covid_fig

    pickle.dump(cities_covid_graph_dict, open('data/covid_cases.p', 'wb'))
        


def main():
    make_covid_graph_pickle()

if __name__=="__main__": 
    main()