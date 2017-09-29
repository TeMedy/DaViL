'''
Created on Aug 30, 2017

@author: Hossein
'''
import unittest
import json
import os 
import utils
import analytics
from time import gmtime, strftime
import scraping


class TestScrapingMethods(unittest.TestCase):
  '''
  Test the methods used to collect data from the web, save into and load from files. 
  '''
  #@unittest.skip("")
  def test_get_team_members(self):
    team_members = scraping.get_team_members()
    found_Johanna = False
    for d in team_members: 
      if d['name'] == 'Johanna Nicoletta': 
        found_Johanna = True
    self.assertEqual(found_Johanna, True, "The AJAX call was not successful!")
    
  #@unittest.skip("")
  def test_save_and_load(self):
    team_members = scraping.get_team_members()
    team_data = {'date': team_members}
    # save data to file 
    data_file_name = '../data/test/web_data_json_test.data'

    utils.save_to_file(data_file_name, team_data)    
    #
    # test loading from the file and if the name of Johanna can be found
    #
    member_data = utils.load_from_file(data_file_name)
    a_day_data = {}
    # take the first item in the dictionary; doesn'e matter which one it is
    for key in member_data: 
      a_day_data = member_data[key]
      break
    found_Johanna = False
    for d in a_day_data: 
      if d['name'] == 'Johanna Nicoletta': 
        found_Johanna = True
    self.assertEqual(found_Johanna, True, "Can not save or load from file")
    
  #@unittest.skip("")
  def test_update_ledger(self):
    test_ledger = {'2017-09-01': [{'name': 'Johanna', 'amount': '345$'}, {'name':"Hossein", 'amount': '22$'}], 
                   '2017-09-02': [{'name': 'Johanna', 'amount': '355$'}, {'name':"Hossein", 'amount': '23$'}]}
    new_data = [{'name': 'Johanna', 'amount': '355$'}, {'name':"Hossein", 'amount': '23$'}, {'name':"Ron", 'amount': '100$'}]
    scraping.update_ledger(test_ledger, new_data)
    today_date = strftime("%Y-%m-%d", gmtime())
    self.assertEqual(today_date in test_ledger, True, "The data has not been added to the ledger")
    # test updating
    update_data = [{'name': 'Johanna', 'amount': '355$'}, {'name':"Hossein", 'amount': '50$'}]
    scraping.update_ledger(test_ledger, update_data, '2017-09-01')
    self.assertEqual(test_ledger['2017-09-01'][1]['amount'] == '50$', True, "Ledger is not updated.")
    #
    #main.update_ledger(['list', 'of', 'some string'], 'something', '20170901')
    
  #@unittest.skip("")
  def test_pars_member_page(self):
    # get a page
    # url for Johanna's page 
    p_url = "https://secure.e2rm.com/registrant/FundraisingPage.aspx?registrationID=3697209&langPref=en-CA&Referrer=https%3a%2f%2fsecure.e2rm.com%2fregistrant%2fsearch.aspx%3feventid%3d210107%26langpref%3den-CA"
    raw_html = scraping.get_member_page(p_url)
    #print("Parsing the page ...")
    parsed_page = scraping.parse_member_page(raw_html)
    #print(json.dumps(parsed_page, indent=4))
    # find 'ericssoncommunity'
    found_ericssoncommunity = False
    for item in parsed_page: 
      if item['supporter_name'] == 'ericssoncommunity':
        if item['amount_dollar'] == '27.38':
          found_ericssoncommunity = True
    self.assertEqual(found_ericssoncommunity, True, "Could not pars the page.")
    #print(parsed_page)
        
        
class TestDataAnalytics(unittest.TestCase):
  #@unittest.skip("")
  def test_get_highest_donation(self):
    supporters_data = {'2017-09-08': {'Johanna Nicoletta': [{'supporter_name': 'ericssoncommunity', 'message': '', 'amount_dollar': '229.41', 'time': 'Jul 19, 2017 12:00 AM'}, {'supporter_name': 'ericssoncommunity', 'message': '', 'amount_dollar': '27.38', 'time': 'May 12, 2017 12:00 AM'}, {'supporter_name': 'Anonymous Donor', 'message': '', 'amount_dollar': '250.00', 'time': 'May 1, 2017 8:45 AM'}], 'Ericsson Activities': [{'supporter_name': 'Foosball Champion', 'message': '', 'amount_dollar': '78.00', 'time': 'Aug 30, 2017 9:35 PM'}, {'supporter_name': 'Bottle Drive -- Aug 8', 'message': '', 'amount_dollar': '194.00', 'time': 'Aug 9, 2017 10:07 AM'}], 'Hossein Seyedmehdi': [], 'Alireza Mirzaee': [{'supporter_name': 'Hossein', 'message': '', 'amount_dollar': '25.00', 'time': 'Aug 9, 2017 10:18 AM'}]}, '2017-09-05': {'Johanna Nicoletta': [{'supporter_name': 'ericssoncommunity', 'message': '', 'amount_dollar': '27.38', 'time': 'May 12, 2017 12:00 AM'}, {'supporter_name': 'Anonymous Donor', 'message': '', 'amount_dollar': '250.00', 'time': 'May 1, 2017 8:45 AM'}], 'Ericsson Activities': [{'supporter_name': 'Foosball Champion', 'message': '', 'amount_dollar': '78.00', 'time': 'Aug 30, 2017 9:35 PM'}, {'supporter_name': 'Bottle Drive -- Aug 8', 'message': '', 'amount_dollar': '194.00', 'time': 'Aug 9, 2017 10:07 AM'}], 'Hossein Seyedmehdi': [], 'Alireza Mirzaee': [{'supporter_name': 'Hossein', 'message': '', 'amount_dollar': '25.00', 'time': 'Aug 9, 2017 10:18 AM'}]}, '2017-09-09': {'Johanna Nicoletta': [{'supporter_name': 'ericssoncommunity', 'message': '', 'amount_dollar': '229.41', 'time': 'Jul 19, 2017 12:00 AM'}, {'supporter_name': 'ericssoncommunity', 'message': '', 'amount_dollar': '27.38', 'time': 'May 12, 2017 12:00 AM'}, {'supporter_name': 'Anonymous Donor', 'message': '', 'amount_dollar': '250.00', 'time': 'May 1, 2017 8:45 AM'}], 'Ericsson Activities': [{'supporter_name': 'Foosball Champion', 'message': '', 'amount_dollar': '78.00', 'time': 'Aug 30, 2017 9:35 PM'}, {'supporter_name': 'Bottle Drive -- Aug 8', 'message': '', 'amount_dollar': '194.00', 'time': 'Aug 9, 2017 10:07 AM'}], 'Hossein Seyedmehdi': [], 'Alireza Mirzaee': [{'supporter_name': 'Hossein', 'message': '', 'amount_dollar': '25.00', 'time': 'Aug 9, 2017 10:18 AM'}]}, '2017-09-06': {'Johanna Nicoletta': [{'supporter_name': 'ericssoncommunity', 'message': '', 'amount_dollar': '27.38', 'time': 'May 12, 2017 12:00 AM'}, {'supporter_name': 'Anonymous Donor', 'message': '', 'amount_dollar': '250.00', 'time': 'May 1, 2017 8:45 AM'}], 'Ericsson Activities': [{'supporter_name': 'Foosball Champion', 'message': '', 'amount_dollar': '78.00', 'time': 'Aug 30, 2017 9:35 PM'}, {'supporter_name': 'Bottle Drive -- Aug 8', 'message': '', 'amount_dollar': '194.00', 'time': 'Aug 9, 2017 10:07 AM'}], 'Hossein Seyedmehdi': [], 'Alireza Mirzaee': [{'supporter_name': 'Hossein', 'message': '', 'amount_dollar': '25.00', 'time': 'Aug 9, 2017 10:18 AM'}]}, '2017-09-03': {'Johanna Nicoletta': [{'supporter_name': 'ericssoncommunity', 'message': '', 'amount_dollar': '27.38', 'time': 'May 12, 2017 12:00 AM'}, {'supporter_name': 'Anonymous Donor', 'message': '', 'amount_dollar': '250.00', 'time': 'May 1, 2017 8:45 AM'}], 'Ericsson Activities': [{'supporter_name': 'Foosball Champion', 'message': '', 'amount_dollar': '78.00', 'time': 'Aug 30, 2017 9:35 PM'}, {'supporter_name': 'Bottle Drive -- Aug 8', 'message': '', 'amount_dollar': '194.00', 'time': 'Aug 9, 2017 10:07 AM'}], 'Hossein Seyedmehdi': [], 'Alireza Mirzaee': [{'supporter_name': 'Hossein', 'message': '', 'amount_dollar': '25.00', 'time': 'Aug 9, 2017 10:18 AM'}]}, '2017-09-07': {'Johanna Nicoletta': [{'supporter_name': 'ericssoncommunity', 'message': '', 'amount_dollar': '27.38', 'time': 'May 12, 2017 12:00 AM'}, {'supporter_name': 'Anonymous Donor', 'message': '', 'amount_dollar': '250.00', 'time': 'May 1, 2017 8:45 AM'}], 'Ericsson Activities': [{'supporter_name': 'Foosball Champion', 'message': '', 'amount_dollar': '78.00', 'time': 'Aug 30, 2017 9:35 PM'}, {'supporter_name': 'Bottle Drive -- Aug 8', 'message': '', 'amount_dollar': '194.00', 'time': 'Aug 9, 2017 10:07 AM'}], 'Hossein Seyedmehdi': [], 'Alireza Mirzaee': [{'supporter_name': 'Hossein', 'message': '', 'amount_dollar': '25.00', 'time': 'Aug 9, 2017 10:18 AM'}]}}
    # Get highest donation today
    highest_donation = analytics.get_highest_donation(supporters_data, 3, a_base_day='2017-09-10')
    self.assertEqual(highest_donation['amount_dollar'], '229.41', "Error in finding the highest donor.")
    # Get highest donation during past week
    highest_donation = analytics.get_highest_donation(supporters_data, 8, a_base_day='2017-09-10')
    self.assertEqual(highest_donation['amount_dollar'], '250.00', "Error in finding the highest donor.")
    # Get highest donation ever!
    highest_donation = analytics.get_highest_donation(supporters_data, 1000, a_base_day='2017-09-10')
    self.assertEqual(highest_donation['amount_dollar'], '250.00', "Error in finding the highest donor.")
    
  #@unittest.skip("")
  def test_get_highest_donation_2(self):
    # from file 
    #print("Performing analytics on a specifit data files for supporters...")
    supporters_data_file = os.path.join(utils.get_test_path(), 'supporters_data_2017-09-20.txt')
    supporters_ledger = utils.load_from_file(supporters_data_file)
    highest_donations = []
    window_days_list = [("Yesterday", 2)]#, ("Last week", 7), ("Last month", 30), ("Overall in 2017", 365)]
    for window_days in window_days_list:
      highest_donations.append([window_days[0], window_days[1], 
                                analytics.get_highest_donation(supporters_ledger, 
                                                               window_days[1], 
                                                               a_base_day = '2017-09-20')])
    #print(json.dumps(highest_donations, indent= 4))
    self.assertEqual(highest_donations[0][2]['amount_dollar'], '25.00', "Error in finding the highest donor.")

  #@unittest.skip("")
  def test_get_highest_donation_3(self):
    # from file 
    #print("Performing analytics on a specifit data files for supporters...")
    supporters_data_file = os.path.join(utils.get_test_path(), 'supporters_data_2017-09-22.txt')
    supporters_ledger = utils.load_from_file(supporters_data_file)
    highest_donations = []
    window_days_list = [("Yesterday", 2), ("Last week", 7), ("Last month", 30), ("Overall in 2017", 365)]
    for window_days in window_days_list:
      highest_donations.append([window_days[0], window_days[1], 
                                analytics.get_highest_donation(supporters_ledger, 
                                                               window_days[1],
                                                               a_base_day= '2017-09-22')])
    #print(json.dumps(highest_donations, indent=4))
    self.assertEqual(highest_donations[0][2]['team_member'], 'Ronald Casselman', "Error in finding the highest donor.")
    self.assertEqual(highest_donations[1][2]['team_member'], 'Ronald Casselman', "Error in finding the highest donor.")
    self.assertEqual(highest_donations[2][2]['team_member'], 'Johanna Nicoletta', "Error in finding the highest donor.")
    self.assertEqual(highest_donations[3][2]['team_member'], 'Johanna Nicoletta', "Error in finding the highest donor.")
    
    