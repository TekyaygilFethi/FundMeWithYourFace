from web3 import Web3


class FundAndWithdraw:
    def __init__(self, fund_me):
        self.fund_me = fund_me

    def fund(self, account, amount):
        self.fund_me.fund({"from": account, "value": amount})

    def withdraw(self, account):
        self.fund_me.withdraw({"from": account})

    def getEntranceFee(self):
        return Web3.fromWei(self.fund_me.getEntranceFee(), "ether")

    def setMinimumUSDThreshold(self, amount, account):
        self.fund_me.setMinimumUSDThreshold(amount, {"from": account})

    def seeAllFundsAndFunders(self, account):
        return self.fund_me.seeAllFundsAndFunders({"from": account})
