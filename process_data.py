import make_csvs, pickle_graphs

# This file just simplifies the process of collecting data and making the neccesary for files the dashboard. 

def main():
    make_csvs.main()
    pickle_graphs.main()

if __name__=="__main__": 
    main()