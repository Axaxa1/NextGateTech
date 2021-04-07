import pandas as pd
import numpy as np


def test_no_nan(data):
    """
    Simply check if data contains any NAN
    :param data: DataFrame
    :return: bool
    """
    return data.isnull().any() == False


def reshape_nav_data(data):
    """
    Reshape the DataFrame with Valuation_Date as index and NAV_Per_Share as columns
    :param data: DataFrame containing Valuation_Data and NAV_Per_Share
    :return: DataFrame
    """
    # Select a subset of the DataFrame
    sub_data = data[["Valuation_Date", "NAV_Per_Share"]]

    # Reset the index
    sub_data = sub_data.reset_index()

    # 1-Add Asset name as a columns
    name = []
    for i in range(len(sub_data[["Subfund_Code", "Share_Class_Code"]])):
        name.append(str(sub_data.iloc[i]["Subfund_Code"]) + str(sub_data.iloc[i]["Share_Class_Code"]))
    new_names = pd.Series(name, index=sub_data.index, name="Asset")
    sub_data = pd.concat((sub_data, new_names), axis=1)
    sub_data = sub_data.drop(["Subfund_Code", "Share_Class_Code"], axis=1)

    # 2-Create a new DataFrame with desired shape
    res = pd.DataFrame()
    for asset in sub_data["Asset"].unique():
        serie = sub_data.loc[sub_data["Asset"] == asset][["NAV_Per_Share", "Valuation_Date"]]
        pd_serie = pd.DataFrame(serie, columns=["NAV_Per_Share", "Valuation_Date"])
        pd_serie = pd_serie.set_index(["Valuation_Date"])
        pd_serie = pd_serie.rename(columns={"NAV_Per_Share": "NAV_Per_Share_" + asset})
        res = pd.concat((res, pd_serie), axis=1)

    return res


def compute_correlations(data):
    """
    Simply return correlation between assets
    :param data: DataFrame of RESHAPED data
    :return: DataFrame
    """
    # Correlations should be calculated on returns
    returns = data.pct_change()
    return returns.corr()
