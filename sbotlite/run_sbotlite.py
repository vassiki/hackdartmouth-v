import sbotlite
import pandas as pd

def get_info(link):
    """
    Function to generate metadata for each first author
    """
    rt_o_not, label = sbotlite.retweet_or_no(link)
    rt = 1 if rt_o_not else 0
    author_names = sbotlite.get_names(link)
    first_author = author_names[0]
    co_authors = author_names[1:]
    metadata = sbotlite.extract_metadata(link)

    # get subject
    subject = sbotlite.get_bioarxiv_subject(link)
    row = {'FirstAuthor':first_author, 'CoAuthors':co_authors,'Label':label, 'RT':rt, 'Date':metadata[0],'Title':metadata[1],'Subject':subject[0]}
    return row

def save_sbotlite_logs(link):
    fn = '../results/logs.tsv'
    df = pd.read_csv(fn, sep='\t')
    row = get_info(link)
    df = df.append(row, ignore_index=True)
    df.to_csv(fn, index=False, sep='\t')
