import time, uuid
from .models import *


def generateRefCode():
    code = str(uuid.uuid4()).replace("-","")[:6]
    return code


def runInvestmentProcess(instance):
    # if a saved investment was altered(not created) and status is approved 
    if instance.status == 'approved':
        if instance.returns < instance.amount:
            instance.returns = instance.amount
            instance.save()
    # for each day
    for each_day in range(instance.package.duration_in_days):
        print(instance.returns)
        # checking to make sure investment returns isn't exceeded
        if instance.returns < instance.roi:
            # sleep for 1day = 86400seconds
            time.sleep(10)
            # accumulate or add profits to investment returns
            instance.returns = instance.returns + instance.daily_profit
            instance.save()
            # checking to see if investment plan is completed
            if instance.returns == instance.roi:
                if instance.status != 'completed':
                    account = Account.objects.get(user=instance.user)
                    account.balance += instance.returns
                    account.save()
                    instance.status = 'completed'
                    instance.save()
                    break