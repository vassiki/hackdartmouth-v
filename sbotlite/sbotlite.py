import pandas as pd
import numpy as np
import gender_guesser.detector as gender
from bs4 import BeautifulSoup
import requests
import re

def format_names():
    """
    Function to generate a dataframe of male and females names
    The names were downloaded from: 
        http://www.cs.cmu.edu/Groups/AI/util/areas/nlp/corpora/names/0.html
    
    Parameters
    ----------
    none
    
    Returns
    -------
    merged : pandas dataframe with one column each for male and female names
    """
    female_fn = '../names/female.txt'
    male_fn = '../names/male.txt'

    males = pd.read_csv(male_fn, skiprows=4)
    males.rename(columns={males.columns[0]:'MaleNames'}, inplace=True)

    females = pd.read_csv(female_fn, skiprows=4)
    females.rename(columns={females.columns[0]:'FemaleNames'}, inplace=True)

    merged = females.combine_first(males)
    merged = merged.applymap(lambda s:s.lower() if type(s) == str else s)
    
    return merged

def check_name_sex(name):
    """
    Function to check if a given name is male or female using a corpus.
    This function will soon be deprecated, and we will use a combination of 
    gender parser and corpus text instead

    Parameters
    ----------
    name : str specifying first name whose sex needs to be determined

    Returns
    -------
    val : corresponding to whether name is male, female, ambiguous or not
          present in the corpus (unknown)
    """
    merged = format_names()
    name = name.lower()
    maleflags = merged['MaleNames'].eq(name).any()
    femaleflags = merged['FemaleNames'].eq(name).any()
    if maleflags and femaleflags:
        val = 'ambiguous'
    elif maleflags:
        val = 'male'
    elif femaleflags:
        val = 'female'
    else:
        val = 'unknown'
    print('The name {0} was decided to be {1}'.format(name, val))
    return val

def gender_guesser(name):
    """
    Function to use gender guesser package to extract name sex

    Parameters
    ----------
    name : str specifying first name of first author

    Returns
    -------
    label : male, mostly_male, female, mostly_female, andy, unknown
    """
    d = gender.Detector()
    return(d.get_gender(name.capitalize()))

def check_name_contingency(name):
    """
    Function to check gender guesser if corpus is not unknown

    Parameters 
    ----------
    name : str specifying first name of first author

    Returns
    -------
    label : male, female, ambiguous or unknown
    """
    val = check_name_sex(name)
    if val == 'unknown':
        val = gender_guesser(name)
        if val == 'mostly_female':
            return('female')
        elif val == 'mostly_male':
            return('male')
        elif val == 'andy':
            return('ambiguous')
        return(val)
    return(val)

def words_in_line(l):
    """
    Function to extract strings from list of beautiful soup contents
    
    Parameters
    ----------
    l : list of meta data
    
    Returns
    -------
    words : All the words in quotes in the meta data
    """
    words = re.findall(r'"(.*?)"', str(l))
    return words

def bioarxiv_content(link):
    """
    Function to extract names from bioarxiv link

    Parameters
    ----------
    link : html link for beautiful soup
    
    Returns
    -------
    names : list of names of all authors
    """
    page_response = requests.get(link)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    all_meta_info = page_content.find_all("meta")
    listify = list(all_meta_info)
    vals = list(map(words_in_line, listify))
    return vals

def get_names(link):
    """
    Function to extract names from bioarxiv link

    Parameters
    ----------
    link : html link for beautiful soup
    
    Returns
    -------
    names : list of names of all authors
    """
    vals = bioarxiv_content(link)
    allnames = [n[0] for n in vals if 'DC.Contributor' in n]
    
    return allnames

def extract_first_author(page_link):
    """
    Function to extract the first name of the first author given the link to the
    biarxiv article

    Parameters
    ----------
    page_link : link to bioarxiv article

    Returns
    -------
    first_name : first name of the first author
    """
    name_list = get_names(page_link)
    #actual_name = re.findall(r'"(.*?)"', str(meta_name))[0]
    actual_name = name_list[0]
    first_name = actual_name.split(" ")[0]
    return first_name

def extract_metadata(link):
    """
    Function to extract meta data such as time stamp of article and title
    
    Parameters
    ----------
    link : link to bioarxiv article

    Returns
    -------
    metadata : list of metadata
    """
    vals = bioarxiv_content(link)
    date_info = [v[0] for v in vals if "DC.Date" in v]
    title_info = [u[0] for u in vals if "citation_title" in u]
    return [date_info[0], title_info[0]]

def get_bioarxiv_subject(link):
    """
    Function to extract the bioarxiv subfield

    Parameters
    ----------
    link : to bioarxiv article
    
    Returns
    -------
    sbj : bioarxiv subject
    """
    page_response = requests.get(link)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    parse_content = page_content.findAll(
        attrs={'class' : 'highwire-list-wrapper highwire-article-collections'}) 
    for i in parse_content:
        sbj = i.text
    return sbj.rsplit()

def retweet_or_no(link):
    """
    Function to decide whether or not to retweet the link represented by
    the bioarxiv article
    
    Parameters
    ----------
    link : link to bioarxiv article
    
    Returns
    -------
    bool : True, if female or ambiguous
           False, if male or unknown 
    """
    # df = format_names()
    name = extract_first_author(link)
    label = check_name_contingency(name)
    if label == 'female' or label == 'ambiguous':
        return True, label
    return False, label
