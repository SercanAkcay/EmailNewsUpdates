import string
import smtplib
from email.message import EmailMessage
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

#########################################################################################################
def email_log_in_info():
  creds = []
  email = ''
  password = ''
  # Read file to get email username and password
  # NOTE: You should only use the first two lines of the file to store your email and password
  f = open("Gmail_Login_Creds.txt", "r")
  
  line_by_line = f.readlines()
  for line in line_by_line:
    creds.append(line.strip())
    
  f.close()
  # Get information from file and store into variables
  email, password = [creds[i] for i in (0, 1)]
  del creds #Free up memory
  
  return(email, password)
  
#########################################################################################################
"""
Allows the program to send an email after the user has logged into their account
"""
def send_email(uname, pword, subject, sender, receiver, msg_content):
  # Set up the message
  # Subject, From, To, and Body
  msg = EmailMessage()
  msg['Subject'] = subject
  msg['From'] = sender
  msg['To'] = receiver
  msg.set_content(str(msg_content))

  # SMTP_SSL creates a secure line to send message using port 465
  with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(uname, pword) # Login
    smtp.send_message(msg) # Send message via email
    
  return
  
#########################################################################################################
"""
Scrapes finance.yahoo.com/news for links to their top 25 most recent articles
"""
def scrape_yahoo_news_links():
  all_links = [] # Includes junk links
  news_and_videos = [] # Only relevant links
  append_to = 'https://finance.yahoo.com' # Used to create whole link
  newsSubstring = '/news' # Used to find /news
  videoSubstring = '/video' # Used to find /video
  
  # Access specific url and load data into soup
  yahoo_news_url = 'https://finance.yahoo.com/news'
  yahoo_news_response = requests.get(yahoo_news_url)
  soup = BeautifulSoup(yahoo_news_response.text, 'html.parser')
    
  # Find all of the links available on webpage and append to all_links
  for link in soup.find_all('a', href=True):
    if link.text:
      all_links.append(link['href'])

  # Search for only /news and /video links
  # Use append to create full link
  for l in all_links:
    if(l.find(newsSubstring) == 0 or l.find(videoSubstring) == 0):
      news_and_videos.append(append_to+l)
      append_to = 'https://finance.yahoo.com'

  # Pop the last two worthless links
  news_and_videos.pop() #'https://finance.yahoo.com/news/'
  news_and_videos.pop() #'https://finance.yahoo.com/videos/'

  return news_and_videos
  
#########################################################################################################
"""
Scrapes finance.yahoo.com/news for headlines to their top 25 most recent articles
"""
def scrape_yahoo_news_titles():
  headLines = [] # Article headlines
  
  # Access specific url and load data into soup
  yahoo_news_url = 'https://finance.yahoo.com/news'
  yahoo_news_response = requests.get(yahoo_news_url)
  soup = BeautifulSoup(yahoo_news_response.text, 'html.parser')

  # Search in specific class in yahoo finance news
  ul = soup.find('ul', {'class': 'My(0) Ov(h) P(0) Wow(bw)'})

  # Searches for top 25 most recent news article titles
  for li in ul.find_all('li'):
    title = [jStream.text for jStream in li.find_all('h3', {'class': 'Mb(5px)'})]
    headLines.append(str(title).strip('[]'))

  return headLines
  
#########################################################################################################
"""
Scrapes https://www.barrons.com/topics/technology for headlines to their top 15 most recent articles
"""
def headlinesBarrons():
  headLines = [] # Article headlines
  styleCol = 'style--column--2u7yywNS style--column-top--2wtJOJkr style--column-8--1yL3Jdqd style--column--37Q00wRx'
  
  # Access specific url and load data into soup
  barrons_news_url = 'https://www.barrons.com/topics/technology/1'
  barrons_news_response = requests.get(barrons_news_url)
  soup = BeautifulSoup(barrons_news_response.text, 'html.parser')

  # Search in specific class in yahoo finance news
  ul = soup.find('div', {'class': styleCol})

  # Searches for top 15 most recent news article titles
  for h3 in ul.find_all('h3'):
    title = [jStream.text for jStream in h3.find_all('a')]
    headLines.append(title)
  
  return headLines
  
#########################################################################################################
"""
Scrapes https://www.barrons.com/topics/technology for links to their top 15 most recent articles
"""
def linksBarrons():
  all_links = [] # Includes all links
  relevant_links = [] # Filters only the relevant links
  articleSubstring = 'https://www.barrons.com/articles/'
  
  # Access specific url and load data into soup
  barrons_news_url = 'https://www.barrons.com/topics/technology/1'
  barrons_news_response = requests.get(barrons_news_url)
  soup = BeautifulSoup(barrons_news_response.text, 'html.parser')

  # Find all of the links available on webpage and append to all_links
  for link in soup.find_all('a', href=True):
    if( articleSubstring in str(link['href']) ):
      all_links.append(str(link['href']))
      
  # Filter out only the links that lead to articles and append to relevant_links
  for i in range(len(all_links)):
    if not(all_links[i] in relevant_links):
      relevant_links.append(all_links[i])
      
  return relevant_links
  
#########################################################################################################
"""
Scrapes finance.yahoo.com for the balance sheeet of the company ticker you enter
"""
def send_balance_sheet(ticker, usernm, passwd):
  msg = ''
  t = str(ticker) #Make sure the ticker symbol is a string
  subjectLine = 'Balance Sheet for $' + t

  yahoo_balance_sheet_url = 'https://finance.yahoo.com/quote/' + t + '/balance-sheet?p=' + t
  yahoo_quote_response = requests.get(yahoo_balance_sheet_url) # Access yahoo finance quote page of ticker
  soup = BeautifulSoup(yahoo_quote_response.text, 'html.parser') # Load the data to soup
  
  # Search for specific class in finance.yahoo/quote
  yFin = soup.find_all('div', {'class': 'D(tbr)'})
  
  headers = []
  temp_list = []
  final = []
  index = 0
  
  #Get headers of each column in the balance sheet
  for h in yFin[0].find_all('div', {'class': 'D(ib)'}):
      headers.append(h.text)
      
  #Balance Sheet contents
  while idx <= len(features)-1:
      #Run through each line of the sheet
      temp = yFin[idx].find_all('div', {'class': 'D(tbc)'})
      for line in temp:
          #add each line to the temp list
          temp_list.append(line.text)
      #Append temp list to the final list
      final.append(temp_list)
      #clear temp_list
      temp_list = []
      idx+=1
  #Set the final list into a data frame
  df = pd.DataFrame(final[1:])
  #Set headers of the data frame
  df.columns = headers
  
  #Crate a pretty message
  msg = str(df) + '\n' + 'Full Balance Sheet at:\n' + yahoo_balance_sheet_url
  #Send the Balance Sheet via email
  send_email(usernm, passwd, subjectLine, usernm, usernm, msg)

  return

#########################################################################################################
"""
Check for new news stories on Yahoo finance

Loop through the list of links, when comparing to the original ones, use a counter to tell you
the location of the new article. Use the location to indicate which stories you are going to
send to yourself, then update the list completely and continue from there.
"""
def AutoEmailUpdates_Yahoo(runTime, checkInterval, usernm, passwd):
  subjectLine = 'New Article(s) from Yahoo'
  msg = ''
  TEMP_TITLES = []
  TEMP_LINKS = []
  ARTICLE_TITLES = []
  ARTICLE_LINKS = []
  NEW_LINKS = []
  NEW_TITLES = []
  newArticleLoc = 0
  endNewArticles = False

  print("Starting...")
  
  # Get newest article titles and links
  ARTICLE_TITLES = scrape_yahoo_news_titles()
  ARTICLE_LINKS = scrape_yahoo_news_links()
  
  #Store them to find where the new ones are later
  TEMP_TITLES = ARTICLE_TITLES
  TEMP_LINKS = ARTICLE_LINKS

  print("Running...")
  
  startTime = time.time()
  in_use = True
  
  while(in_use):
    msg = ''
    elapsedTime = time.time() - startTime
    
    #Sleep first, I assume you already know what the newest articles are
    time.sleep(checkInterval)
    
    #Obtain information of new articles
    ARTICLE_TITLES = scrape_yahoo_news_titles()
    ARTICLE_LINKS = scrape_yahoo_news_links()

    #Check where the location of the first title in the old list doesn't match in the new list
    for i in range(len(TEMP_TITLES)):
      if( (not(TEMP_TITLES[0] == ARTICLE_TITLES[i])) ):
        newArticleLoc = newArticleLoc + 1
      #If it matches later in the list, don't look further
      if(TEMP_TITLES[0] == ARTICLE_TITLES[i]):
        endNewArticles = True
      #Break from the for loop once you find the end of the new articles
      if(endNewArticles):
        break

    #If there is a difference, then only mark those differences
    #for replacement
    if(not(newArticleLoc == 0)):
      for i in range(0, newArticleLoc):
        NEW_LINKS.append(ARTICLE_LINKS[i])
        NEW_TITLES.append(ARTICLE_TITLES[i])
      
    #Make sure both the new titles list and new links list aren't empty
    if( not(len(NEW_TITLES) == 0) and not(len(NEW_LINKS) == 0) ):
      if( not(len(NEW_TITLES) == len(ARTICLE_TITLES)) ):
      #Format the message with title above and link below, separate new articles using \n\n
        for i in range(len(NEW_TITLES)):
          msg = msg + str(NEW_TITLES[i]).strip('[]') + '\n' + str(NEW_LINKS[i]).strip('[]') + '\n\n'
          
    #Sends email to yourself with new articles as long as the message isn't empty
    if( not(msg == '') ):
      send_email(usernm, passwd, subjectLine, usernm, usernm, msg)
    
    #Reset all of the variables in use
    TEMP_TITLES = ARTICLE_TITLES
    TEMP_LINKS = ARTICLE_LINKS
    NEW_LINKS = []
    NEW_TITLES = []
    newArticleLoc = 0
    endNewArticles = False
    
    #Once we pass the time that we want to scrape for, kill the program
    if(elapsedTime >= int(runTime)):
      print("Finished...")
      in_use = False
  
  return
  
#########################################################################################################
"""
Check for new news stories on Barrons

Loop through the list of links, when comparing to the original ones, use a counter to tell you
the location of the new article. Use the location to indicate which stories you are going to
send to yourself, then update the list completely and continue from there.
"""
def AutoEmailUpdates_Barrons(runTime, checkInterval, usernm, passwd):
  subjectLine = 'New Article(s) from Barrons'
  msg = ''
  TEMP_TITLES = []
  TEMP_LINKS = []
  ARTICLE_TITLES = []
  ARTICLE_LINKS = []
  NEW_LINKS = []
  NEW_TITLES = []
  newArticleLoc = 0
  endNewArticles = False

  print("Starting...")

  # Get newest article titles and links
  ARTICLE_TITLES = headlinesBarrons()
  ARTICLE_LINKS = linksBarrons()

  #Store them to find where the new ones are later
  TEMP_TITLES = ARTICLE_TITLES
  TEMP_LINKS = ARTICLE_LINKS

  print("Running...")

  startTime = time.time()
  in_use = True

  while(in_use):
    msg = ''
    elapsedTime = time.time() - startTime
    
    #Sleep first, I assume you already know what the newest articles are
    time.sleep(checkInterval)
    
    #Obtain in formation of new articles
    ARTICLE_TITLES = headlinesBarrons()
    ARTICLE_LINKS = linksBarrons()

    #Check where the location of the first title in the old list doesn't match in the new list
    for i in range(len(TEMP_TITLES)):
      if( (not(TEMP_TITLES[0] == ARTICLE_TITLES[i])) ):
        newArticleLoc = newArticleLoc + 1
      #If it matches later in the list, don't look further
      if(TEMP_TITLES[0] == ARTICLE_TITLES[i]):
        endNewArticles = True
      #Break from the for loop once you find the end of the new articles
      if(endNewArticles):
        break

    #If there is a difference, then only mark those differences
    #for replacement
    if(not(newArticleLoc == 0)):
      for i in range(0, newArticleLoc):
        NEW_LINKS.append(ARTICLE_LINKS[i])
        NEW_TITLES.append(ARTICLE_TITLES[i])
      
    #Make sure both the new titles list and new links list aren't empty
    if( not(len(NEW_TITLES) == 0) and not(len(NEW_LINKS) == 0) ):
      if( not(len(NEW_TITLES) == len(ARTICLE_TITLES)) ):
        #Format the message with title above and link below, separate new articles using \n\n
        for i in range(len(NEW_TITLES)):
          msg = msg + str(NEW_TITLES[i]).strip('[]') + '\n' + str(NEW_LINKS[i]).strip('[]') + '\n\n'
          
    #Sends email to yourself with new articles as long as the message isn't empty
    if( not(msg == '') ):
      send_email(usernm, passwd, subjectLine, usernm, usernm, msg)
    
    #Reset all of the variables in use
    TEMP_TITLES = ARTICLE_TITLES
    TEMP_LINKS = ARTICLE_LINKS
    NEW_LINKS = []
    NEW_TITLES = []
    newArticleLoc = 0
    endNewArticles = False
    
    #Once we pass the time that we want to scrape for, kill the program
    if(elapsedTime >= int(runTime)):
      print("Finished...")
      in_use = False

  return

#########################################################################################################

