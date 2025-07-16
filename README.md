# Wallet-Credit-Scoring-Model
 
This project provides a robust machine learning model to assign a credit score between 0 and 1000 to Aave V2 wallets based on their historical transaction behavior. The model is designed to be transparent, explainable, and easily extensible.

Project Overview
The goal of this project is to quantify wallet reliability from raw, on-chain transaction data. A higher score indicates a responsible and stable user, while a lower score reflects risky, bot-like, or potentially exploitative behavior.

The model uses a heuristic scoring algorithm, which is a rule-based machine learning model. This approach was chosen for its transparency, as it allows us to trace the exact factors that contribute to a user's score, a critical requirement for any credit system.

Feature Engineering
The model's intelligence comes from a set of carefully engineered features that transform raw transaction logs into a behavioral profile for each wallet. The key features include:

count_LiquidationCall: The number of times a user has been liquidated. This is the single most important indicator of high-risk behavior.

wallet_age_days: The time between a user's first and last transaction. A longer history suggests a more established and stable user.

repayment_ratio: The ratio of total assets repaid versus total assets borrowed. A ratio close to 1 indicates responsible borrowing.

borrow_to_deposit_ratio: The ratio of total borrowed value to total deposited value. A high ratio can indicate over-leveraging.

unique_assets_used: The number of different crypto assets a user has interacted with, showing their level of engagement with the protocol.

How to Run the Script
The entire process is packaged into a single, reusable Python script.

1. Prerequisites
Python 3.8+

A virtual environment (recommended)

2. Setup
First, clone the repository and set up a virtual environment:

# Clone the repository
git clone <your-repo-url>
cd <your-repo-name>

# Create and activate a virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\Activate
# On macOS/Linux:
source venv/bin/activate

3. Execute the Scoring Script
Run the script from your terminal, providing the path to the input JSON file.

--- Example usage:
--- python score_wallets.py path/to/user-transactions.json

The script will process the data and save the results to a file named wallet_scores.csv by default.

To specify a different output file, use the -o flag:

--- python score_wallets.py path/to/user-transactions.json -o my_scores.csv

