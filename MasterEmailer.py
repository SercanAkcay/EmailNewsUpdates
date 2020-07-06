import AutoEmailerFunctions as bbc

#Global Log-In Information
CREDENTIALS = ''
USERNAME = ''
PASSWORD = ''
ARTICLE_TITLES = []
ARTICLE_LINKS = []
BALANCE_SHEET = []
TEMP_TITLES = []
TEMP_LINKS =  []

"""
FUNCTIONS:
##############################################################################

email_log_in_info()
  - input: none
  - output: returns email and password
  - use: opens the file 'Gmail_Login_Creds.txt' and reads the first two lines
         of the file.
         
##############################################################################

send_email(username, password, subject, sender, receiver, message_contents)
  - input:
      username (string)
      password (string)
      subject of email (string)
      sender (string)
      receiver (string)
      message_contents (any, it casts as a string)
  - output:
      none
  - use:
      As it says, it will send an email
  
##############################################################################

scrape_yahoo_news_links()
  - input:
      none
  - output:
      list of 25 most recent news links
  - use:
      Gather the links so you don't need to go looking for it
      
##############################################################################

scrape_yahoo_news_titles()
  - input:
      none
  - output:
      list of 25 most recent news headlines
  - use:
      Gather the article headlines so you don't need to go looking for it
  
##############################################################################

find_balance_sheet(ticker)
  - input:
      ticker (string)
  - output:
      balance sheet as a data frame using pandas
  - use:
      To get the balance sheet of any valid company listed in yahoo finance

##############################################################################
linksBarrons()
  - input:
      none
  - output:
      list of 15 most recent news links
  - use:
      Gather the links so you don't need to go looking for it
      
##############################################################################

headlinesBarrons()
  - input:
      none
  - output:
      list of 15 most recent news headlines
  - use:
      Gather the article headlines so you don't need to go looking for it
  
##############################################################################
"""

# Gmail account log-in information
CREDENTIALS = bbc.email_log_in_info()
USERNAME = CREDENTIALS[0]
PASSWORD = CREDENTIALS[1]

print("Here is what you can do:")
print("1: Send automatic news updates for a specified time period and between a specified time interval")
print("2: Send balance sheets of a specific ticker")

u_input = input("Enter what you would like to do: ")

if(u_input == '1'):
  hrs = input("How long should I check for news? (hours, decimal): ")
  timeToRun = int(hrs) * 3600
  intv = input("How often should I check for news? (minutes, integer): ")
  interval = int(intv) * 60
  
  print("Supported websites: Yahoo Finance and Barrons")
  websiteToScrape = input("Which website would you like to scrape? (y, b): ")
  websiteToScrape = websiteToScrape.lower()
  
  if(websiteToScrape == 'y'):
    bbc.AutoEmailUpdates_Yahoo(timeToRun, interval, USERNAME, PASSWORD)
  elif(websiteToScrape == 'b'):
    bbc.AutoEmailUpdates_Barrons(timeToRun, interval, USERNAME, PASSWORD)

elif(u_input == '2'):
  ticker = input("Enter the ticker of the stock you would like a balance sheet for: ")
  bbc.send_balance_sheet(ticker, USERNAME, PASSWORD)

