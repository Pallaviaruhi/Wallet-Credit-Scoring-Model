

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import argparse
import sys

def load_and_clean_data(file_path):
    
    try:
        df = pd.read_json(file_path)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(1) # Exit the script
    except ValueError:
        print(f"Error: The JSON file '{file_path}' is malformed.")
        sys.exit(1)

    # Flatten the nested 'actionData'
    action_data_df = pd.json_normalize(df['actionData'])
    
    # Combine with essential top-level columns
    df_cleaned = pd.concat([
        df[['userWallet', 'timestamp']],
        action_data_df[['type', 'amount', 'assetSymbol']]
    ], axis=1)

    # Rename for consistency
    df_cleaned.rename(columns={'userWallet': 'user_id', 'assetSymbol': 'reserve_symbol'}, inplace=True)
    
    # Convert data types
    df_cleaned['timestamp'] = pd.to_datetime(df_cleaned['timestamp'], unit='s')
    df_cleaned['amount'] = pd.to_numeric(df_cleaned['amount'], errors='coerce')
    df_cleaned.dropna(subset=['amount'], inplace=True)
    
    return df_cleaned

def engineer_features(df):
    """Engineers features for each user from the cleaned data."""
    print("Engineering features...")
    user_summary = df.pivot_table(
        index='user_id',
        columns='type',
        values='amount',
        aggfunc=['count', 'sum'],
        fill_value=0
    )
    user_summary.columns = ['_'.join(col).strip() for col in user_summary.columns.values]

    # Calculate wallet age and unique assets
    wallet_age = df.groupby('user_id')['timestamp'].agg(['min', 'max'])
    user_summary['wallet_age_days'] = (wallet_age['max'] - wallet_age['min']).dt.days
    user_summary['unique_assets_used'] = df.groupby('user_id')['reserve_symbol'].nunique()

    # Calculate ratios
    sum_repay = user_summary.get('sum_Repay', 0)
    sum_borrow = user_summary.get('sum_Borrow', 1) # Default to 1 to avoid division by zero
    sum_deposit = user_summary.get('sum_Deposit', 1)
    
    user_summary['repayment_ratio'] = (sum_repay / sum_borrow)
    user_summary['repayment_ratio'] = user_summary['repayment_ratio'].replace([np.inf, -np.inf], 0).fillna(0)
    user_summary['repayment_ratio'] = user_summary['repayment_ratio'].apply(lambda x: min(x, 1.0))

    user_summary['borrow_to_deposit_ratio'] = (sum_borrow / sum_deposit)
    user_summary['borrow_to_deposit_ratio'] = user_summary['borrow_to_deposit_ratio'].replace([np.inf, -np.inf], 0).fillna(0)

    # Ensure all possible transaction type columns exist
    all_txn_types = ['Deposit', 'Borrow', 'Repay', 'RedeemUnderlying', 'LiquidationCall']
    for t_type in all_txn_types:
        for agg in ['count', 'sum']:
            col = f'{agg}_{t_type}'
            if col not in user_summary.columns:
                user_summary[col] = 0
                
    
    return user_summary

def calculate_scores(features_df):
    """Calculates and scales the credit score based on features."""
  
    score_df = features_df.copy()
    
    # Start with a base score
    score_df['credit_score'] = 500.0
    
    # Apply scoring rules
    score_df['credit_score'] -= score_df['count_LiquidationCall'] * 250
    score_df['credit_score'] += np.log1p(score_df['wallet_age_days']) * 20
    score_df['credit_score'] += score_df['repayment_ratio'] * 150
    score_df['credit_score'] -= score_df['borrow_to_deposit_ratio'] * 100
    score_df['credit_score'] += score_df['unique_assets_used'] * 10
    
    # Scale the score to a 0-1000 range
    scaler = MinMaxScaler(feature_range=(0, 1000))
    scores = score_df['credit_score'].values.reshape(-1, 1)
    score_df['final_score'] = scaler.fit_transform(scores).astype(int)
    
    return score_df

def main():
    """Main function to run the entire pipeline."""
    parser = argparse.ArgumentParser(description="Generate credit scores for Aave wallets from transaction data.")
    parser.add_argument("input_file", help="Path to the input JSON transaction file.")
    parser.add_argument("-o", "--output_file", default="wallet_scores.csv", help="Path to save the output CSV file (default: wallet_scores.csv).")
    
    args = parser.parse_args()

    # Run the pipeline
    cleaned_data = load_and_clean_data(args.input_file)
    features = engineer_features(cleaned_data)
    final_scores = calculate_scores(features)
    
    # Prepare and save the output file
    output_df = final_scores[['final_score']].reset_index()
    
    print(f"Saving scores to '{args.output_file}'...")
    output_df.to_csv(args.output_file, index=False)
    print(f"Success! Scores saved to '{args.output_file}'.")

if __name__ == "__main__":
    main()