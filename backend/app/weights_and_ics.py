'''
    Author: Daiyaan Salie   
     
'''
import numpy as np
import pandas as pd
from app.dataframes import df_Index_Constituents

from app import main
from flask import request, render_template, Response
from flask_cors import CORS
import json

app = main.app

CORS(app, resources={r"/*":{'origins':"*"}})

tbl_Index_Constituents = df_Index_Constituents

def getICsAndWeights(rDate,IndexCode,tbl_Index_Constituents):
    '''
        What function does:
            The function retrieves the date(year and quarter) as well as index-code which returns the weights and alphas for the 
            shares on that index for that specific quarter.

        Args:
            table (str): dbo.tbl_Index_Constituents.
            datetime (date): rDate - Year and Quarter
            string (str): indexCode.            

        Returns:
            The function returns a column called "weights" and a column called "Alphas" for the filtered shares as well as the gross market cap
            for each share as well as the ICB sub-sector to which each share belongs.
        # Add a section detailing what errors might be raised
        Raises:
    
    '''
    #rDate will be supplied by the user: consisting of year and Quarter 
    rDate = pd.to_datetime(rDate, format = "%Y-%m")
    rDate_Month = rDate.month
    rDate_Year = rDate.year

    #search tbl_Index_Constituents Date column and find Quarter and Year for each date in column
    Dates_Col = tbl_Index_Constituents["Date"]
    Dates_Col = pd.arrays.DatetimeArray(Dates_Col)
    Dates_Col_Month = Dates_Col.month
    Dates_Col_Year = Dates_Col.year

    #Filter tbl_Index_Constituents using supplied quarter and year data from rData
    tbl_Index_Constituents_Date = tbl_Index_Constituents.loc[(Dates_Col_Month == rDate_Month) & (Dates_Col_Year == rDate_Year),]


    #IndexCode is provided by user: "ALSI", "FLED", "LRGC", "MIDC", "SMLC", "TOPI", "RESI", "FINI", "INDI", "PCAP", "SAPY" or "ALTI"
    IndexCode = IndexCode 

    #function to identify The index column that must be searched
    def Index_Col_Identifier(argument):
        match argument:
            case "FLED":
                return "ALSI New"
            case  "LRGG"|"MIDC"|"SMILC":
                return "Index New"
            case default:
                return argument+" New"
    
    IndexCode_Col = Index_Col_Identifier(IndexCode) #Obtain column name to search relevant rows

    #Filter tbl_Index_Constituents_Date using supplied IndexCode in the column identified from Index_Col_Identifier function
    tbl_Index_Constituents_final = tbl_Index_Constituents_Date[tbl_Index_Constituents_Date[IndexCode_Col] == IndexCode]

    #Generate results table with Shares and corresponding share weights
    Alpha = pd.DataFrame(tbl_Index_Constituents_final.loc[:,"Alpha"])
    Gross_Market_Capitalisation = np.array(tbl_Index_Constituents_final.loc[:,"Gross Market Capitalisation"])
    Weigths = pd.DataFrame(Gross_Market_Capitalisation/np.sum(Gross_Market_Capitalisation))
    Gross_Market_Capitalisation = pd.DataFrame(Gross_Market_Capitalisation)
    ICB_SubSector = pd.DataFrame(tbl_Index_Constituents_final.loc[:,"ICB Sub-Sector"]) #
    Results = pd.concat([ Alpha.reset_index(drop=True),Weigths.reset_index(drop=True),Gross_Market_Capitalisation.reset_index(drop=True),ICB_SubSector.reset_index(drop=True)],axis=1)
    Results.columns = ['Alpha','Weights','Gross Market Capitalisation','ICB Sub-Sector']

    return Results

Quarter_month = {1:3, 2:6, 3:9, 4:12}

rDate_year = '2019' #Get year from user
rDate_quarter = 2 #get quarter from user
rDate_month = str(Quarter_month[rDate_quarter])
rDate = rDate_year +"-"+ rDate_month #Create single date value from supplied year and quarter

IndexCode = "TOPI" #Get input from user
Output1 = getICsAndWeights(rDate,IndexCode,tbl_Index_Constituents)


print(Output1)

@app.route('/weights')
def get_weights():
    return(Output1.to_json(orient='records'))