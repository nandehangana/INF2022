'''
    Author: Daiyaan Salie
    
'''
import numpy as np
import pandas as pd
from app.dataframes import df_BA_Beta_Output, df_Index_Constituents
from app.weights_and_ics import getICsAndWeights

tbl_BA_Beta_Output = df_BA_Beta_Output
tbl_Index_Constituents = df_Index_Constituents

def getBetasMktAndSpecVols(rDate, ICs, tbl_BA_Beta_Output, mktIndexCode):
    '''
        What function does:
            This function takes in 

        Args:
            table (str): dbo.tbl BA Beta Output.
            datetime (date): rDate.
            string (str): ICs.
            string (str): mktIndexCode.

        Returns:
    

        # Add a section detailing what errors might be raised
        Raises:
    
    '''

    #rDate will be supplied by the user: consisting of year and Quarter 
    rDate = pd.to_datetime(rDate, format = "%Y-%m")
    rDate_Month = rDate.month
    rDate_Year = rDate.year

    #search tbl_Index_Constituents Date column and find Quarter and Year for each date in column
    Dates_Col = tbl_BA_Beta_Output["Date"]
    Dates_Col = pd.arrays.DatetimeArray(Dates_Col)
    Dates_Col_Month = Dates_Col.month
    Dates_Col_Year = Dates_Col.year

    #Filter tbl_BA_Beta_Output using supplied quarter and year data from rData
    tbl_BA_Beta_Output_Date = tbl_BA_Beta_Output.loc[(Dates_Col_Month == rDate_Month) & (Dates_Col_Year == rDate_Year),]

    #Market index code provided by the user which could be "J203", "J200", "J250", "J257" or "J258"
    mktIndexCode = mktIndexCode

    #Filter tbl_BA_Beta_Output_Dates using provided mktIndexCode
    tbl_BA_Beta_Output_mktIndex = tbl_BA_Beta_Output_Date.loc[tbl_BA_Beta_Output_Date["Index"] == mktIndexCode]


    #list of IndexCodes obtain from  the Alpha column in the Output of Function 1.
    ICs = ICs
    tbl_BA_Beta_Output_IC = tbl_BA_Beta_Output_mktIndex.loc[tbl_BA_Beta_Output_mktIndex["Instrument"].isin(ICs)]

    mktVol_row = tbl_BA_Beta_Output_mktIndex.loc[tbl_BA_Beta_Output_mktIndex["Instrument"] == mktIndexCode]


    #Generate results table with Shares and corresponding share weights
    Betas = tbl_BA_Beta_Output_IC.loc[:,"Beta"]
    specVols = tbl_BA_Beta_Output_IC.loc[:,"Unique Risk"]
    mktVol = mktVol_row.loc[:,"Total Risk"]
    Results = pd.concat([Betas.reset_index(drop=True), specVols.reset_index(drop=True),mktVol.reset_index(drop=True)],axis=1)
    Results.columns = ['Betas','specVols','mktVol']

    return Results


Quarter_month = {1:3, 2:6, 3:9, 4:12}

#inputs provided from user 
rDate_year = '2019' #Get year from user
rDate_quarter = 2 #get quarter from user
rDate_month = str(Quarter_month[rDate_quarter])
rDate = rDate_year +"-"+ rDate_month #Create single date value from supplied year and quarter

IndexCode = "TOPI" 
Output1 = getICsAndWeights(rDate,IndexCode,tbl_Index_Constituents)
ICs = Output1['Alpha']
mktIndexCode = "J203"

Output2 = getBetasMktAndSpecVols(rDate,ICs,tbl_BA_Beta_Output,mktIndexCode)

