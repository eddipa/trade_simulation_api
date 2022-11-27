import numpy as np
import matplotlib.pyplot as plt

import datetime

import os
from django.conf import settings

from django.db import models

from .servieces import BaseSimulator


class Simulation(models.Model):
    """
    Simulation model

    This model is used to simplify the process of generating the results of the
    Simulation.

    This model is NOT saved!

    Properties
    ----------
    account_size :
        initial account size

    total_trades :
        number of trades that we want to simulate

    risk_per_trade :
        the percentage of risk per trade. for example 2 represents 2 percent risk
        per trade

    win_rate :
        the percentage of winning in a single. aka: if we trade this strategy for
        100 times how many wins do we have.

    risk_reward :
        the percentage of profit erp trade devided by the risk percentage. 
        (REWARD/RISK). ironic! :D

    methods
    -------
    simulate :
        returns predict_profit result from BaseSimulator

    """
    account_size = models.DecimalField(
        max_digits=20, decimal_places=2, default=1000)
    total_trades = models.IntegerField(default=100)
    risk_per_trade = models.DecimalField(
        max_digits=4, decimal_places=2, default=2)
    win_rate = models.DecimalField(max_digits=4, decimal_places=2, default=70)
    risk_reward = models.DecimalField(
        max_digits=4, decimal_places=4, default=2)

    def simulate(self):
        """
        Simulatie mathod

        This method calls predict_prodit method from BaseSimulation class

        Returns
        -------
        simulation result in dictionary format

        """
        return BaseSimulator.predict_profit(self.account_size, self.total_trades, self.risk_per_trade, self.win_rate, self.risk_reward)

    def simulate_old(self):
        account = self.account_size
        accounts = [account]
        profits = []
        loss = []
        wins = []
        total_win = 0
        max_con_l = 0
        max_con_w = 0
        con_l = 0
        con_w = 0
        pre = 0
        rnd = list(np.round(np.random.uniform(1, 101, self.total_trades), 2))
        for i in range(len(rnd)):
            r = rnd[i]
            win = r <= self.win_rate
            risk = -np.round(account * self.risk_per_trade / 100, 2)
            profit_per_trade = abs(risk) * self.risk_reward
            profit = profit_per_trade if win else risk
            profits.append(profit)
            account += profit
            accounts.append(account)
            if profit > 0:
                total_win += 1
                wins.append(profit)
                con_l = 0
                if pre == 1:
                    con_w += 1
                    if con_w > max_con_w:
                        max_con_w = con_w
                pre = 1
            else:  # 0 is also a loss (spread + commissions)
                loss.append(abs(profit))
                con_w = 0
                if pre == -1:
                    con_l += 1
                    if con_l > max_con_l:
                        max_con_l = con_l
                pre = -1
        avg_win = np.mean(wins)
        avg_loss = np.mean(loss)
        max_win = np.max(wins)
        max_loss = np.max(loss)
        win_r = np.round(total_win / self.total_trades * 100, 2)
        rrr = np.round(avg_win / avg_loss, 2)
        profit_factor = np.round(np.sum(wins) / np.sum(loss), 2)
        net_profits = np.cumsum(profits)
        gain = np.round(accounts[-1] - self.account_size, 2)
        growth_rate = np.round(
            (accounts[-1] - self.account_size) / self.account_size * 100, 2)
        print("--- Trading Results ---\n")
        print("Total trades       : {}".format(self.total_trades))
        print("Wins               : {} / {}%".format(total_win, win_r))
        print("Average Win        : {}".format(np.round(avg_win, 2)))
        print("Average Loss       : {}".format(np.round(avg_loss, 2)))
        print("Max Win            : {}".format(np.round(max_win, 2)))
        print("Max Loss           : {}".format(np.round(max_loss, 2)))
        print("Max Cons. Wins     : {}".format(max_con_w))
        print("Max Cons. Loss     : {}".format(max_con_l))
        print("Risk Reward Ratio  : {}".format(rrr))
        print("Profit Factor      : {}".format(profit_factor))
        print("Risk per trade     : {}%".format(self.risk_per_trade))
        print("---")
        print("Initial Account    : {}".format(self.account_size))
        print("Profit             : {} / {}%".format(gain, growth_rate))
        print("Final Account      : {}".format(np.round(account, 2)))
        print()
        print("Results are compounded. Spread and commissions are not calculated.")

        result_dict = {}
        result_dict["Total trades"] = "{}".format(self.total_trades)
        result_dict["Wins"] = "{} / {}%".format(total_win, win_r)
        result_dict["Average Win"] = "{}".format(np.round(avg_win, 2))
        result_dict["Average Loss"] = "{}".format(np.round(avg_loss, 2))
        result_dict["Max Win"] = "{}".format(np.round(max_win, 2))
        result_dict["Max Loss"] = "{}".format(np.round(max_loss, 2))
        result_dict["Max Cons. Wins"] = "{}".format(max_con_w)
        result_dict["Max Cons. Loss"] = "{}".format(max_con_l)
        result_dict["Risk Reward Ratio"] = "{}".format(rrr)
        result_dict["Profit Factor"] = "{}".format(profit_factor)
        result_dict["Risk per trade"] = "{}%".format(self.risk_per_trade)
        result_dict["Initial Account"] = "{}".format(self.account_size)
        result_dict["Profit"] = "{} / {}%".format(gain, growth_rate)
        result_dict["Final Account"] = "{}".format(np.round(account, 2))

        self.net_profits = net_profits
        self.accounts = accounts

        return result_dict

    def img(self):
        fig, ax = plt.subplots(2, 1, figsize=(16, 10))
        ax[0].plot(self.net_profits)
        ax[1].plot(self.accounts)
        ax[1].axhline(self.account_size, color="#000000",
                      ls="-.", linewidth=0.5)
        ax[0].set_title("Equirty Curve")
        ax[1].set_title("Account Growth")

        basename = "imgfile"

        suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")

        filename = "_".join([basename, suffix])

        destination_path = os.path.join(settings.MEDIA_ROOT, filename + '.png')

        destination = open(destination_path, 'wb+')

        plt.savefig(destination, bbox_inches='tight')

        return destination_path
