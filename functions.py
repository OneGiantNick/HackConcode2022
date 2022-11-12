import json
from web3 import Web3
import wallet_details

with open("data.json", "r") as f:
    data = json.load(f)

dbsol_contract_address = data["contract_address"]
users_abi, users_bytcode = data["users_abi"], data["users_bytecode"]
session_abi, session_bytecode = data["session_abi"], data["session_bytecode"]
appointment_abi, appointment_bytecode = (
    data["appointment_abi"],
    data["appointment_bytecode"],
)

# For connecting to ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337

# Deployer wallet details
my_address = wallet_details.my_address
private_key = wallet_details.private_key

db = w3.eth.contract(address=dbsol_contract_address, abi=users_abi)


def handleTransaction(transaction):
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    print("Sending Transaction!")
    # Sending txn
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    print("Waiting for transaction to finish...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Done!")
    return tx_receipt


def createUser(username, password):
    print(f"Attempting to create user: {username} with password: {password}")
    try:
        nonce = w3.eth.getTransactionCount(my_address)
        transaction = db.functions.createUser(username, password).buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": my_address,
                "nonce": nonce,
            }
        )
        handleTransaction(transaction)
        return "success"
    except:
        return "error"


def createAppointment(username, appointment_datetime):
    print(f"Making appointment for {username} at {appointment_datetime}")
    nonce = w3.eth.getTransactionCount(my_address)
    transaction = db.functions.createAppointment(
        username, appointment_datetime
    ).buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": my_address,
            "nonce": nonce,
        }
    )
    handleTransaction(transaction)


def login(username, password):
    print(f"Attempting to log in {username}")
    try:
        nonce = w3.eth.getTransactionCount(my_address)
        transaction = db.functions.login(username, password).buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": my_address,
                "nonce": nonce,
            }
        )
        tx_receipt = handleTransaction(transaction)
        # Process event
        log_to_process = tx_receipt["logs"][0]
        processed_log = db.events.loginEvent().processLog(log_to_process)
        session = processed_log["args"]["value"]
        return session
    except:
        return "error"


def logout(session):
    print(f"Attempting to log out from {session}")
    try:
        nonce = w3.eth.getTransactionCount(my_address)
        transaction = db.functions.logout(session).buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": my_address,
                "nonce": nonce,
            }
        )
        tx_receipt = handleTransaction(transaction)
        return session
    except:
        return "error"


def updateNewcomer(username, sex, height, weight):
    pass


def getUser(username):
    return db.functions.getUser(username).call()


def getUserFromSession(session_contract_address):
    session = w3.eth.contract(address=session_contract_address, abi=session_abi)
    return session.call().username()


def getUserAppointments(username):
    print(f"Generating appointments from {username}")
    try:
        nonce = w3.eth.getTransactionCount(my_address)
        transaction = db.functions.getUserAppointments(username).buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": my_address,
                "nonce": nonce,
            }
        )
        tx_receipt = handleTransaction(transaction)
        log_to_process = tx_receipt["logs"][0]
        processed_log = db.events.userAppointments().processLog(log_to_process)
        appointment_list = processed_log["args"]["appt"]
        return appointment_list
    except:
        return "error"


def getAllUsers():
    return db.functions.getAllUsers().call()


def getAllAppointments():
    return db.functions.getAllAppointments().call()
