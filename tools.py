import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import firebase_admin
from firebase_admin import credentials, firestore
from data import test_no_nan, compute_correlations


def create_data(path):
    """
    Read CSV exemple file
    :param path: str to CSV training file
    :return: DataFrame
    """
    try:
        d = pd.read_csv(path, index_col=["Subfund_Code", "Share_Class_Code"])
    except FileNotFoundError:
        raise FileNotFoundError("Data should are not here : {} !".format(path))

    # Drop useless columns
    d = d.drop(["Subfund_Long_Name", "Dividend_PCCY"], axis=1)
    return d


def connect_firebase(private_key):
    """
    Connect to remote firebase
    :param private_key: json file containing the private key
    :return: firestore client
    """
    cred = credentials.Certificate(private_key)
    firebase_admin.initialize_app(cred)
    return firestore.client()


def read_firebase(datab):
    """
    Print all documents for collections tests and correlations
    :param datab: firestore client
    :return: None
    """
    testsref = datab.collection(u'tests')
    docs = testsref.stream()
    for doc in docs:
        print('{} : {}'.format(doc.id, doc.to_dict()))
    correlationsref = datab.collection(u'correlations')
    docs = correlationsref.stream()
    for doc in docs:
        print('{} : {}'.format(doc.id, doc.to_dict()))


def update_test(data, datab):
    """
    Write tests results in the firebase
    :param data: DataFrame of data
    :param datab: Firestore client
    :return: None
    """
    # Test collection ref
    testsref = datab.collection(u'tests')

    # -- Update no_nan_test
    # Get document ref
    no_nan_ref = datab.collection(u'tests').document(u'no_nan')
    # Run test
    t = test_no_nan(data)
    # Adapt the structure
    no_nan_test = {}
    for i in range(len(t)):
        no_nan_test[t.index[i]] = bool(t.iloc[i])
    # Write in the data base
    no_nan_ref.set(no_nan_test)


def update_correlations(nav_data, datab):
    """
    Write correlation in the firebase
    :param nav_data: RESHAPED Nav series
    :param datab: firestore client
    :return: None
    """
    # Test collection ref
    corr = compute_correlations(nav_data)
    for col in corr.columns:
        corr_ref = datab.collection(u'correlations').document(col)
        corr_data = {}
        for col2 in corr.columns:
            corr_data[col2] = corr[col][col2]
        corr_ref.set(corr_data)

