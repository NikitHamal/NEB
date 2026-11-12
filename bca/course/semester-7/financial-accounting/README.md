# Financial Accounting — BCA 403 (Semester VII, 2 credits)

Conceptual framework and GAAP with Nepal's NFRS, the accounting equation and double entry, journalising with VAT and TDS, ledgers and T-accounts, subsidiary books and the trial balance with error rectification, bank reconciliation, depreciation and inventory valuation, final accounts with year-end adjustments, and ratio analysis with a SQLite double-entry ledger.

| Unit | Title | Hours |
|---|---|---|
| 1 | Conceptual Framework of Accounting, GAAP, NFRS and the Accounting Equation | 5 |
| 2 | Recording Transactions, Journal, VAT and TDS Entries, Ledger and T-Accounts | 7 |
| 3 | Subsidiary Books, Trial Balance and Error Rectification | 6 |
| 4 | Bank Reconciliation Statement | 6 |
| 5 | Depreciation and Inventory Valuation | 7 |
| 6 | Final Accounts with Year-End Adjustments | 8 |
| 7 | Ratio Analysis and a Computerised Ledger in SQLite | 6 |
| 8 | Introduction to Company Accounts: shares, debentures, forfeiture, redemption of preference shares | 9 |

## Verification

`bca/tools/check_accounting.py` plus `fill_script_outputs.py`: every Python block is executed and its output inserted; the checker recomputes each figure by an independent route (per-account balances instead of delta tracking, column sums, closed forms with exact fractions) and `--verify` demands that every expected output line and prose figure is present. The trial balance, balance sheet and DuPont identity are asserted to balance.

## Note on the code

The revised curriculum list maps Financial Accounting to BCA 403 (Semester VII); BCA 402 is Software Project Management. This book is registered under BCA 403 to match `CURRICULUM.md`. Nepal-specific rates (VAT 13%, corporate tax 25%, TDS on rent 10%) are used as teaching figures; confirm against the current Finance Act before filing anything real.


## Session 21: syllabus gap closed

Checked against the current TU BCA outline (7 units: theoretical framework, accounting process, BRS, inventories (and depreciation), final accounts of sole proprietors, **introduction to company accounts**). The book was missing the whole company-accounts unit (meaning, features and types of company, share capital and its kinds, debentures and their kinds, shares versus debentures, issue of shares and debentures, redemption of preference shares). It is now **Unit 8**, with four worked examples whose figures are recomputed by a Python block. Smaller gaps closed: qualitative characteristics and accounting policies (1.7), capital and revenue items with contingent assets and liabilities (2.8), stock taking (5.7) and the manufacturing account (6.8). Nepal-specific thresholds in 8.1 (private versus public company, SEBON, Rs 100 par) are stated as commonly taught; check the current Companies Act, 2063 and its amendments.
