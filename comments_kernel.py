import pandas as pd
import numpy as np
from keras.models import load_model
import pickle
import pathlib
from pathlib import Path


def to_str(spisok):
    return ', '.join(spisok)

def get_df(path_='mfd'):
    if path_=='mfd':
        mfd_saved_tokens_pkl = Path(pathlib.Path.cwd(), 'mfd_saved_tokens_pkl.pkl')
    if path_=='smartlab':
        mfd_saved_tokens_pkl = Path(pathlib.Path.cwd(), 'smartlab_saved_tokens_pkl.pkl')
    df = pd.read_pickle(mfd_saved_tokens_pkl)
    df.text = df['text'].apply(to_str)
    return df


def get_x_test(df):
    path_tfidf_model = Path(pathlib.Path.cwd(), 'nn_folder', 'FINAL_tfidf_model.pickle')
    path_svd = Path(pathlib.Path.cwd(), 'nn_folder', 'FINAL_svd.pickle')
    with open(path_tfidf_model, 'rb') as f:
        tfidf_model = pickle.load(f)
    with open(path_svd, 'rb') as z:
        svd = pickle.load(z)
    vectors_test = tfidf_model.transform(raw_documents=df.text).toarray()
    svd_test_vectors = svd.transform(vectors_test)
    svd_test_vectors = pd.DataFrame(svd_test_vectors, index=df.index,
                                    columns=['topic{}'.format(i) for i in range(30)])
    x_test = (svd_test_vectors.T / np.linalg.norm(svd_test_vectors, axis=1)).T
    x_test = np.array(x_test)
    x_test = np.asarray(x_test).reshape(len(x_test), 5, 6)
    return x_test


def get_y_pred(x_test, model):
    y_pred = model.predict(x_test)
    y_pred = [np.argmax(i) for i in y_pred]
    return y_pred


def get_comments_kernel():
    path_final_nn_model = Path(pathlib.Path.cwd(), 'nn_folder', 'FINAL_NN_MODEL.h5')
    loaded_model= load_model(path_final_nn_model)
    df = get_df(path_='mfd')
    x_test = get_x_test(df)
    y_pred = get_y_pred(x_test, loaded_model)
    df['m_comments_kernel'] = y_pred
    df1 = get_df(path_='smartlab')
    x_test1 = get_x_test(df1)
    y_pred1 = get_y_pred(x_test1, loaded_model)
    df1['s_comments_kernel_'] = y_pred1
    
    df['s_comments_kernel'] = df1['s_comments_kernel_']
    df_to_show = df[['m_comments_kernel', 's_comments_kernel']]
    df_to_show.to_pickle('kernel_file.pkl')
