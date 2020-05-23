import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px

import pandas as pd
import time, math, pickle, datetime

from utils import *
from markdown_text import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title ='COVID Sentiment Dashboard'

server = app.server

agg_df = pd.read_csv('data/aggregate_data.csv')

def add_text_col(df):
    df['text'] = df.apply(lambda row:str(row.City.title()) + '<br>' + 'Polarity Mean=' + str(row.Polarity_Mean) + '<br>' + 'Subjectivity Mean=' + str(row.Subjectivity_Mean), axis=1)

add_text_col(agg_df)

map = px.scatter_geo (
    data_frame=agg_df[agg_df.Week == 1],
    lat='Latitude',
    lon='Longitude',
    text='text',
    scope='usa',
)

map.update_layout(
    title={
        'text': 'Mean Polarity and Subjectivity From Mar 1 - to Mar 7',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
)

tweet_df = pd.read_csv('data/tweet_data.csv')

p_dist_hist = px.histogram(
    data_frame=tweet_df[(tweet_df['Week'] == 1) & (tweet_df['City'] == 'new york')],
    x='Polarity',
    histnorm='percent',
    labels={'x': 'Polarity', 'y': 'Percent'}
)

p_dist_hist.update_layout(
    title={
        'text': 'Polarity Distribution From Mar 1 - Mar 7 in New York',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },

    xaxis_title='Polarity',
    yaxis_title='Percent'
)

s_dist_hist = px.histogram(
    data_frame=tweet_df[(tweet_df['Week'] == 1) & (tweet_df['City'] == 'new york')],
    x='Subjectivity',
    histnorm='percent',
)

s_dist_hist.update_layout(
    title={
        'text': 'Subjectivity Distribution From Mar 1 - Mar 7 in New York',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },

    xaxis_title='Subjectivity',
    yaxis_title='Percent'
)

week_dict = init_week_dict()
max_week = tweet_df['Week'].max()+1

def week_slider_desc(week_num):
    return f'{date_format(week_dict[week_num][0])} - {date_format(week_dict[week_num][1])}'

def date_format(dt_obj):
    return dt_obj.strftime("%b %-d")

covid_cases = pickle.load(open('data/covid_cases_graphs.p', 'rb'))

city_covid_cases_area = covid_cases['new york']

city_covid_cases_area.update_layout(
    shapes=[
        {'type': 'line',

        'yref': 'paper',
        'y0': 0,
        'y1': 1,

        'xref': 'x',
        'x0': week_dict[1][0],
        'x1': week_dict[1][0],},

        {'type': 'line',

        'yref': 'paper',
        'y0': 0,
        'y1': 1,

        'xref': 'x',
        'x0': week_dict[1][1],
        'x1': week_dict[1][1],}]
)

app.layout = html.Div([
    html.Div([

        # first row div
        html.Div([
            html.H1(id='header', 
                children=['COVID-19 Twitter Sentiment in Biggest 20 Cities in USA'], 
                className='twelve columns'),
        ], className='row'),

        # second row div
        html.Div([

            # Week Range Slider Title
            html.P(id='week-slider-title', children=['Week Range Slider'], 
                className='twelve columns')
        ], className='row'),


        # third row div
        html.Div([

            html.P('', className='one columns'),


            # Week Range Slider
            html.Div([
                dcc.RangeSlider(
                id='week-slider',
                min=agg_df['Week'].min(),
                max=agg_df['Week'].max()+1,
                value=[agg_df['Week'].min(), agg_df['Week'].min()],
                marks={str(i): {'label':week_slider_desc(i)} for i in agg_df['Week'].unique()},
                step=None,
                allowCross=False),
            ], className='ten columns'),
            
        ], className='row'),

        html.Br(),

        # fourth row div, has map and two dist hists
        html.Div([

            html.P(className='one column'),

            html.Div(first_row_md, className='md three columns'),

            dcc.Graph(id='map', figure=map, hoverData={'points': [{'text': 'new york<'}]},
                className='four columns'),

            dcc.Graph(id='p-dist-hist', figure=p_dist_hist, className='four columns'),
            

        ], className='row'),

        # fith row div, has text week table, and cases graph
        html.Div([

            html.P(className='one column'),

            html.Div(second_row_md, className='md three columns'),


            dcc.Graph(
                id='covid-cases-area',
                figure=covid_cases['new york'],
                className='four columns'),

            dcc.Graph(id='s-dist-hist', figure=s_dist_hist, className='four columns')

        ], className='row')
    ])
], id='main-div')

@app.callback(
    Output('map', 'figure'),
    [Input('week-slider', 'value')])
def update_map(selected_weeks):

    f_agg_df = get_ranged_agg_tweet_df(*selected_weeks)
    add_text_col(f_agg_df)

    map = px.scatter_geo(
        data_frame=f_agg_df,
        lat='Latitude',
        lon='Longitude',
        text='text',
        scope='usa',
    )  

    map.update_layout(
        title={
            'text': f'Mean Polarity and Subjectivity From {date_format(week_dict[selected_weeks[0]][0])} - To {date_format(week_dict[selected_weeks[1]][1])}',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
     )

    return map


@app.callback(
    [Output('p-dist-hist', 'figure'),
    Output('s-dist-hist', 'figure'),
    Output('covid-cases-area', 'figure')],
    [Input('map', 'hoverData'),
    Input('week-slider', 'value')])
def update_dist_hists(hoverData, selected_weeks):

    city = hoverData['points'][0]['text'].split('<')[0].lower()

    w1, w2 = selected_weeks

    f_tweet_df = tweet_df[(tweet_df['City'] == city) & (tweet_df['Week'] >= w1) & (tweet_df['Week'] <= w2)]

    p_dist_hist = px.histogram(
        data_frame=f_tweet_df,
        x='Polarity',
        histnorm='percent',
        
    )

    p_dist_hist.update_layout(
        title={
        'text': f'Polarity Distribution From {date_format(week_dict[w1][0])} - {date_format(week_dict[w2][1])} in {city.title()}',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
        },

        xaxis_title='Polarity',
        yaxis_title='Percent'
    )

    s_dist_hist = px.histogram(
        data_frame=f_tweet_df,
        x='Subjectivity',
        histnorm='percent',
    )

    s_dist_hist.update_layout(
        title={
        'text': f'Subjectivity Distribution From {date_format(week_dict[w1][0])} - {date_format(week_dict[w2][1])} in {city.title()}',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
        },

        xaxis_title='Subjectivity',
        yaxis_title='Percent'
    )

    city_covid_cases_area = covid_cases[city]

    city_covid_cases_area.update_layout(shapes=[
        {'type': 'line',

        'yref': 'paper',
        'y0': 0,
        'y1': 1,

        'xref': 'x',
        'x0': week_dict[w1][0],
        'x1': week_dict[w1][0],},
        
        {'type': 'line',

        'yref': 'paper',
        'y0': 0,
        'y1': 1,

        'xref': 'x',
        'x0': week_dict[w2][1],
        'x1': week_dict[w2][1],}])

    return p_dist_hist, s_dist_hist, city_covid_cases_area


def get_ranged_agg_tweet_df(w1, w2):
    city_dict = [dict() for i in range(len(CITIES))]

    for i, c in enumerate(CITIES):

        city_df = agg_df[(agg_df['City'] == c) & (agg_df['Week'] >= w1) & (agg_df['Week'] <= w2)]
        
        city_tweet_num_sum = city_df['Number_of_Tweets'].sum()

        temp_p_avg = 0
        temp_s_avg = 0

        for j, row in city_df.iterrows():
            row_num_tweets = row['Number_of_Tweets']
            temp_p_avg += row['Polarity_Mean'] * (row_num_tweets / city_tweet_num_sum)
            temp_s_avg += row['Subjectivity_Mean'] * (row_num_tweets / city_tweet_num_sum)
        
        city_dict[i]['City'] = c
        city_dict[i]['Longitude'] = C_TO_COORDS[c][1]
        city_dict[i]['Latitude'] = C_TO_COORDS[c][0]
        city_dict[i]['Polarity_Mean'] = round(temp_p_avg, 3)
        city_dict[i]['Subjectivity_Mean'] = round(temp_s_avg, 3)

    return pd.DataFrame(city_dict)


if __name__ == '__main__':
    app.run_server(debug=True)