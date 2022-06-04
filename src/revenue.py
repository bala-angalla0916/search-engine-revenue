import pandas as pd
import os
from datetime import datetime
import logging
pd.set_option('mode.chained_assignment', None)
## Reference field names to validate log file
field_names = ['hit_time_gmt', 'date_time', 'user_agent', 'ip', 'event_list', 'geo_city', 'geo_region', 'geo_country', 'pagename', 'page_url', 'product_list', 'referrer']

## Search Engine Revenue class to identify revenue and publish to S3 bucket based on hit file from S3 Event
class SearchEngineRevenue():
    def __init__(self, df):
       self.df = df

    def get_date(self):
        exec_date = datetime.today().strftime('%Y-%m-%d')        
        return exec_date
       
    def validate_df(self):
        if self.df.empty:            
            return "DataFrame is empty!"
            exit      
        else:            
            return "DataFrame is Valid"
            
                
    def validate_fields(self):  
        print(self.df.head())      
        header_rec_file = self.df.columns.values.tolist()
        header_rec = set(header_rec_file)
        ref_fields = set(field_names)
        if header_rec == ref_fields:            
            return "Tab file have required field names"
        else:            
            return "Tab file doesn't have required field names! Please check tab file"
            exit
    
    def validate_input(self):
        self.validate_df() 
        self.validate_fields() 
        

    def get_domain(self):
        self.validate_input()
        df=self.df
        res = df[df['referrer'].str.contains('search?', regex=False)]
        for index, row in  res.iterrows():        
            token=row['referrer'].split('http://')[1].split('/')[0]
            Search_Engine_Domain=token.split('.')[-2]+'.'+token.split('.')[-1]
            res.loc[index,'Search_Engine_Domain'] = Search_Engine_Domain        
        domain_df = res[['ip','Search_Engine_Domain']]      
        logging.info("Search Engine domain identified!")  
        return domain_df    
    
    
    def get_revenue(self):        
        domain_df = self.get_domain()        
        rev_df = self.df[self.df['pagename'].str.contains("order complete", case=False)]

        for index, row in rev_df.iterrows():
            prod = row['product_list'].split(';')[1].split('-')[0]
            revenue = row['product_list'].split(';')[3]            
            rev_df.loc[index,'Search_Keyword'] = prod
            rev_df.loc[index,'Revenue'] = revenue

        merge_df = pd.merge(rev_df, domain_df, on='ip', how='left')
        final_df = merge_df[['Search_Engine_Domain', 'Search_Keyword', 'Revenue']].sort_values(by=['Revenue'], ascending=False)
        logging.info("Revenue identified!")
        return final_df

    def publish_revenue(self):
        final_df = self.get_revenue(self)
        exec_date = self.get_date()        
        file_nm = f's3://search-engine-revenue-output/{exec_date}_SearchKeywordPerformance.tab'
        final_df.to_csv(file_nm, sep='\t', index=False)
        logging.info("Revenue file pusblished to S3 Output Bucket")


