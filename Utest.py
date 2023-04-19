import unittest
import predict_numeric as pn
import tensorFinance as tf
import news
import pandas as pd
import numpy as np
import json

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
        self.assertEquals(type(news_to_dict), dict)
    
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
        self.assertEquals(type(news_scores), dict)

        # news tops test
        news_tops = news.tops(self.test_news_scores,5)
        self.assertEquals(type(news_tops), tuple)


    
    



if __name__ == '__main__':
    unittest.main()