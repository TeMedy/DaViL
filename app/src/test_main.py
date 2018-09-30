'''
Created on Aug 29, 2017

@author: Hossein
'''

import pdb

import argparse
import os, time
from email_handler import send_email
import utils # import get_raw_data_path, get_visual_data_path
import tqdm
import scraping
import analytics
#import visualizer
from datetime import datetime

FILE_NAME_MEMBERS = 'member_data.txt'
FILE_NAME_SUPPORTERS = 'supporters_data.txt'

if __name__ == "__main__":
  print("Starting a new run at {} ...".format( str(datetime.now()) ))
  parser = argparse.ArgumentParser(description='Data analytics and Visualization for LightTheNight (DaViL)')
  parser.add_argument('--no-email', dest='send_email', default=True, action='store_false')

  args = parser.parse_args()

  # get the absolute path to the data files
  team_data_file = os.path.join(utils.get_raw_data_path(), FILE_NAME_MEMBERS)
  supporters_data_file = os.path.join(utils.get_raw_data_path(), FILE_NAME_SUPPORTERS)


  #
  # Scrape the web
  #
  team_members = scraping.get_team_members()

  # Update the ledger file with new team member data
  team_ledger = utils.load_from_file(team_data_file)
  scraping.update_ledger(team_ledger, team_members)
  utils.save_to_file(team_data_file, team_ledger)
  # Get each team member's page showing the supporters and detailed amount of donations
  print("Getting all the pages for team members...")
  all_supporters = {}
  for member in tqdm.tqdm(team_members):
    p_url = member['pageUrl']
    name = member['name']
    all_supporters[name] = scraping.parse_member_page(scraping.get_member_page(p_url))
  # Update the supporter's ledger in the files
  supporters_ledger = utils.load_from_file(supporters_data_file)
  scraping.update_ledger(supporters_ledger, all_supporters)
  utils.save_to_file(supporters_data_file, supporters_ledger)
  # Get thermometer
  file_name_thermometer = os.path.join(utils.get_raw_data_path(), 'thermometer.jpg')
  scraping.get_thermometer(file_name_thermometer)
