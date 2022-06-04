import sys, os
import pytest
import pandas as pd
from datetime import datetime
from unittest.mock import MagicMock, patch, PropertyMock
from src import revenue
from src.revenue import SearchEngineRevenue

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..","..",'src'))

test_data = os.path.abspath(os.path.dirname(__file__) + '../../test')
test_file=os.path.join(test_data, 'test_data.tsv')

class TestRevenue():
    @pytest.fixture
    def odate(self):
        return datetime.today().strftime('%Y-%m-%d')

    
    @pytest.fixture
    def test_df(self):        
        df = pd.read_csv(test_file, sep='\t')
        print(df.head())
        return df

    @pytest.fixture
    def fields_list(self):        
        data = pd.read_csv(test_file, sep='\t')
        return data.columns.values.tolist()
    
    @pytest.fixture
    def mock(self):
        return MagicMock()


    def test_get_date(self, test_df, odate):
        eDate = SearchEngineRevenue(test_df).get_date()
        assert eDate and odate

    def test_validate_df(self, test_df):
        res = SearchEngineRevenue(test_df).validate_df()       
        ref = "DataFrame is Valid"
        assert res and ref

    def test_validate_fields(self, test_df):
        res = SearchEngineRevenue(test_df).validate_fields()
        ref = "Tab file have required field names"
        assert res and ref

    def test_get_domain(self, test_df):
        res = SearchEngineRevenue(test_df).get_domain()
        ref = ['ip', 'Search_Engine_Domain']
        flist = res.columns.values.tolist()
        assert ref and flist

    def test_get_revenue(self, test_df):
        res = SearchEngineRevenue(test_df).get_revenue()
        ref = ['Search_Engine_Domain', 'Search_Keyword', 'Revenue']
        assert ref and res.columns.values.tolist()

    




