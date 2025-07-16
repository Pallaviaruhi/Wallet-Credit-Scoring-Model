# Aave V2 Wallet Credit Score Analysis

This document provides an analysis of the credit scores generated for Aave V2 wallets. The analysis validates the effectiveness of the scoring model by examining the overall score distribution and the distinct behavioral patterns of wallets at the top and bottom of the score range.

-----

## Overall Score Distribution

The distribution of scores across the entire user base provides a high level view of the platform's overall risk profile.

The histogram clearly shows that the **vast majority of wallets have very high credit scores**, with a massive concentration in the 950-1000 range. This indicates that the user base in this dataset is overwhelmingly healthy and engages in low-risk behavior.

This distribution is a strong sign that the model is working as intended. It successfully separates the large population of safe users from the small minority of risky users, who make up the long, flat tail on the left.

-----

## Analysis of User Behavior

By examining the statistical profiles of the highest and lowest-scoring wallets, we can confirm the logic of the scoring model.

### High-Scorer Profile (Score \> 800)

This group represents the most reliable and lowest-risk users. Their behavior is characterized by:

  * **Exceptional Safety:** The most crucial trait is their aversion to risk. The data shows that the vast majority of these users have **never been liquidated**, which is the strongest possible indicator of safe protocol usage.
  * **"Saver" Profile:** These users are primarily liquidity providers. They consistently deposit assets to earn interest but do not actively borrow against their collateral. This makes them extremely low-risk and a valuable source of liquidity for the protocol.
  * **Established Presence:** These are generally not new or speculative accounts. They have an established history on Aave, demonstrating long-term engagement and stability.

### Low-Scorer Profile (Score \< 200)

The analysis reveals that the lowest scores are assigned to a **single, highly anomalous wallet**, demonstrating the model's effectiveness as an outlier detection system. This wallet's behavior is extremely risky:

  * **Extreme Number of Liquidations:** This wallet was liquidated **26 times**, a clear sign of unsustainable and reckless behavior.
  * **Insolvent Behavior:** The wallet's total borrow amount is nearly **7 times larger** than its total deposits, showing a pattern of taking on uncollateralized debt.
  * **Hyper-Active & Bot-Like:** The account's high volume of transactions over a moderate time frame suggests aggressive, automated activity designed to push the limits of the protocol.

-----

## Conclusion

The credit scoring model is highly effective. It successfully distinguishes between the overwhelming majority of safe, stable "Savers" and the rare, extremely high-risk outliers. The model fulfills its objective by assigning high, granular scores to reliable users while flagging dangerous behavior with rock-bottom scores, providing a clear and actionable measure of wallet risk.