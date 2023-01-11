# VenmoAutoTransact
[![Python 3.11](https://img.shields.io/badge/Python-3.11-yellow.svg)](http://www.python.org/download/)


Automatically make venmo transactions between two debit card accounts according to a schedule. This can be used to meet minimum debit card transaction quantity for bank bonuses

## Installation:
1. `git clone https://github.com/shanedoolane/VenmoAutoTransact.git`
2. `pip install -r requirements.txt`

## Useage
1. Populate `credentials.py`:
   1. Get your `access_token`: https://github.com/mmohades/Venmo#usage
   2. Get target `user_id`: https://github.com/mmohades/Venmo#usage
   3. Fill out your email notification details in `credentials.py`: https://myaccount.google.com/apppasswords
4. Customize spend parameters in `main.py` according to your requirement
5. Run `main.py`
6. Wait for an email confirming the script has finished