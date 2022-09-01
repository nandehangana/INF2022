'''
    Author: Kenneth Ssekimpi
'''
from app.main import frames_dict
import pandas as pd

# Retrieving all the necessary dataframes from the dictionary to work with downstream
df_BA_Beta_Output = pd.DataFrame(frames_dict['tbl_BA_Beta_Output'])
df_Beta_Output = pd.DataFrame(frames_dict['tbl_Beta_Output'])
df_EOD_Equity_Data = pd.DataFrame(frames_dict['tbl_EOD_Equity_Data'])
df_EOD_Interest_Rate_Data = pd.DataFrame(frames_dict['tbl_EOD_Interest_Rate_Data'])
df_FTSEJSE_Index_Series = pd.DataFrame(frames_dict['tbl_FTSEJSE_Index_Series'])
df_Index_Constituents = pd.DataFrame(frames_dict['tbl_Index_Constituents'])
df_Industry_Classification_Benchmark = pd.DataFrame(frames_dict['tbl_Industry_Classification_Benchmark'])

from app import indices, sectors, shares, weights_and_ics
