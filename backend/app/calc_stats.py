'''
    Author: Daiyaan Salie
    
'''
import numpy as np
import pandas as pd
from app.weights_and_ics import getICsAndWeights
from app.betas_mkt_spec_vols import getBetasMktAndSpecVols, tbl_BA_Beta_Output


output1 = getICsAndWeights("2020-01-01","ALSI","tbl_Index_Constituents")
ICs = output1["Alpha"]
mktIndexCode = "J203"
output2 = getBetasMktAndSpecVols("2020-01-01",ICs,tbl_BA_Beta_Output,mktIndexCode)


weights = np.transpose(np.matrix(output1["Weights"]))
betas = np.transpose(np.matrix(output2["Betas"]))
specVols = np.transpose(np.matrix(output2["specVols"]))
mktVol = output2["mktVol"][0]


def CalcStats(weights,betas,specVols,mktVol):
    '''
        Write what function does:
            

        Args:
            (numeric): weights;
            (numeric): betas;
            (numeric): mktVol; and
            (numeric): specVols.
            

        Returns:
            pfBeta - portfolio beta;
            sysCov - systematic covariance matrix;
            pfSysVol - portfolio systematic volatility;
            specCov - specific covariance matrix;
            pfSpecVol - portfolio specific volatility;
            totCov - total covariance matrix;
            pfVol - portfolio total volatility; and
            CorrMat - correlation matrix.

        # Add a section detailing what errors might be raised
        Raises:
    
    '''
    pfBeta = round(np.matmul(np.transpose(weights),betas),3)

    sysCov = np.matmul(betas,np.transpose(betas))*(mktVol**2)

    pfSysVol = np.transpose(weights)@betas@np.transpose(betas)@weights*(mktVol**2)

    specCov = np.diagflat(specVols)@np.diagflat(specVols)

    pfSpecVol = np.transpose(weights)@(specCov)@weights

    totCov = sysCov + specCov

    pfVol = pfSysVol + pfSpecVol

    d = np.diagflat(np.matrix(np.diag(totCov)))
    
    corrMat = (np.linalg.inv(d)@(sysCov+specCov))@np.linalg.inv(d)

    Output = {"pfBeta" : pfBeta, "sysCov" : sysCov, "pfSysVol" : pfSysVol, "specCov" : specCov, "pfSpecVol" : pfSpecVol, "totCov" : totCov, "pfVol" : pfVol, "corrMat": CorrMat}
    
    return (Output)