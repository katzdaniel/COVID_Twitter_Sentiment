# This project attempts to see the relation between COVID growth and sentiment on Twitter in different American cities.

## A hosted dashboard can be found [here](https://covid-twitter-sentiment.herokuapp.com/).

**This is school project and should not be thought of as anything more.**

## Notes
- It is against Twitter TOS to share individual tweets without embeding a tweet card so I can not share the database with tweets.
    - You can either make your own database by running the scrape<span>.</span>py file.
    - Or, you can use the processed csv files in the repository which I will update.
- The dashboard can be slow at times as it needs to process the data to display it, but the covid graphs are saved as pickle objects for optimization as they are not dynamic beyond changing cities. 
- The dashboard is meant to be displayed on a fullsize 11+ inch screen and will likely not work on smaller screens.
- The scraping starts from the first week of March as COVID related tweets were scarcer before then. 

## Instructions

#### To view the dashboard locally
1. Download the required packages from the requirements.txt file into a conda env or with pip.
2. Run the app<span>.</span>py file and open the link printed into the terminal in a browser.

#### To scrape data from Twitter
1. Download the required packages from the requirements.txt file into a conda env or with pip.
2. Run the scrape.py file. This process will take a while as it often times out and needs to wait. 
    - The cities scraped can be changed by modifying the cities list and city dictionaries in the utils<span>.</span>py file.
    - The search terms used can be modified by adding or modifying the search term list in the main scraping loops in the scrape<span>.</span>py file. 
    - The amount scraped can be changed in the main scraping loops in the scrape<span>.</span>py file.
3. After the database is made, run the process<span>.</span>py file to make the neccasry files for the dashboard.

## Bugs
- The week range selector has an extra unselectable node on the right end as otherwise the week descriptors get cut of.
- Changing the hover text in the map is bugged in dash so there is extraneous when cities are hovered over.
- If scraping too much, the scraper will continually time out and not work.
- Textblob sometimes produces a polarity of exactly .5 or -.5 when the tweet text is not gramatically correct after filtering and thus a wrongful bias forms toward these data points in the polarity and subjectivity averages as well as in the histograms.
- Hovering on the map, a mean Polarity or Subjectivity score will occasionally have an extraneous number of decimals. 

## Citations
- Libraries:
    - Dash/Plotly
    - Twint
    - TextBlob
    - Pandas
- Favicon: https://icons8.com/icons/set/coronavirus
- NYT COVID dataset: https://github.com/nytimes/covid-19-data
- List of cities by population: https://worldpopulationreview.com/us-cities/