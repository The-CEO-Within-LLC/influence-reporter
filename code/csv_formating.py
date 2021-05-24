import datetime as date
import pandas as pd
import csv


def get_date():
    '''

    :return: returns todays date
    '''
    today = date.today()
    return today

def write_to_csv(info, file_name):
    '''
    appends a .csv file
    :param info: a list of tuples with format (int, string)
    :param file_name: the name of a .csv file to be added to
    :return: none
    '''
    data_writer = csv.writer(open(file_name, "a+", newline=''), delimiter=',')
    date=get_date()
    for tuple in info:
        data_writer.writerow([tuple[1], tuple[0], date])

def csv_to_frame(file_name):
    '''
    converts a .csv file to a dataframe
    :param file_name: a .csv file that has 3 items per line
    :return: a dataframe
    '''
    df = pd.read_csv(file_name, names = ["name", "number", "date"])
    return df

def formatting_df(df):
    '''
    formats the data frame for easy use. If this function is causing errors it is likely due to there being data taken from the same data but with a different value. (simply delete that bad data to resolve the issue)
    :param df: a pandas dataframe
    :return: a nice dataframe
    '''
    df = df.drop_duplicates() #deletes and duplicate entries
    df['number']=pd.to_numeric(df['number']) #converts pesky strings
    df_formatted = df.pivot(index="date", columns='name',values='number') #columns become the titles and the index becomes date
    df_formatted=df_formatted.interpolate('linear') #any nan values are converted to an estimate using a linear function
    df_formatted['date'] = df_formatted.index
    df_formatted.insert(0, value=df_formatted.pop('date'), column='date') #this line makes it so when the dataframe is uploaded to google sheets the index will be visible
    df_formatted=df_formatted.iloc[::-1] #reverses the index (frame will start at the most recent date and the last lin will be the oldest)
    df_formatted=df_formatted.fillna(value=0) #any nan values get turned into 0
    return df_formatted