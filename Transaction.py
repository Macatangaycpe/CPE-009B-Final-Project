#send
from dataclasses import dataclass
from typing import Dict, Any, Union

#storing account details using data class instead of the usual class declaration
@dataclass
class account_details:
    account_number: str
    account_name: str
    amount: float

#enter account details 
def validate_account(account_number: str, account_name: str) -> bool:
    #validation via number or name
    if not account_number or not account_name:
        return False
    return True

#amount //checks if the amount is not zero or less than 0
def validate_amount(amount: float) -> bool:
    return amount > 0

#generates a random 12 digit reference number
def reference_number(sequence_value: int) -> str:
    return f"{sequence_value:012d}"

current_sequence = 1

#confirmation //check transaction details via dictionary using the combination of string, float and boolean in the save file
def confirm_transaction(details: account_details) -> Dict[str, Union[str, float, bool, None]]:
    # confirmation step
    is_valid_account = validate_account(details.account_number, details.account_name)
    is_valid_amount = validate_amount(details.amount)
    
    # returns the status, the failed transaction message and no data
    if not (is_valid_account and is_valid_amount):
        return {
            "Status" : "Failed",
            "Message": "Invalid Transaction",
            "Data" : None
        }
    
    ref_num = reference_number(current_sequence)
    current_sequence += 1

    # displays transaction info using stored value from dictionary
    transaction_info = {
        "Status" : "Success",
        "Reference Number" : reference_number(current_sequence),
        "Account Name" : details.account_name,
        "Account Number" : details.account_number,
        "Amount" : details.amount,
    }
    
    return transaction_info 


#payment transaction

#bills
##government,electricity,internet,water

#bank
##loans, transfer

#credits
##shopping credits, game credits, load credits


#deposit
#amount
#confirmation
#transaction info

#withdraw
#amount
#confirmation
#transaction info

#confirmation 
#OTP/PIN/PASSWORD

#transaction info(receipt)
#name
#amount
#account details
#transaction details
#date
#time