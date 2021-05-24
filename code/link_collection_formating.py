import data_scrape.py as scrape


def links_to_txt(list):
    '''
    writes a list of string into a txt file. each string gets its own line
    :param list: a list
    :return: none
    '''
    file=open('url_list.txt', 'w') 
    for link in list:
        file.write(link +'\n')
    file.close()


def sub_list_maker(link_list, string):
    '''

    :param link_list: a list of strings
    :param string: an indicator for which type of links one would like take make a sublist out of
    :return: a list of links which all contain the inputted string
    '''
    f=open(link_list, "r")
    sub_list = []
    for link in f:
        if string in link:
            sub_list.append(link.replace('\n',''))
    return sub_list
	

def link_collection(facebook_list, waldenu_list):
    '''

    :param facebook_list: list of facebook links (made automatically by another function)
    :param waldenu_list: list of scholarworks links (made automatically by anoother function)
    :return: a list with of tuples with the titles and number of impressions for each website input
    '''
    f=open("url_list.txt", "r") #note that this is the same text file from links_to_text()
    num_and_title_list_social=[] #list for social media data
    num_and_title_list_written=[] #list for academic data
    for link in facebook_list:
        if "business.facebook" in link:
            num_and_title_list_social.append(scrape.data_grab_facebook_business(link))
        elif "www.facebook" in link:
            num_and_title_list_social.append(scrape.data_grab_facebook(link))
    scholar_data=scrape.data_grab_waldenu(waldenu_list)
    for tuple in scholar_data:
        num_and_title_list_written.append(tuple)
    for line in f:
        if 'researchgate.net' in line:
            num_and_title_list_written.append(scrape.data_grab_researchgate(line))
        else:
            print("")
    return (num_and_title_list_social, num_and_title_list_written)