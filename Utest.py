import unittest
import predict_numeric as pn
import news
import pandas as pd
import numpy as np
import json
import portfol_funcs as pf

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.test_data = pd.read_csv('csv_files/TEST.csv')
        self.test_data_news = pd.read_csv('csv_files/TEST_NEWS.csv')
        self.test_data_bal = pd.read_csv('csv_files/TEST_BAL.csv')
        self.test_data_in = pd.read_csv('csv_files/TEST_IN.csv')
        self.test_df = pd.read_csv('csv_files/TEST_FUNCS.csv')
        self.test_rsi = pd.read_csv('csv_files/TEST_RSI.csv')

        with open('json_files/TEST_NEWS.json', 'r') as f:
            self.test_news =  json.load(f)
        
        with open('json_files/TEST_NEWS_TO_DICT.json', 'r') as f:
            self.test_news_to_dict =  json.load(f)

        with open('json_files/TEST_NEWS_SCORES.json', 'r') as f:
            self.test_news_scores =  json.load(f)

        with open('json_files/TEST_NEWS_TOPS.json', 'r') as f:
            self.test_news_tops =  json.load(f)      

    def test_EMA_difference(self):
        self.assertEqual(pn.calculate_EMA_difference(np.array(self.test_data["EMA_Short"]),np.array(self.test_data["EMA_Long"])).all(), np.array(self.test_df['EMA_DIFF']).all())

    def test_Plus_min(self):
        self.assertEqual(pn.calculate_Puls_min(np.array(self.test_data['Weekly_Price'])).all(), np.array(self.test_df['Plus_Min']).all())
    
    def test_News_to_dict(self):
        news_to_dict = news.news_to_dict(self.test_news)
        self.assertIsInstance(news_to_dict, dict, "did not return a dict")
    
    """ def between(num):s
        return true if between 0 - 1

    def test_predictions(self):
        acc , predict = pn.predict(self.test_data,self.test_df['Plus_Min'])
        tf_acc, tf_pred = tf.tensor_main(self.test_data,self.test_df['Plus_Min'])
        self.assertTrue(self.between(acc))
        self.assertTrue(self.between(tf_acc)) """

    def test_News_scores(self):
        # news scores test
        news_scores = news.score(self.test_news)
        self.assertIsInstance(news_scores, dict,"scores are not the correct type")

        # news tops test
        news_tops = news.tops(self.test_news_scores,5)
        self.assertIsInstance(news_tops, tuple,"tops is not the correct type")

    def test_portfolio_functions(self):
        test_port = {'AAPL':2.0, 'AAPF':3.10, 'SPLK':1.0}
        test_port_copy = test_port.copy()

        test_inputs = ['VZ:s', 'VZ:b','VZ:B;AAPL: s;AapF :S;KO:B','VZ:h']

        clean = pf.clean_user_input_portfolio(test_inputs[0])
        #self.assertIsInstance(clean,dict,'clean did not return a dictionary')
        self.assertEqual(clean,{'VZ':'s'}, "ERROR: small split failed")

        clean = pf.clean_user_input_portfolio(test_inputs[2])
        self.assertEquals(clean,{'VZ':'b','AAPL':'s','AAPF':'s','KO':'b'}, "ERROR: large clean failed")

        updated_port = pf.update_port(self.test_news_scores,test_port,test_inputs[0])
        #self.assertIsInstance(updated_port,dict,'updated port did not return a dictionary')
        self.assertEqual(updated_port,test_port_copy,"ERROR: selling ticker thats not in port changed port")

        updated_port = pf.update_port(self.test_news_scores,test_port,test_inputs[2])
        del test_port_copy['AAPL']
        del test_port_copy['AAPF']
        if 'VZ' in self.test_news_scores:
            test_port_copy['VZ'] = self.test_news_scores['VZ']
        else:
            test_port_copy['VZ'] = None
        if 'KO' in self.test_news_scores:
            test_port_copy['KO'] = self.test_news_scores['KO']
        else:
            test_port_copy['KO'] = None
        self.assertEqual(updated_port,test_port_copy,"ERROR: big update failed")
                    

if __name__ == '__main__':
    unittest.main()