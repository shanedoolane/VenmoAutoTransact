from venmo_api import Client
import numpy as np
import random
import yagmail
import datetime
import math
import pytz
import time
from credentials import device_id, access_token, from_email, to_email, email_password, funding_source_id , target_user_id
pacific = pytz.timezone('US/Pacific')

# initialize the client:
client = Client(access_token=access_token)


# Define the parameters for spend:
max_spend = 0.39  # total amount to spend across all trnasactions in the series
transaction_qty = 5  # number of transactions to make
min_time = 3  # minimum time between transactions
max_time = 6  # maximum time between transactions


# Generate the transaction values using the dirichlet distribution
values = max_spend * np.random.dirichlet([10] * transaction_qty, size=1)[0]

# Generate the payment message string
chinese_characters = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十',
                      '百', '千', '万', '亿', '上', '中', '下', '左', '右',
                      '天', '地', '人', '我', '你', '他', '她', '它', '谁',
                      '什', '么', '的', '是', '了', '有']
string_list = []
for i in range(transaction_qty):
    string_list.append(''.join(random.sample(chinese_characters, 20)))


# zip the data
data_set = list(zip(values, string_list))

# generate the empty log string and counters
logstr = ''
transacted = 0.0
attempted_qty = 0

try:
    amount = 0
    for amount, note in data_set:

        # clean the amount (round down to two decimal):
        amount = math.floor(amount * 100) / 100

        # validate transaction with tests
        if transacted + amount > max_spend:
            raise ValueError('Transaction would exceed max spend')
        if attempted_qty + 1 > transaction_qty:
            raise ValueError('Transaction would exceed max transaction qty')
        if note == '' or None:
            raise ValueError('Note string invalid')
        if note == '' or None:
            raise ValueError('Note string invalid')
        if amount <= 0:
            raise ValueError('Transaction for 0.00 cant be attempted')
        transaction_succeed = False
        # Attempt the transaction
        client.payment.send_money(amount=amount,
                                  note=note,
                                  target_user_id=target_user_id,
                                  funding_source_id=funding_source_id)
        transaction_succeed = True
        print(f'Transaction Succeeded at {str(datetime.datetime.now(pacific))[:-13]}, amount: ${amount:,.2f}, Note: {note}')
        logstr += f'${amount:,.2f} ---> ' + str(datetime.datetime.now(pacific))[:-13] + ' [SUCCESS]\n'
        transacted += amount
        attempted_qty += 1

        # Start the waiting period
        sleep_time = random.uniform(min_time, max_time)
        print(f"Sleeping for {sleep_time} minutes")
        time.sleep(sleep_time * 60)

except Exception as e:
    print(e)
    now = str(datetime.datetime.now(pacific))[:-13]

    if not transaction_succeed:
        logstr += f'${amount:,.2f} ---> ' + str(datetime.datetime.now(pacific))[:-13] + ' [FAILURE]\n'

    yag = yagmail.SMTP(from_email, email_password)
    contents = [
        f'Auto Venmo transaction failed at {now} (PT)\n\nAttempted amount: ${amount:,.2f}\n\nTraceback Exception: {e}\n\nTransaction Log:\n{logstr}']
    yag.send(to_email, 'Venmo Transaction Failed', contents)
    pass
else:
    now = datetime.datetime.now(pacific)
    yag = yagmail.SMTP(from_email, email_password)
    contents = [
        f'Auto Venmo Completed {now} (PT)\n\nTotal Amount Transacted: ${transacted:,.2f}\n\nNumber of Transactions: {attempted_qty}\n\nTransaction Log:\n{logstr}']
    yag.send(to_email, 'Venmo Transaction Completed', contents)
    print('Done')
    pass
