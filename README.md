# HackConcode2022
HealthUP - Our project for HackConcode2022


HealthUP is a webapp that aims to help users manage their health options. It runs on a decentralised user ID management system. Users are entered into the system via peer-to-peer validation and the data is stored on the blockchain. HealthUP currently supports creation of user profiles, booking appointments and updating of user info(to a certain extent, some particulars are not yet in the constructor).

## Setting Up

### Pip Modules
Use the package manager [pip] (https://pip.pypa.io/en/stable/) to install the prequisites found in requirements.txt

```bash
pip install flask
pip install py-solc-x
pip install web3
pip install pytz
```

### Ganache
This project runs off the ganache simulated blockchain, install ganache here (https://trufflesuite.com/ganache/)

Once you have downloaded ganache, start by creating a new project by clicking on *new workspace*.

<img width="854" alt="image" src="https://user-images.githubusercontent.com/47775170/200106196-ae739378-32a1-487c-aeac-6cb386ba3d5e.png">

click on *save workspace*.

<img width="846" alt="image" src="https://user-images.githubusercontent.com/47775170/200106321-98bad9c8-e9d4-41ef-8b78-115cbfff5b56.png">

You will be brought to the following screen.

<img width="846" alt="image" src="https://user-images.githubusercontent.com/47775170/200106343-4bfe596a-63e8-47ad-8052-a80c7c89c7f3.png">

Choose any of the wallets to use as the deployer wallet. Copy and paste the address and private key into *deploy.py*. You can find these by clicking on the key icon next to the wallet. **Below is a sample wallet. Do not use it. Use a wallet that is on your simulated ganache blockchain**

<img width="501" alt="image" src="https://user-images.githubusercontent.com/47775170/200106405-5169730d-7233-434b-8c60-145d3c3214ba.png">




## Usage

### Deploy.py

Start the project by running *deploy.py* it is located at /deploy.

```bash
/deploy.py
```

### Running the flask server

Start the flask server in order to interact with the webpage.

```bash
py app.py
```

Users will now be able to sign up and log in.

### Session management

Upon logging in, the user's session contract address is stored in a cookie. We configured the session to be valid for 30 mins before the user is auto logged out or upon closing of the tab.

### Directories

**Dashboard**

Dashboard will greet the user and show the latest health events.

**Appointments**

Displays all appointments user has and also allows the booking of more apppointments with their local healthcare institutions

**My Health**

Shows users BMI, health records and particulars (records and particulars are placeholders as no time to implement but it functions the same as BMI) users will be able to update these values.

## Documentation

### db.sol

The smart contract that django interacts with to store data on the blockchain. Written in solidity

#### Session

Smart contract to store individual sessions of users who log in. Stores username, login date and logout date

