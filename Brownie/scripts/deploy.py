import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpers.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    deploy_mocks,
)
from Manager.user_manager import CheckUserRole


def __deploy_fund_me(account):
    print("Deploying contract...")
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks(account)
        price_feed_address = MockV3Aggregator[-1].address
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def __get_pre_deployed_contract():
    try:
        fund_me_contract_obj = FundMe[-1]
        return fund_me_contract_obj
    except:
        return None


def main():
    input(
        "You should login before perform this action! Please prepare yourself for camera, please stand still and directly look to the camera. Please press 'Enter' key to login with your face id!"
    )
    name, role = CheckUserRole()
    if role == "Admin":
        print(f"Welcome {name}!")
        account = get_account()
        pre_deployed_fund_me = __get_pre_deployed_contract()
        if pre_deployed_fund_me is not None:
            deploy_choice = input(
                "This contract has been deployed before. Please enter y to deploy it again! If you enter another value it will not be deployed again.\n: "
            )
            if deploy_choice == "y":
                __deploy_fund_me(account)
        else:
            __deploy_fund_me(account)
    else:
        print("You don't have required authorization! ")


def get_fund_me():
    return __get_pre_deployed_contract()
