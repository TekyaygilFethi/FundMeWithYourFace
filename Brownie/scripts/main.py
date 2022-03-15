import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from web3 import Web3
from scripts.helpers.fund_and_withdraw import FundAndWithdraw
from scripts.deploy import get_fund_me
from scripts.helpers.helpful_scripts import get_account

from Manager.user_manager import CheckUserRole


def main():
    account = get_account()
    input(
        "You should login before perform this action! Please prepare yourself for camera, please stand still and directly look to the camera. Please press 'Enter' key to login with your face id!"
    )
    name, role = CheckUserRole()
    if role is not None:
        print(f"Welcome {name}!")
        fund_me = get_fund_me()
        if fund_me != None:
            fund_and_withdraw_obj = FundAndWithdraw(fund_me)
            action_choice = None
            while action_choice != "q":
                action_choice = input(
                    """
                        Please enter your operation:\n
                        1. Fund\n
                        2. See minimum entrance fee (Please note that you will see this amount in eth format!)\n
                        3. Withdraw (for contract owner only!)\n
                        4. Set minimum USD Threshold (for contract owner only!)\n
                        5. See All Funds And Funders (for contract owner only!)\n
                        q. Quit
                    """
                )
                try:
                    if action_choice == "1":
                        fund_value = Web3.toWei(
                            input("Please enter your fund amount in ETH: "), "ether"
                        )
                        fund_and_withdraw_obj.fund(account, fund_value)
                        print(f"{fund_value} funded successfully!")

                    elif action_choice == "2":
                        print(fund_and_withdraw_obj.getEntranceFee())

                    elif action_choice == "3":
                        fund_and_withdraw_obj.withdraw(account)

                    elif action_choice == "4":
                        new_threshold = input(
                            "Please enter the USD amount of new threshold: "
                        )
                        fund_and_withdraw_obj.setMinimumUSDThreshold(
                            new_threshold, account
                        )

                    elif action_choice == "5":
                        print(fund_and_withdraw_obj.seeAllFundsAndFunders(account))

                    elif action_choice == "q":
                        break

                    else:
                        print("Please enter a valid input!")
                except Exception as e:
                    print(f"Couldn't complete operation: {e}")

        else:
            print("This contract has not been deployed. Contact the admin!")
    else:
        print("You couldn't login! Please try again!")
