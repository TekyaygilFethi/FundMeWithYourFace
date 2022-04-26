# Fund Me With Your Face

This project combines the power of Brownie and OpenCV for creating an elegant way of logging in before making operations on Blockchain. With this project, you can fund or withdraw these funds by logging in with your face real time. Did I mention that this project compatible with only Rinkeby Network?

# Program Life Cycle

1. Compile the Solidity(.sol) files
2. If you are admin deploy the contract by logging ing with your face
3. Make operations by logging in with your face


# Folder Structure

To assure the program is working, there are folder structure rules to follow. 

1. Brownie structure exists on Brownie folder

2. Your images which will help to be recognized and Excel file which holds the user data (such as name, role, id etc) exists in Data Folder 

3. The module that allows your pc to recognize who you are by webcam exists in FaceRecognition folder

4. Your modules that performs mid operations such as user control according to the read value from webcam exists in Manager folder

## .env file

In Brownie folder, create an .env file. This file should contain secret information for your Brownie part of your application
```bash
PRIVATE_KEY=0x{YOUR_PRIVATE_KEY}
WEB3_INFURA_PROJECT_ID={YOUR_ID}
ETHERSCAN_TOKEN={YOUR_ETHERSCAN_TOKEN}
```
PRIVATE_KEY is the private key of your Rinkeby account
WEB3_INFURA_PROJECT_ID is the ID of the project you've created on https://infura.io/
ETHERSCAN_TOKEN is a token that allows you to deploy your contract on chain

## brownie-config.yaml

In Brownie folder, you can see brownie-config.yaml file. This file contains configurations for your Brownie app. To go one by one:
### dependencies
dependencies are the global sol files and by giving their Github addresses (because we cant pip install them) we can inform Brownie about where these files can be found.

### compiler/solc/remappings
remappings allows you to assign links to a keywords. For example in;
```bash
"@chainlink=smartcontractkit/chainlink-brownie-contracts@0.4.0"
```
line, we are saying Brownie that when it sees ```@chainlink```, it will replace it with ```smartcontractkit/chainlink-brownie-contracts@0.4.0```


### dotenv
dotenv allows Brownie to recognzie your .env file

### networks
networks section holds the information which varies by network.

verify is a flag that tells Brownie the contract will be deployed to the chain. If it is True, then the contract will be deployed.

eth_usd_price_feed holds the address of currency converter contract and allows us to get latest Currency price of ETH/USD pair.

### wallets
wallets holds the private key of your accounts such as Rinkeby accounts.


# Users

There are 2 types of authenticated users. One is Admin and the other one is Standard. The only difference between them is the authorization of deploying contract. Only admin users can deploy contracts. Bot users can perform operations on application which we will be informed in a moment.




# Setting Up The Program

1. Clone the project
```bash
git clone https://github.com/TekyaygilFethi/FundMeWithYourFace.git
```

2. First create a virtual environment. Assume we want to give myenv as a venv name.
```bash
python -m venv myvenv
```

3. Activate the virtual environment
FOR MAC:
```bash
source myvenv/bin/activate
```
FOR WINDOWS:
```bash
myvenv/Scripts/activate
```


4. Install the required dependencies from requirements.txt file:
```bash
pip install -r requirements.txt
```
5. You must set your users and their images first. To set users and their roles, Please navigate to the Data/Excel/Users.csv file. This csv file contains 3 columns, ID, Name and Role.

- ID: This column ensures users are not being merged when they have the same name and surname.
- Name Surname: Name and surname of the user
- Role: Role of the user


6. Add your users and please be careful about ID's. ID column should be **UNIQUE!**

7. Add your user images to Data/images folder. Please be careful about naming convetion of images.
```bash
{Name Surname}_{ID}
```
For instance, for Fethi Tekyaygil which has ID 1 should have his photo like this:

```bash
Fethi Tekyaygil_1.jpg
```

8. Navigate to the Brownie Folder, we must compile the sol files in order to work with them.
```bash
>> cd Brownie
>> brownie compile
```

9. For deploying a contract, you must be registered as admin. After that when in Brownie folder in terminal, execute the following command for Rinkeby network:
```bash
brownie run scripts/deploy.py --network rinkeby
```
After pressing enter, you will be asked for webcam login with this message.
```
You should login before perform this action! Please prepare yourself for camera, please stand still and directly look to the camera. Please press 'Enter' key to login with your face id!
```
When you press the enter, your webcam will be opened and once it detects you, you will be logged in. If no one or unauthorized user (which does not takes place in xlsx or images folder) the program will wait 10 seconds before closing to capture authorized user.
If you are authorized as admin, you should see a welcome message with your name in it ```Welcome {Your Name Surname}!``` and the contract will be deployed. If this contract has deployed previously, the program will ask you if it should create a new one or use the existing one.

```
This contract has been deployed before. Do you want to deploy it again?
```
# Running The Program

1. For open the application, execute the following command for Rinkeby network in Brownie folder:
```bash
brownie run scripts/main.py --network rinkeby
```
**_Careful, the contract must be deployed first, if not the program will inform you!_**

```
This contract has not been deployed. Contact the admin!
```

2. Then you will be asked for webcam login again. Press enter to login with your face.

3. Then select your operation. Operations are:
- Fund (For non-contract owner only): With this method you can find any amount of ETH. Careful, you should enter the amount in ETH!
- See Minimum Entrance Fee in ETH: See the minimum value for funding.
- Withdraw (For contract owner only): Withdraw all the money funded.
- Set Minimum Fund Amount (For contract owner only): Set minimum amount required for funding in USD. Careful, you should enter the amount in USD!
- See All Funds And Funders (For contract owner only): See all funders and the fund values.
- Quit: Exit the program


# CONGRATULATIONS!
Congratulations you've come so far! When you work this project on local network, some errors and unstable actions happening. If you can find why and PR them, I will announce you on my LinkedIn as a problem solver! Feel free to Pull Request :)
