# EmailNewsUpdates
- Description:
  - When you're away from your computer and can't be bothered to look at the website, you can run this instead for automatic updates sent directly  to your gmail account.
  - This code will allow you to send yourself emails of the most recent news articles (with links), or you can send the balance sheet of any ticker (given that it's supported on yahoo finance). 

- Supported Websites:
  https://www.barrons.com/topics/technology 
  and 
  https://finance.yahoo.com/news

- Functions stored in AutoEmailer.py
- Main program run from Master_Emailer.py
- Gmail login credentials should be stored in 'Gmail_Login_Creds.txt' (Use only 2 lines in the text doc for this to work)
  - The first line in this file will be your username
  - The second line will be your gmail app password
  - Check out this short tutorial to set up your gmail account so your program can log in: 
    - Title: How to Send Emails Using Python - Plain Text, Adding Attachments, HTML Emails, and More
    - Link: https://www.youtube.com/watch?v=JRCJ6RtE3xU
    - Timestamps: 0:00-2:25
    - DO NOT SHARE THIS PASSWORD (OR ANY OF YOUR PASSWORDS) WITH ANYONE
  
- Run the code using: 'python3 Master_Emailer.py' in your terminal
  - You will be prompted for what you would like to do from there
    - 1: Send automatic news updates for a specified time period and between a specified time interval
    - 2: Send the balance sheet of a specific ticker
  - After all of this information is entered, just let it run.
 
- BUGS:
  - If by chance the code doesn't run the first time through, just wait a few minutes and try it out again. I still need to implement some try statements into the code
    
