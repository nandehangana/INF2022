import pandas as pd
from app import main
from flask import jsonify, request, Response
from flask_cors import CORS
from app.dataframes import df_Index_Constituents, df_FTSEJSE_Index_Series, df_Industry_Classification_Benchmark, df_BA_Beta_Output

app = main.app

CORS(app, resources={r"/*":{'origins':"*"}})

@app.route('/api/index')
def getIndex():
    query_params = request.args
    index_name = query_params.get("indexName")
    date = query_params.get("date")

    return df_Index_Constituents.to_json(orient='records')

