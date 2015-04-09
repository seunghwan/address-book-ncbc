import ConfigParser
import getopt
import getpass
import sys
import os.path
from email.mime.text import MIMEText
import smtplib

def get_userid_and_password(default_domain = 'ncbctimothy.org'):
  # try reading login info from config file
  if os.path.exists("user.cfg"):
    config = ConfigParser.RawConfigParser()
    config.read('user.cfg')
    if config.has_section('user'):
      user = config.get('user', 'id')
      pw = config.get('user', 'pw')
      if user.find('@') == -1:
        user += '@' + default_domain
      return (user, pw) 

  # parse command line options
  try:
    opts, args = getopt.getopt(sys.argv[1:], "", ["user=", "pw="])
  except getopt.error, msg:
    print 'python spreadsheetExample.py --user [username] --pw [password] '
    sys.exit(2)
  
  # Process options
  user = ''
  pw = ''
  # Use userid and password from the command line if exists.
  for o, a in opts:
    if o == "--user":
      user = a
    elif o == "--pw":
      pw = a

  # Read userid and password if they're not set.
  if user == '':
    message = 'Userid (i.e., YOURID@' + default_domain + ' or just YOURID): '
    user = raw_input(message)
    if user.find('@') == -1:
      user += '@' + default_domain
      print 'Set Userid to ', user
  if pw == '':
    pw = getpass.getpass()

  if user == '' or pw == '':
    print 'python spreadsheetExample.py --user [username] --pw [password] '
    sys.exit(2)

  return (user, pw)

def send_email(subject, message):
  if not os.path.exists('subscribers.cfg'):
    return
  
  emails = []
  config = ConfigParser.RawConfigParser()
  config.read('subscribers.cfg')

  for subscriber in config.sections():
    emails.append(config.get(subscriber, 'email'))

  user, pw = get_userid_and_password()
  server = 'smtp.gmail.com'
  port = 587

  msg = MIMEText(message)
  msg['Subject'] = subject
  msg['To'] = ", ".join(emails)
  msg['From'] = user
  email = smtplib.SMTP(server, port)
  email.starttls()
  email.login(user, pw)
  email.sendmail(user, emails, msg.as_string())
  email.quit()

if __name__=='__main__':
  send_email("test", "test")
