import pickle_graphs, make_csvs

# This file just simplifies the process of collecting data and making the neccesary for files the dashboard. 

def main():
    pickle_graphs.main()
    make_csvs.main()

if __name__=="__main__": 
    main()