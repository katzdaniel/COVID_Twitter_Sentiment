from dash_core_components import Markdown

# This file is where the markdown for the text in the dashboard is stored. 

first_row_md = Markdown("""  
###### Introduction:
This project attempts to track sentiment (polarity and subjectivity) on Twitter from the top 20 cities in America and easily view the results and compare it to the spread of COVID-19 in those cities.

###### Instructions:

- Drag one end of the week range slider to change the week(s) shown in the data.
    - When the two ends are on top of eachother, such as when no changes have been made, click on a selected week to show the two ends of the slider.
    - When the selected week(s) change, the vertical lines in the total cases graph they show the start and end of the selected weeks.
- Hover over different cities in the map to change the displayed data to be about the selected city.
    - When hovering over a city, a pop-up will appear that shows information such as average polarity and subjectivty in that city in the given time frame.

""")

second_row_md = Markdown("""
###### Definitions:
- Polarity how positive or negative an individual Tweet is. The greater the polarity, the more positive the tweet and the lesser the polarity, the more negative a tweet.
- Subjectivity is how objective an individual Tweet is. The closer the subjectivity score is to 0, the more objective a tweet and the closer the subjectivity score is to 1, the more subjective it is.

###### Notes:
- This website was designed to be displayed on a fullsize 11+ inch screen and will likely not work on smaller screens.
- The website might be a bit slow as it dynamically process most of the its data.
  
  
Source code, citations, and a list of bugs can be found at this [github repository](https://github.com/Quadr0/COVID_Twitter_Sentiment).
""")