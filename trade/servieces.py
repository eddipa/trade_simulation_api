import numpy as np


class BaseSimulator:
    @staticmethod
    def predict_profit(account_size, total_trades, risk_per_trade, win_rate, risk_reward, print_results=False):
        """
        Simulation method

        This method generates simulation data in a dictionary format

        @ this method is from the following article by Atilla Yurtseven:
        https://towardsdatascience.com/how-to-simulate-trades-in-python-7e613c83fd5a

        Parameters
        ----------
        arg1 :
            account_size

        arg2 :
            total_trades

        arg3 :
            risk_per_trade

        arg4 :
            win_trade

        arg5 :
            risk_reward

        arg6 :
            print_results = False

        Returns
        -------
        dict

        """
        account = account_size
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
        rnd = list(np.round(np.random.uniform(1, 101, total_trades), 2))
        for i in range(len(rnd)):
            r = rnd[i]
            win = r <= win_rate
            risk = -np.round(account * risk_per_trade / 100, 2)
            profit_per_trade = abs(risk) * risk_reward
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
        win_r = np.round(total_win / total_trades * 100, 2)
        rrr = np.round(avg_win / avg_loss, 2)
        profit_factor = np.round(np.sum(wins) / np.sum(loss), 2)
        net_profits = np.cumsum(profits)
        gain = np.round(accounts[-1] - account_size, 2)
        growth_rate = np.round(
            (accounts[-1] - account_size) / account_size * 100, 2)

        result_dict = {}
        result_dict["Total trades"] = "{}".format(total_trades)
        result_dict["Wins"] = "{} / {}%".format(total_win, win_r)
        result_dict["Average Win"] = "{}".format(np.round(avg_win, 2))
        result_dict["Average Loss"] = "{}".format(np.round(avg_loss, 2))
        result_dict["Max Win"] = "{}".format(np.round(max_win, 2))
        result_dict["Max Loss"] = "{}".format(np.round(max_loss, 2))
        result_dict["Max Cons. Wins"] = "{}".format(max_con_w)
        result_dict["Max Cons. Loss"] = "{}".format(max_con_l)
        result_dict["Risk Reward Ratio"] = "{}".format(rrr)
        result_dict["Profit Factor"] = "{}".format(profit_factor)
        result_dict["Risk per trade"] = "{}%".format(risk_per_trade)
        result_dict["Initial Account"] = "{}".format(account_size)
        result_dict["Profit"] = "{} / {}%".format(gain, growth_rate)
        result_dict["Final Account"] = "{}".format(np.round(account, 2))

        if (print_results):
            print("--- Trading Results ---\n")
            print("Total trades       : {}".format(total_trades))
            print("Wins               : {} / {}%".format(total_win, win_r))
            print("Average Win        : {}".format(np.round(avg_win, 2)))
            print("Average Loss       : {}".format(np.round(avg_loss, 2)))
            print("Max Win            : {}".format(np.round(max_win, 2)))
            print("Max Loss           : {}".format(np.round(max_loss, 2)))
            print("Max Cons. Wins     : {}".format(max_con_w))
            print("Max Cons. Loss     : {}".format(max_con_l))
            print("Risk Reward Ratio  : {}".format(rrr))
            print("Profit Factor      : {}".format(profit_factor))
            print("Risk per trade     : {}%".format(risk_per_trade))
            print("---")
            print("Initial Account    : {}".format(account_size))
            print("Profit             : {} / {}%".format(gain, growth_rate))
            print("Final Account      : {}".format(np.round(account, 2)))
            print()
            print("Results are compounded. Spread and commissions are not calculated.")

        return result_dict


def simulate(account_size, total_trades, risk_per_trade, win_rate, risk_reward):
    account = account_size
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
    rnd = list(np.round(np.random.uniform(1, 101, total_trades), 2))
    for i in range(len(rnd)):
        r = rnd[i]
        win = r <= win_rate
        risk = -np.round(account * risk_per_trade / 100, 2)
        profit_per_trade = abs(risk) * risk_reward
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
    win_r = np.round(total_win / total_trades * 100, 2)
    rrr = np.round(avg_win / avg_loss, 2)
    profit_factor = np.round(np.sum(wins) / np.sum(loss), 2)
    net_profits = np.cumsum(profits)
    gain = np.round(accounts[-1] - account_size, 2)
    growth_rate = np.round(
        (accounts[-1] - account_size) / account_size * 100, 2)
    print("--- Trading Results ---\n")
    print("Total trades       : {}".format(total_trades))
    print("Wins               : {} / {}%".format(total_win, win_r))
    print("Average Win        : {}".format(np.round(avg_win, 2)))
    print("Average Loss       : {}".format(np.round(avg_loss, 2)))
    print("Max Win            : {}".format(np.round(max_win, 2)))
    print("Max Loss           : {}".format(np.round(max_loss, 2)))
    print("Max Cons. Wins     : {}".format(max_con_w))
    print("Max Cons. Loss     : {}".format(max_con_l))
    print("Risk Reward Ratio  : {}".format(rrr))
    print("Profit Factor      : {}".format(profit_factor))
    print("Risk per trade     : {}%".format(risk_per_trade))
    print("---")
    print("Initial Account    : {}".format(account_size))
    print("Profit             : {} / {}%".format(gain, growth_rate))
    print("Final Account      : {}".format(np.round(account, 2)))
    print()
    print("Results are compounded. Spread and commissions are not calculated.")
    fig, ax = plt.subplots(2, 1, figsize=(16, 10))
    ax[0].plot(net_profits)
    ax[1].plot(accounts)
    ax[1].axhline(account_size, color="#000000", ls="-.", linewidth=0.5)
    ax[0].set_title("Equirty Curve")
    ax[1].set_title("Account Growth")
    plt.show()
