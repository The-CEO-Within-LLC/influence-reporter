import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium.webdriver.firefox.options import Options
import link_collection_formating.py as links
import facebook_func.py as book
import csv_formating.py as csv_form


#----------------accessing google sheets---------------
scope =["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"] #these are really important
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope) #json file obtained from google cloud credentials (needed to accesses google sheet)
client = gspread.authorize(creds)

#---------------collecting info from google sheets--------------------
link_sheet=client.open("name of google sheet").get_worksheet('links') #opens a google sheet which contains a list of links in the first column
links_list_sheet=link_sheet.col_values(1) #gets all the links from the sheet opened in the last line 
links.links_to_txt(links_list_sheet) #makes (or appends) a text file to store the links


#-----------------data scraping---------------------
facebook_url_list=links.sub_list_maker("url_list.txt", 'facebook') #creates a list of just the facebook links
waldenu_url_list=links.sub_list_maker('url_list.txt','scholarworks') #creates a list of just the scholarworks links
random_facebook_list=book.choose_five_facebook_links(facebook_url_list) #generates a random list of 4 facebook links
all_data=links.link_collection(random_facebook_list, waldenu_url_list) #runs all the data collection functions (two tuple lists are created here)
social_data=all_data[0] # list of social media data
written_data=all_data[1] #list of academic paper data
csv_form.write_to_csv(social_data, 'social_data.csv') #these lines write the data collected to their respective .csv files
csv_form.write_to_csv(written_data,'written_data.csv')


#--------------formatting and relaying data-----------------------
sheet_social = client.open("name of google sheet").get_worksheet('social')
sheet_written = client.open('name of google sheet').get_worksheet('written')


social_dataframe_unf=csv_form.csv_to_frame('social_data.csv')
social_dataframe_form=csv_form.formatting_df(social_dataframe_unf)
print('social formatting done')
written_dataframe_unf=csv_form.csv_to_frame('written_data.csv')
written_dataframe_form=csv_form.formatting_df(written_dataframe_unf)
print('written formatting done')
sheet_social.update([social_dataframe_form.columns.values.tolist()] + social_dataframe_form.values.tolist()) #uploads the data frame to the google sheet
print('social sheet uploaded')
sheet_written.update([written_dataframe_form.columns.values.tolist()] + written_dataframe_form.values.tolist())
print('written sheet uploaded')
print('script done')
