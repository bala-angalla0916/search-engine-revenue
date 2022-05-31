import pandas as pd
import sys
import os
from datetime import datetime

## Reference field names to validate log file
field_names = ['hit_time_gmt', 'date_time', 'user_agent', 'ip', 'event_list', 'geo_city', 'geo_region', 'geo_country', 'pagename', 'page_url', 'product_list', 'referrer']

class SearchEngineRevenue():
    def __init__(self, logfile):
       self.logfile = logfile

    def get_date(self):
        exec_date = datetime.today().strftime('%Y-%m-%d')        
        return exec_date

       
    def validate_file(self):
        res = os.path.exists(self.logfile)
        if res is True:            
            print("File Exists")
        else:
            print("File doesn't exists")
            exit
            
    
    def validate_fields(self):
        df = pd.read_csv(self.logfile , sep='\t')
        header_rec_file = df.columns.values.tolist()
        header_rec = set(header_rec_file)
        ref_fields = set(field_names)
        if header_rec == ref_fields:
            print("Tab file have required field names")
        else:
            print("Tab file doesn't have required field names! Please check tab file")
            exit
    
    def read_file(self):
        self.validate_file() 
        self.validate_fields() 
        df = pd.read_csv(self.logfile, sep='\t')
        return df

    def get_domain(self, df):
        df = self.read_file()
        res = df[df['referrer'].str.contains('search?', regex=False)]
        for index, row in  res.iterrows():        
            token=row['referrer'].split('http://')[1].split('/')[0]
            Search_Engine_Domain=token.split('.')[-2]+'.'+token.split('.')[-1]
            res.loc[index,'Search_Engine_Domain'] = Search_Engine_Domain        
        domain_df = res[['ip','Search_Engine_Domain']]
        return domain_df
    
    def load_tab_file(self, df):
        exec_date = self.get_date()        
        file_nm = f'{exec_date}_SearchKeywordPerformance.tab'
        df.to_csv(file_nm, sep='\t', index=False)
    
    def get_revenue(self):
        log_df = self.read_file()
        domain_df = self.get_domain(log_df)        
        rev_df = log_df[log_df['pagename'].str.contains("order complete", case=False)]

        for index, row in rev_df.iterrows():
            prod = row['product_list'].split(';')[1].split('-')[0]
            revenue = row['product_list'].split(';')[3]            
            rev_df.loc[index,'Search_Keyword'] = prod
            rev_df.loc[index,'Revenue'] = revenue

        merge_df = pd.merge(rev_df, domain_df, on='ip', how='left')
        final_df = merge_df[['Search_Engine_Domain', 'Search_Keyword', 'Revenue']].sort_values(by=['Revenue'], ascending=False)
        self.load_tab_file(final_df)    


