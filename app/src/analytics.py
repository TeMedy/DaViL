'''
Created on Sep 9, 2017

@author: Hossein
'''

import utils
import os, json
import datetime
import copy

def str2date(date_str):
  '''
  convert YYYY-MM-DD to datetime.date
  '''
  splitted_date = date_str.split('-')
  # convert to int 
  d = [int(s) for s in splitted_date]
  return datetime.date(d[0], d[1], d[2])
 
def get_sum_donations(team_members):
  '''
  computes the sum_donations of donations for all team members
  input 
    :dict : a dictionary of team members
  output
    :float : sum of donations 
  '''
  sum_donations = 0 
  for member_info in team_members:
    # get the amount field and remove dollar sign  
    amount = member_info['amount'].replace('$', '').replace(',', '')
    sum_donations += float(amount)
  return sum_donations

def get_highest_donation(supporters_data, window_days, a_base_day = None):
  '''
  return the highest donation within the past number of days 
  input: 
    :list : a ledger containing supporter's data ['2017-09-01': {}, ...]
    :int : a window size indicates how many days it comparison  goes back. 
            For instance, if window_days == 1, the function gets the highest 
            donation today; if window_days == 7, the function will
            return the highest donation within the past week.
    :str : a day in the format of YYYY-MM-DD
  return: 
    :dict : {'supporter_name': a_supporter_name, 'amount': a_dollar_amount, 
            'supportee': a_team_member, 'message': a_message }
  '''
  # get the day before the window day
  base_day = datetime.date.today()
  if a_base_day: 
    base_day = str2date(a_base_day)
  cutoff_day = base_day - datetime.timedelta(days = window_days)
  days_before_cutoff = [day for day in supporters_data if str2date(day) <= cutoff_day]
  # Find the day 'YYYY-MM-DD' right before the window day
  day_before_cutoff = ''
  if len(days_before_cutoff) > 0: 
    day_before_cutoff = max(days_before_cutoff) #the day before cut off

  # get the supporters on the day right before the beginning of the window
  supporters_before_cutoff = []
  if day_before_cutoff in supporters_data: 
    supp_data = supporters_data[day_before_cutoff]
    for member in supp_data: 
      for supporter in supp_data[member]: 
        supp = copy.copy(supporter) #E.g., supp = {'time': 'Jul 19, 2017 12:00 AM', 'message': '', 'amount_dollar': '229.41', 'supporter_name': 'ericssoncommunity'}
        supp['team_member'] = member 
        supporters_before_cutoff.append(supp)     
   
  # get the supporters on the last day of the ledger   
  last_day = max(supporters_data)
  supporters_within_window = []
  supp_data = supporters_data[last_day]
  for member in supp_data: 
    for supporter in supp_data[member]: 
      #print("supporter = " + json.dumps(supporter))
      supp = copy.copy(supporter)
      supp['team_member'] = member
      # Subtract the set of supporters before the window day from the set 
      # of supporters on the last day to get the donations within the days 
      # determined by the window_days. But since these are lists of 
      # dictionaries, the subtraction is not straight forward. 
      if supp not in supporters_before_cutoff:
        # exclude if no amount in dollar
        try: 
          d = float(supp['amount_dollar'].replace('$', '')) 
          supporters_within_window.append(supp)
        except: 
          pass 
  # find the highest donor:
  if len(supporters_within_window) > 0:
    # remove the dollar sign and compare all donation amounts to find the max
    highest_donation = max(supporters_within_window, key = lambda x: float(x['amount_dollar'].replace('$', '')))
    return highest_donation

def get_donation_by_division(team_ledger, members_divisions):
  '''
  return
    :list : [('a_division_lable', money_raised_float), (...), ...]
  '''
  money_raised_by_div = {}
  last_day= max(team_ledger)
  # only use the last day
  team = team_ledger[last_day]
  for member in team:
    member_name = member['name']
    if member_name in members_divisions:
      # make sure the member division is not empty
      if members_divisions[member_name]:
        divis_of_member = members_divisions[member_name]
        money_raised_by_member = float(member['amount'].replace("$", "").replace(',', ''))
        if divis_of_member in money_raised_by_div: 
          money_raised_by_div[divis_of_member] += money_raised_by_member
        else:
          money_raised_by_div[divis_of_member] = money_raised_by_member
  #print(json.dumps(money_raised_by_div))
  return money_raised_by_div.items()

def get_historical_donaitons(team_data):
  result = []
  for day in team_data: 
    sum_donation = get_sum_donations(team_data[day])
    result.append((day, sum_donation))
  result.sort(key= lambda x: x[0])
  return result

def get_all_members_division(team_ledger, members_divisions):
  '''
  Get all the members and their divisions. it includes members with no
  division too. 
  '''
  last_day = max(team_ledger)
  team_data = team_ledger[last_day]
  member_divs = {}
  for member in team_data: 
    name = member['name']
    member_divs[name] = ''
    if name in members_divisions: 
      member_divs[name] = members_divisions[name]
  return member_divs

def is_new_member(member_data):
  '''
  determine if there was a new member yesterday 
  input: 
    :dict a ledger of memeber's data
  output: 
    :bool : True/False
  '''
  dates = list(member_data.keys())
  dates.sort()
  if len(dates) > 1: 
    if len(member_data[dates[-1]]) > len(member_data[dates[-2]]): 
      return True 
  return False 

if __name__ == "__main__":
  # Test sum donation 
  dstr = "2017-09-01"
  print("date str of {} is {}.".format(dstr, str2date(dstr)))
  #
  fname = os.path.join(utils.get_raw_data_path(), 'member_data.txt')
  member_data = utils.load_from_file(fname)
  sum_donation = get_sum_donations(member_data[max(member_data)])
  print("sum donation is {} dollar".format(sum_donation))
  
  # Test donations by division 
  fname = os.path.join(utils.get_raw_data_path(), 'members_divisions.txt')
  members_divisions = utils.load_from_file(fname)
  dbd = get_donation_by_division(member_data, members_divisions)
  print(dbd)
  
  # Test all members divisions 
  members_divs = get_all_members_division(member_data, members_divisions)
  print(members_divs)
  
  # Test historical data 
  print(get_historical_donaitons(member_data))
  #
  # Test the highest donation functionality 
  #
  supporters_data = {'2017-09-08': {'Johanna Nicoletta': [{'supporter_name': 'ericssoncommunity', 'message': '', 'amount_dollar': '229.41', 'time': 'Jul 19, 2017 12:00 AM'}, {'supporter_name': 'ericssoncommunity', 'message': '', 'amount_dollar': '27.38', 'time': 'May 12, 2017 12:00 AM'}, {'supporter_name': 'Anonymous Donor', 'message': '', 'amount_dollar': '250.00', 'time': 'May 1, 2017 8:45 AM'}], 'Ericsson Activities': [{'supporter_name': 'Foosball Champion', 'message': '', 'amount_dollar': '78.00', 'time': 'Aug 30, 2017 9:35 PM'}, {'supporter_name': 'Bottle Drive -- Aug 8', 'message': '', 'amount_dollar': '194.00', 'time': 'Aug 9, 2017 10:07 AM'}], 'Hossein Seyedmehdi': [], 'Alireza Mirzaee': [{'supporter_name': 'Hossein', 'message': '', 'amount_dollar': '25.00', 'time': 'Aug 9, 2017 10:18 AM'}]}, '2017-09-05': {'Johanna Nicoletta': [{'supporter_name': 'ericssoncommunity', 'message': '', 'amount_dollar': '27.38', 'time': 'May 12, 2017 12:00 AM'}, {'supporter_name': 'Anonymous Donor', 'message': '', 'amount_dollar': '250.00', 'time': 'May 1, 2017 8:45 AM'}], 'Ericsson Activities': [{'supporter_name': 'Foosball Champion', 'message': '', 'amount_dollar': '78.00', 'time': 'Aug 30, 2017 9:35 PM'}, {'supporter_name': 'Bottle Drive -- Aug 8', 'message': '', 'amount_dollar': '194.00', 'time': 'Aug 9, 2017 10:07 AM'}], 'Hossein Seyedmehdi': [], 'Alireza Mirzaee': [{'supporter_name': 'Hossein', 'message': '', 'amount_dollar': '25.00', 'time': 'Aug 9, 2017 10:18 AM'}]}, '2017-09-09': {'Johanna Nicoletta': [{'supporter_name': 'ericssoncommunity', 'message': '', 'amount_dollar': '229.41', 'time': 'Jul 19, 2017 12:00 AM'}, {'supporter_name': 'ericssoncommunity', 'message': '', 'amount_dollar': '27.38', 'time': 'May 12, 2017 12:00 AM'}, {'supporter_name': 'Anonymous Donor', 'message': '', 'amount_dollar': '250.00', 'time': 'May 1, 2017 8:45 AM'}], 'Ericsson Activities': [{'supporter_name': 'Foosball Champion', 'message': '', 'amount_dollar': '78.00', 'time': 'Aug 30, 2017 9:35 PM'}, {'supporter_name': 'Bottle Drive -- Aug 8', 'message': '', 'amount_dollar': '194.00', 'time': 'Aug 9, 2017 10:07 AM'}], 'Hossein Seyedmehdi': [], 'Alireza Mirzaee': [{'supporter_name': 'Hossein', 'message': '', 'amount_dollar': '25.00', 'time': 'Aug 9, 2017 10:18 AM'}]}, '2017-09-06': {'Johanna Nicoletta': [{'supporter_name': 'ericssoncommunity', 'message': '', 'amount_dollar': '27.38', 'time': 'May 12, 2017 12:00 AM'}, {'supporter_name': 'Anonymous Donor', 'message': '', 'amount_dollar': '250.00', 'time': 'May 1, 2017 8:45 AM'}], 'Ericsson Activities': [{'supporter_name': 'Foosball Champion', 'message': '', 'amount_dollar': '78.00', 'time': 'Aug 30, 2017 9:35 PM'}, {'supporter_name': 'Bottle Drive -- Aug 8', 'message': '', 'amount_dollar': '194.00', 'time': 'Aug 9, 2017 10:07 AM'}], 'Hossein Seyedmehdi': [], 'Alireza Mirzaee': [{'supporter_name': 'Hossein', 'message': '', 'amount_dollar': '25.00', 'time': 'Aug 9, 2017 10:18 AM'}]}, '2017-09-03': {'Johanna Nicoletta': [{'supporter_name': 'ericssoncommunity', 'message': '', 'amount_dollar': '27.38', 'time': 'May 12, 2017 12:00 AM'}, {'supporter_name': 'Anonymous Donor', 'message': '', 'amount_dollar': '250.00', 'time': 'May 1, 2017 8:45 AM'}], 'Ericsson Activities': [{'supporter_name': 'Foosball Champion', 'message': '', 'amount_dollar': '78.00', 'time': 'Aug 30, 2017 9:35 PM'}, {'supporter_name': 'Bottle Drive -- Aug 8', 'message': '', 'amount_dollar': '194.00', 'time': 'Aug 9, 2017 10:07 AM'}], 'Hossein Seyedmehdi': [], 'Alireza Mirzaee': [{'supporter_name': 'Hossein', 'message': '', 'amount_dollar': '25.00', 'time': 'Aug 9, 2017 10:18 AM'}]}, '2017-09-07': {'Johanna Nicoletta': [{'supporter_name': 'ericssoncommunity', 'message': '', 'amount_dollar': '27.38', 'time': 'May 12, 2017 12:00 AM'}, {'supporter_name': 'Anonymous Donor', 'message': '', 'amount_dollar': '250.00', 'time': 'May 1, 2017 8:45 AM'}], 'Ericsson Activities': [{'supporter_name': 'Foosball Champion', 'message': '', 'amount_dollar': '78.00', 'time': 'Aug 30, 2017 9:35 PM'}, {'supporter_name': 'Bottle Drive -- Aug 8', 'message': '', 'amount_dollar': '194.00', 'time': 'Aug 9, 2017 10:07 AM'}], 'Hossein Seyedmehdi': [], 'Alireza Mirzaee': [{'supporter_name': 'Hossein', 'message': '', 'amount_dollar': '25.00', 'time': 'Aug 9, 2017 10:18 AM'}]}}
  hd = get_highest_donation(supporters_data, 2, a_base_day='2017-09-10')
  print("highest donation yesterday is {}.".format(hd)) 
  hd = get_highest_donation(supporters_data, 7, a_base_day='2017-09-10')
  last_hd = hd
  print("highest donation during past 7 days is {}.".format(hd)) 
  hd30 = get_highest_donation(supporters_data, 7, a_base_day='2017-09-10')
  if hd30 != last_hd:
    print("highest donation during past 30 days is {}.".format(hd30)) 
  
  # check if there is a new member
  print("checking if there is a new member...")
  member_data = {
                 "2017-09-05": [{"pageUrl": "https://secure.e2rm.com/registrant/FundraisingPage.aspx?registrationID=3697209&langPref=en-CA&Referrer=https%3a%2f%2fsecure.e2rm.com%2fregistrant%2fsearch.aspx%3feventid%3d210107%26langpref%3den-CA", "name": "Johanna Nicoletta", "isTeamCaptain": "True", "amount": "$277.38", "facebookId": "1633682560"}, {"pageUrl": "https://secure.e2rm.com/registrant/FundraisingPage.aspx?registrationID=3877056&langPref=en-CA&Referrer=https%3a%2f%2fsecure.e2rm.com%2fregistrant%2fsearch.aspx%3feventid%3d210107%26langpref%3den-CA", "name": "Ericsson Activities", "isTeamCaptain": "False", "amount": "$272.00", "facebookId": ""}, {"pageUrl": "https://secure.e2rm.com/registrant/FundraisingPage.aspx?registrationID=3869108&langPref=en-CA&Referrer=https%3a%2f%2fsecure.e2rm.com%2fregistrant%2fsearch.aspx%3feventid%3d210107%26langpref%3den-CA", "name": "Alireza Mirzaee", "isTeamCaptain": "False", "amount": "$25.00", "facebookId": ""}, {"pageUrl": "https://secure.e2rm.com/registrant/FundraisingPage.aspx?registrationID=3855399&langPref=en-CA&Referrer=https%3a%2f%2fsecure.e2rm.com%2fregistrant%2fsearch.aspx%3feventid%3d210107%26langpref%3den-CA", "name": "Hossein Seyedmehdi", "isTeamCaptain": "False", "amount": "$0.00", "facebookId": ""}], 
                 "2017-09-06": [{"pageUrl": "https://secure.e2rm.com/registrant/FundraisingPage.aspx?registrationID=3697209&langPref=en-CA&Referrer=https%3a%2f%2fsecure.e2rm.com%2fregistrant%2fsearch.aspx%3feventid%3d210107%26langpref%3den-CA", "name": "Johanna Nicoletta", "isTeamCaptain": "True", "amount": "$277.38", "facebookId": "1633682560"}, {"pageUrl": "https://secure.e2rm.com/registrant/FundraisingPage.aspx?registrationID=3877056&langPref=en-CA&Referrer=https%3a%2f%2fsecure.e2rm.com%2fregistrant%2fsearch.aspx%3feventid%3d210107%26langpref%3den-CA", "name": "Ericsson Activities", "isTeamCaptain": "False", "amount": "$272.00", "facebookId": ""}, {"pageUrl": "https://secure.e2rm.com/registrant/FundraisingPage.aspx?registrationID=3869108&langPref=en-CA&Referrer=https%3a%2f%2fsecure.e2rm.com%2fregistrant%2fsearch.aspx%3feventid%3d210107%26langpref%3den-CA", "name": "Alireza Mirzaee", "isTeamCaptain": "False", "amount": "$25.00", "facebookId": ""}],
                 "2017-09-09": [{"pageUrl": "https://secure.e2rm.com/registrant/FundraisingPage.aspx?registrationID=3697209&langPref=en-CA&Referrer=https%3a%2f%2fsecure.e2rm.com%2fregistrant%2fsearch.aspx%3feventid%3d210107%26langpref%3den-CA", "name": "Johanna Nicoletta", "isTeamCaptain": "True", "amount": "$506.79", "facebookId": "1633682560"}, {"pageUrl": "https://secure.e2rm.com/registrant/FundraisingPage.aspx?registrationID=3877056&langPref=en-CA&Referrer=https%3a%2f%2fsecure.e2rm.com%2fregistrant%2fsearch.aspx%3feventid%3d210107%26langpref%3den-CA", "name": "Ericsson Activities", "isTeamCaptain": "False", "amount": "$272.00", "facebookId": ""}, {"pageUrl": "https://secure.e2rm.com/registrant/FundraisingPage.aspx?registrationID=3869108&langPref=en-CA&Referrer=https%3a%2f%2fsecure.e2rm.com%2fregistrant%2fsearch.aspx%3feventid%3d210107%26langpref%3den-CA", "name": "Alireza Mirzaee", "isTeamCaptain": "False", "amount": "$25.00", "facebookId": ""}, {"pageUrl": "https://secure.e2rm.com/registrant/FundraisingPage.aspx?registrationID=3855399&langPref=en-CA&Referrer=https%3a%2f%2fsecure.e2rm.com%2fregistrant%2fsearch.aspx%3feventid%3d210107%26langpref%3den-CA", "name": "Hossein Seyedmehdi", "isTeamCaptain": "False", "amount": "$0.00", "facebookId": ""}] 
                 }
  #print(member_data.keys())
  print(is_new_member(member_data))

