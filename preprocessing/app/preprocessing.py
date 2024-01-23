import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
import pickle

class DataProcessor:
    def __init__(self, data):
        self.df = data
        self.var_categorical = []
        self.var_numerical = []
        self.var_datetime = []


    def replacer(self,currency):
        code = ["DZD","DA","AOA","KZ","XOF","BWP","P","BIF","FBu","XOF","CFA",'EGP',"E£","CDF","FC","DJF",",",
            "Fdj","XAF","FCFA","CVE","$","KMF","CF","XOF","CFA","ERN","Nkf","ETB","Br","XAF","FCFA","GMD","D","GHS",
            "GH₵","LYD","LD","MGA","Ar","MWK","K","LRD","L$","LD$","GWP","CFA","GNF","FG","KES","KSh","LSL","L","M","XOF",
            "CFA","MRO","MUR","Rs","MAD","DH","MZN","MT","NAD","$", "N$","NGN","N","ZWD","K","SLL","Sl","SOS","Sh","SCR",
            "SR","STD","Db","RWF","FRw","RF","R₣","SSP","SS£","SDG","SZL","ZAR","R","TZS","TSh","TND","DT","ZMW","K","UGX","USh"]
        code = [i.lower() for i in code]
        actual = currency
        currency = str(currency).replace(",","")
        currency = currency.lower()
        for i in code:
            try:
                if currency.__contains__(i):            
                    currency = currency.replace(i,"")
                    currency = float(currency)
            except:
                pass   
        if type(currency) == float:
            return currency
        else:
            return actual
        
    def clean_and_encode(self):
        self.df.replace(["Unknown", "unknown", "None", "none", "Null", "null", "_", "-", "N/A", "NA", "Not Available"], np.NaN, inplace=True)

        for i in list(self.df.columns):
            if self.df[i].isnull().sum()/len(self.df) >= 0.80:
                self.df.drop(i, axis=1, inplace = True)  


        for column in self.df:
            if self.df[column].dtypes == 'object':
                try:
                    self.df[column] = self.df[column].map(self.replacer).astype(float)
                except:
                    pass

                if self.df[column].dtypes == 'object':
                    try:
                        pd.to_datetime(self.df[column])
                        self.var_datetime.append(column)
                        self.df[column] = pd.to_datetime(self.df[column])
                    except:
                        self.var_categorical.append(column)
                        pass

            elif pd.api.types.is_integer_dtype(self.df[column]) or pd.api.types.is_float_dtype(self.df[column]):
                 self.var_numerical.append(column)

            elif self.df[column].dtypes == 'datetime64[ns]':
                    self.var_datetime.append(column)

            for i in list(self.df[self.var_numerical]):
                median_value = self.df[i].median()
                self.df[i].fillna(median_value, inplace=True)

            for i in list(self.var_categorical):
                self.df[i] = self.df[i].fillna(method='ffill')

            for i in list(self.var_datetime):
                self.df[i] = self.df[i].fillna(method='ffill')


        self.df.drop_duplicates(inplace=True)

        # Encode the categorical columns
        one_hot_dfs = []
        for column in self.var_categorical:
            enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
            one_hot_encoded = enc.fit_transform(self.df[[column]])
            pickled = pickle.dumps(enc)
            feature_names = enc.get_feature_names_out([column])
            one_hot_df = pd.DataFrame(one_hot_encoded, columns=feature_names)
            one_hot_dfs.append(one_hot_df)

        # Concatenate all the one-hot encoded DataFrames
        one_hot_encoded_df = pd.concat(one_hot_dfs, axis=1)

        # Combine the numerical columns and the one-hot encoded columns
        result_df = pd.concat([self.df[self.var_numerical], one_hot_encoded_df], axis=1)

        return result_df, pickled