'''
Created on Aug 29, 2017

@author: Hossein
'''
import argparse
import os, time
from email_handler import send_email
import utils # import get_raw_data_path, get_visual_data_path
import tqdm
import scraping
import analytics
import visualizer
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

  #
  # Perform analytics 
  #
  print("Performing analytics...")
  highest_donations = []
  window_days_list = [("Yesterday", 2), ("Last 7 days", 7), ("Last 30 days", 30), ("Overall in 2017", 365)]
  for window_days in window_days_list:
    highest_donations.append([window_days[0], window_days[1], 
                              analytics.get_highest_donation(supporters_ledger, window_days[1])])
  # get data for donations per divisions 
  fname = os.path.join(utils.get_raw_data_path(), 'members_divisions.txt')
  members_divisions = utils.load_from_file(fname)
  dbd = analytics.get_donation_by_division(team_ledger, members_divisions)
  # Historical donation 
  doantions_over_time = analytics.get_historical_donaitons(team_ledger)
  # Get division of all team members && update the members_divisions with new members 
  mem_div = analytics.get_all_members_division(team_ledger, members_divisions)
  fname = os.path.join(utils.get_raw_data_path(), 'members_divisions.txt')
  utils.save_to_file(fname, mem_div)
  # create new file for the admins
  fname = os.path.join(utils.get_admin_data_path(), 'members_divisions.txt')
  utils.save_to_file(fname, mem_div)
  
  #
  # Visualization
  #
  #logo file: 
  file_name_logo = os.path.join(utils.get_raw_data_path(), 'logo_LTN.png')
  file_name_template_pptx = os.path.join(utils.get_raw_data_path(), 'template.pptx')
  #
  file_name_by_div = os.path.join(utils.get_raw_data_path(), 'divisions.png')
  visualizer.generate_bar_chart(dbd,  file_name_by_div) 
  #
  file_name_time_series = os.path.join(utils.get_raw_data_path(), 'time_series.png')
  visualizer.generate_time_series(doantions_over_time, file_name_time_series)
  # 
  out_file_name = 'LTN_daily_stats.pptx'# + time.strftime('%b %d, %Y') + '.pptx'
  fname = os.path.join(utils.get_visual_data_path(), out_file_name)
  visualizer.generate_ppt(fname, highest_donations = highest_donations, 
                 image_total_fund_raised = file_name_time_series, 
                 image_fund_by_division = file_name_by_div, 
                 image_thermometer= file_name_thermometer,
                 logo=file_name_logo, 
                 file_template_presentation= file_name_template_pptx)
  #
  # Send email
  #
  if args.send_email:
    print("Sending e-mail...")
    send_email(utils.get_raw_data_path(), subject = "LTN -- raw data", body="Do not reply.\n")
    send_email(utils.get_visual_data_path(), subject = "Today's LTN stats and charts", body="Automatically generated email.\n\n")
    if analytics.is_new_member(team_ledger):
      send_email(utils.get_admin_data_path(), subject = "New LTN Member!", body="Please update the team of the new member.")

  print("Done!")
