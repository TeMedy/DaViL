'''
Created on Aug 30, 2017

@author: Hossein
'''

import os
from utils import get_raw_data_path, get_visual_data_path
import pudb

#MAIL_SERVER = 'smtp.mail.yahoo.com'; MAIL_USERNAME = 'ltn.ericsson@yahoo.com'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_USERNAME = 'ltn.ericsson@gmail.com'
MAIL_PORT = 587
MAIL_PASSWORD = os.environ['MAIL_PASSWORD']

DEFAULT_SUBJECT = 'Stats for LTN'
DEFAULT_BODY = 'Here are the stats for the Light The Night.'

def get_files_to_be_sent(data_dir):
  '''
  Obtains a listing of the files inside the directory specified by data_dir,
  filters out unwanted files and returns a list of the file paths.

    :str : List of paths of files in data_dir.
  '''
  files_in_dir = os.listdir(data_dir)
  files_to_be_sent = []

  for file_in_dir in files_in_dir:
    if file_in_dir.startswith("."):
      # Exclude "hidden" files.
      continue
    elif file_in_dir.endswith(".py"):
      # Exclude Python source code.
      continue

    files_to_be_sent.append(os.path.join(data_dir, file_in_dir))

  return files_to_be_sent

def get_recipients(data_dir):
  '''
  Obtains a listing of the emails inside the directory specified by data_dir,
  inputs
    :str : paths of files in data_dir.
  '''
  files_in_dir = os.listdir(data_dir)
  file_recipients = ''

  # get the file with name .recipient
  for file_in_dir in files_in_dir:
    if file_in_dir == ".recipients":
      file_recipients = os.path.join(data_dir, file_in_dir)
  # return if there is no such file
  if not file_recipients:
    return
  # read the emails from the file
  with open(file_recipients) as f:
    flines = f.readlines()
    # strip the lines from white spaces, e.g., \n, ...
    # and exclude lines that start with '#'
    recipients = [s.strip() for s in flines if len(s) > 0 and s[0] != '#']
  # return if there is no emails  to use
  if not recipients:
    return

  return recipients

def send_email(data_dir, recipients = None, subject = DEFAULT_SUBJECT, body = DEFAULT_BODY):
  '''
  This function emails the files in data_dir. If the recipients
  are not  given as input to the function, it will use the emails
  listed in a hidden file in the same directory.
  19.1.14. email: Examples
  https://docs.python.org/3.4/library/email-examples.html
  input:
    :str : an input directory
    :list : a list of email addresses
  '''

  import smtplib
  from os.path import basename
  from email.mime.application import MIMEApplication
  from email.mime.multipart import MIMEMultipart
  from email.mime.text import MIMEText


  if 'MAIL_PASSWORD' not in os.environ:
    raise Exception("Could not find the \"MAIL_PASSWORD\" environment variable.")

  msg = MIMEMultipart()
  msg['From'] = MAIL_USERNAME
  if not recipients:
    recipients = get_recipients(data_dir)
    if not recipients:
      raise Exception("There is no recipient email(s). Create a '.recipient' file and include the emials in it.")
  msg['To'] = ', '.join(recipients)
  msg['Subject'] = subject

  msg.attach(MIMEText(body, 'plain'))

  for data_file_name in get_files_to_be_sent(data_dir):
    # Attach the files
    with open(data_file_name, "rb") as fil:
      part = MIMEApplication(
          fil.read(),
          Name = basename(data_file_name) )

    # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(data_file_name)
    msg.attach(part)

  text = msg.as_string()

  with smtplib.SMTP(host=MAIL_SERVER, port=MAIL_PORT) as server:
      server.starttls()
      # print("user name = {}, password = {}".format(MAIL_USERNAME, MAIL_PASSWORD))
      server.login(MAIL_USERNAME, MAIL_PASSWORD)
      server.sendmail(MAIL_USERNAME, recipients, text)
      #server.quit()

if __name__ == "__main__":
  print("sending emails...")
  d = get_raw_data_path()
  print("recipient list: {}".format(get_recipients(d)))

  #pu.db

  send_email(d)

  print("Done!")
