import pandas as pd
import pathlib
from pathlib import Path

names=['author', 'text_initial', 'text_date', 'url']

from natasha import (Segmenter, NewsEmbedding, NewsMorphTagger, NewsSyntaxParser, Doc, MorphVocab)    
segmenter = Segmenter()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
morph_vocab = MorphVocab()
def get_tokenized_text_by_natasha(text_initial):
    try:
        tokenized_text = []
        doc = Doc(text_initial)
        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)
        doc.parse_syntax(syntax_parser)
        for token1 in doc.tokens:
            token1.lemmatize(morph_vocab)
            tokenized_text.append(token1.lemma)
        tokenized_text = [x for x in tokenized_text if x and x not in '- \t\n.,;:!?(—)«»<>„“…+..?…?/©']
        return tokenized_text
    except:
        return text_initial

def df_with_tokens_and_date(df_from_csv):
    df_temp = df_from_csv.copy()
    df_temp['tokenized_text'] = df_temp.text_initial.apply(get_tokenized_text_by_natasha)
    from collections import defaultdict
    dates = defaultdict(list)
    dates2 = defaultdict(str)
    for i in range(len(df_temp)):
        dates[df_temp.text_date.iloc[i]].extend(df_temp.tokenized_text.iloc[i])
        dates2[df_temp.text_date.iloc[i]] = dates2[df_temp.text_date.iloc[i]] + df_temp.text_initial.iloc[i]
    df_with_tokens = pd.DataFrame(index=pd.DatetimeIndex(dates.keys()), data=None)
    df_with_tokens['text'] = dates.values()
    df_with_tokens['text_initial'] = dates2.values()
    df_with_tokens.index.name = 'date'
    df_with_tokens.sort_index(inplace=True)
    days = df_with_tokens.index.to_series().dt.dayofweek
    df_with_tokens['days'] = days
    for i in range(2, len(df_with_tokens)):
        if df_with_tokens.days.iloc[i] == 5:
            df_with_tokens.text.iloc[i-1].extend(df_with_tokens.text.iloc[i])
        if df_with_tokens.days.iloc[i] == 6:
            df_with_tokens.text.iloc[i-2].extend(df_with_tokens.text.iloc[i])
    df_with_tokens = df_with_tokens[(df_with_tokens.days!=5)&(df_with_tokens.days!=6)]

    return df_with_tokens

def df_from_csv_and_dropna(path_for_token_eco , names):
    df = pd.read_csv(path_for_token_eco, names=names)
    df.dropna(inplace=True)
    return df

def rename_date(date):
    return str(date)[-4:] + '-' + str(date)[-7:-5] + '-' + str(date)[-10:-8]

def get_eco_with_tokens(path_for_token_eco):
    df_from_csv = df_from_csv_and_dropna(path_for_token_eco,names)
    df_from_csv.reset_index(drop=True, inplace=True)
    df_from_csv['text_date'] = df_from_csv['text_date'].apply(rename_date)
    df_with_tokens = df_with_tokens_and_date(df_from_csv)
    df_with_tokens.to_pickle(Path(pathlib.Path.cwd(), 'tokens_folder', 'eco_saved_tokens_pkl.pkl'))
    df_with_tokens.to_csv(Path(pathlib.Path.cwd(), 'tokens_folder', 'eco_saved_tokens.csv'))



    

    
### КОД ДЛЯ collab ###
    
def df_from_csv_and_dropna_collab(path, names):
    df_collab = pd.read_csv(path, names=names)
    df_collab.dropna(inplace=True)
    return df_collab

def get_collab_with_tokens(collab_file_name):
    df_from_csv_col = df_from_csv_and_dropna_collab(collab_file_name,names)
    df_from_csv_col.reset_index(drop=True, inplace=True)
    
    df_with_tokens_col = df_with_tokens_and_date(df_from_csv_col)
    df_with_tokens_col.to_pickle(Path(pathlib.Path.cwd(), 'tokens_folder', 'collab_saved_tokens_pkl.pkl'))
    df_with_tokens_col.to_csv(Path(pathlib.Path.cwd(), 'tokens_folder', 'collab_saved_tokens.csv'))    