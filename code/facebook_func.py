import random as random
#facebook doesn't like being scraped so these functions, given a list of facebook links, will select 4 unique links every time the script is run.
def random_ints(length, number_of_items):
    '''
    This function creates a list of unique random ints between 0 and number_of_items. Using a cache it 'remembers' the previous random numbers it generated so over the course of multiple script calls this function will not repeat until it runs out of unique numbers
    :param length: the length of the returned list
    :param number_of_items: the number of items in some list
    :return: a list of size length with random int between 0 and number_of_items
    '''
    cache=read_from_cache()
    list=[]
    i=0
    while len(list)!=length:
        ran_int = random.randint(0, number_of_items-1)
        i+=1
        if i == 12: #this will clear the cache if there are not enough unique numbers to fill the list
            clear_cache()
            return random_ints(length, number_of_items)
        elif ran_int not in cache and ran_int not in list:
            list.append(ran_int)
    write_to_cache(list)
    return list
	
def choose_five_facebook_links(link_list):
    '''
    using a list of ints this function selects items from a list
    :param link_list: a list of strings
    :return: a sublist of strings from link_list
    '''
    int_list=random_ints(length=4,number_of_items=len(link_list)) #facebook only lets you scrape 4 sites at a time so DO NOT CHANGE THE LENGTH!!!!!
    ran_link_list=[]
    for i in int_list:
        ran_link_list.append(link_list[i])
    return ran_link_list

def write_to_cache(list):
    '''
    adds items from a list to a txt doc
    :param list: a list
    :return: nothing
    '''
    f = open('facebook_cache.txt', 'a')
    for char in list:
        f.write(str(char) + ',')
    f.close()


def read_from_cache():
    '''
    reads a one line, comma seperated txt document and adds each item to a list
    :return: a list containing all the items in the txt doc
    '''
    f=open('facebook_cache.txt','r')
    list=[]
    for line in f:
        list=line.split(',')
    if list!=[]:
        list.pop(len(list)-1) #removes the empty item added by the split (this is because when adding items to the txt doc there is always a comma after every item)
    int_list=[]
    for i in list:
        int_list.append(int(i))
    return int_list

def clear_cache():
    '''
    deletes the contents of the facebook_cache.txt file
    :return: none
    '''
    f=open('facebook_cache.txt','r+')
    f.truncate(0)
    f.close()