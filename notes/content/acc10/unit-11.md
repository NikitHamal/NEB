---
subject: Accountancy
grade: 10
title: Store Accounting (जिन्सी लेखा)
unit: 11
hours: 4
area: Government Accounting of Nepal
---

A government office does not spend all its money on salaries and services. It also buys **goods** — furniture, computers, stationery, uniforms, spare parts, medicines, fuel — and those goods have to be looked after. Somebody must know how many chairs were received, how many were issued to which room, how many are in the store today, and where the tenth one went. That record is the **store account (जिन्सी लेखा)**. This unit explains what store accounting is and why it matters, the formats it uses, the main store formats, and how the store is verified.

::: key What the examiner tests here
Group A asks: "What is store accounting?", "Write any two importance of store accounting", "What is a bin card?". Group B asks for the objectives and importance of store accounting, or the main store formats. Learn the names of the formats with one line each — the जिन्सी दाखिला फाराम, the जिन्सी निकासा फाराम, the store ledger, the bin card and the stock statement.
:::

## 11.1 Store accounting: introduction, objectives and importance

**Store accounting (जिन्सी लेखा)** is the branch of government accounting that records the **receipt, storage, issue and balance of goods (जिन्सी)** held by a government office, in quantity and in value, so that the goods can be accounted for at any moment and at any later date.

The word **जिन्सी** covers both kinds of goods an office holds: **consumable** goods, which are used up — stationery, ink, cleaning materials, medicines, fuel — and **non-consumable (durable)** goods, which keep their identity — furniture, computers, vehicles, machines, musical instruments. Both must be entered in the store account the moment they are received, and both must be issued against a written requisition.

**Objectives.**

1. To record every article **received**, with its quantity, specification, value, supplier and the voucher by which it was bought.
2. To record every article **issued**, with the date, the quantity and the person or section that received it.
3. To show the **stock balance** at any time, so that the office knows what it holds without a physical count.
4. To **prevent loss, misuse and theft**, because an article that has to be signed for is far less likely to disappear.
5. To provide the **evidence** an auditor needs: the purchase voucher, the receipt entry, the issue entry and the balance must agree.
6. To help **budgeting**, by showing what is already in stock and what must be bought next year.

**Importance.** In a government office, goods are public property. A chair bought with public money does not become the property of the clerk who uses it, and it cannot be taken home, sold or given away. Store accounting is what makes that rule enforceable: it ties every article to a document and a person. It also protects the honest officer, because a written store record is the only defence against a later allegation that goods were received and never accounted for.

```figure caption="The life of a store article. Each arrow is a document, and the balance in the store ledger is the running result."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.1,2.5))
ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,6)
steps=[(0.2,"Purchase and\nbill passed"),(2.1,"Received into store\n(जिन्सी दाखिला)"),
       (4.0,"Entered in the\nstore ledger and bin card"),(5.9,"Issued on requisition\n(जिन्सी निकासा)"),
       (7.8,"Physical verification\nand stock statement")]
for x,t in steps:
    ax.add_patch(FancyBboxPatch((x,2.3),1.75,1.7,boxstyle="round,pad=0.05",
                 fc="#eaf1ff" if x<4 else "#f6f8fc", ec=ACCENT if x<4 else MUTED, lw=1.0))
    ax.text(x+0.875,3.15,t,ha='center',va='center',fontsize=5.6,color=INK)
for a,b in ((1.95,2.1),(3.85,4.0),(5.75,5.9),(7.65,7.8)):
    ax.add_patch(FancyArrowPatch((a,3.15),(b,3.15),arrowstyle="-|>",mutation_scale=8,color=INK,lw=1.0))
ax.text(5.0,1.2,"No article may move without a document",ha='center',fontsize=6.4,color=MUTED)
```

## 11.2 Formats used in store accounting

| Format | What it records |
|---|---|
| **जिन्सी दाखिला फाराम (goods received form)** | An article received into the store: date, description, specification, quantity, unit, value, supplier and the purchase voucher |
| **जिन्सी निकासा फाराम (issue form)** | An article issued out of the store: date, description, quantity, the requisition and the receiving officer's signature |
| **जिन्सी खाता (store ledger)** | The head-wise record of every article, showing receipts, issues and the balance |
| **बिन कार्ड (bin card)** | A card kept on the shelf with the article itself, showing the same receipts, issues and balance |
| **जिन्सी मौज्दात फाँटबारी (stock statement)** | The periodic statement of goods in hand, by head, used for reporting and for budgeting |
| **जिन्सी जाँच फाराम (verification form)** | The record of the physical verification of the store, with the differences found |
| **भौचर (voucher)** | The accounting entry that brings the store figures into the accounts |

The **rule** is the same as everywhere in government accounting: no article may be received, issued or written off without the prescribed form, signed by the officer authorised to sign it.

## 11.3 Main store formats

**The जिन्सी दाखिला फाराम (goods received form)** is filled in when the goods arrive. It is compared with the purchase order and the bill; if the quantity or the specification does not match, the goods are not accepted, or are accepted only in part and the supplier is informed in writing. Once the form is signed, the article exists in the office's records.

**The जिन्सी निकासा फाराम (issue form)** is filled in when goods leave the store. The section that needs the article sends a **requisition**, and the storekeeper issues against it. The person who receives the goods signs the form — and that signature is what makes him answerable for the article afterwards.

**The store ledger (जिन्सी खाता)** is the main book. One page, or one account, is opened for each article, and the page carries the date, the particulars, the receipt quantity, the issue quantity, the balance quantity, the rate and the value. Government store ledgers are commonly kept in the **continuous balance** form, so the balance can be read at a glance after every entry rather than being struck at the end of the month.

**The bin card (बिन कार्ड)** is a small card attached to the shelf or the bin where the article is kept. It carries the same figures as the store ledger — receipt, issue, balance — and it exists so that a person standing at the shelf knows what is there without walking to the office. The storekeeper sees immediately when stock is running low. The **card and the ledger must agree**; when they do not, the difference is investigated.

```figure caption="A continuous-balance store ledger page. Receipts add, issues subtract, and the balance is struck after every entry — which is why the page is called continuous."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.1,2.4))
ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,6)
cols=["Date","Particulars","Receipt","Issue","Balance"]
xs=[0.2,1.5,4.4,5.9,7.4]
ws=[1.3,2.9,1.5,1.5,1.5]
ax.add_patch(Rectangle((0.2,4.6),8.7,1.0,fc="#eaf1ff",ec=INK,lw=1.0))
for x,w,c in zip(xs,ws,cols):
    ax.add_patch(Rectangle((x,4.6),w,1.0,fc="#eaf1ff",ec=INK,lw=1.0))
    ax.text(x+w/2,5.1,c,ha='center',va='center',fontsize=7,color=INK,weight='bold')
rows=[("01/04","Received from Nepal Trading","50","","50"),
      ("05/04","Issued to account section","","10","40"),
      ("12/04","Received from Nepal Trading","25","","65"),
      ("20/04","Issued to store room","","15","50")]
for i,r in enumerate(rows):
    y = 3.6 - i*0.95
    for x,w,v in zip(xs,ws,r):
        ax.add_patch(Rectangle((x,y),w,0.95,fc="white",ec=MUTED,lw=0.8))
        ax.text(x+w/2,y+0.47,v,ha='center',va='center',fontsize=6.4,color=INK)
ax.text(5.0,0.2,"Article: Steel almirah, size 4 ft — head 31121",ha='center',fontsize=6.2,color=MUTED)
```

```photo id="acc10/warehouse" caption="A well-arranged store. Every shelf location answers to a bin card, and the bin card answers to the store ledger." width="78"
```

## 11.4 Use of the store account and store verification

**Use of the store account.** The store account is read by three different people for three different reasons. The **storekeeper** uses it to know what is in stock and what to requisition. The **accounts section** uses it to value the goods and to bring the receipts into the accounts. The **auditor** uses it to trace an article from the bill to the store ledger, from the store ledger to the bin card, and from the bin card to the shelf — and to see whether the article that was issued is still being used by the office that received it.

The store account is also the base of the **stock statement (जिन्सी मौज्दात फाँटबारी)**, sent periodically to the higher office, and it is what shows, at the end of the year, the value of goods still in hand.

**Store verification.** A physical count of the store is made **annually** — and, for valuable or easily misused goods, more often — by a **store inspection committee** of at least two officers, one of whom is not connected with the store. The committee counts the articles, compares the count with the store ledger and the bin card, and records the differences in the verification form. Differences are then explained: an excess is brought into account; a shortage is recovered from the person responsible, or written off by the competent authority after investigation. Goods that are worn out, unserviceable or beyond repair are written off with the approval of the prescribed authority and disposed of in the prescribed manner.

::: example Store ledger entries
**Problem.** The store of a District Education Office holds steel almirahs under head 31121. During Baisakh the following took place. Baisakh 1 — 50 almirahs received from Nepal Trading at Rs. 6,000 each against a bill of Rs. 3,00,000. Baisakh 5 — 10 issued to the accounts section. Baisakh 12 — 25 received from Nepal Trading. Baisakh 20 — 15 issued to the school supervision section. Complete the store ledger and state the balance.
Show also the value of the closing stock.

**Solution.**
Step 1 — Enter each receipt in the receipt column and each issue in the issue column, and carry the balance after every entry.

| Date | Particulars | Receipt (no.) | Issue (no.) | Balance (no.) |
|---|---|---|---|---|
| Baisakh 1 | Received from Nepal Trading | 50 | | 50 |
| Baisakh 5 | Issued to the account section | | 10 | 40 |
| Baisakh 12 | Received from Nepal Trading | 25 | | 65 |
| Baisakh 20 | Issued to the school supervision section | | 15 | 50 |

Step 2 — Rate: Rs. 6,000 each (from the Baisakh 1 bill).
Step 3 — Closing stock $= 50 \times 6{,}000 = Rs.\ 3{,}00{,}000$.
Step 4 — Check against the documents: total received $= 50 + 25 = 75$; total issued $= 10 + 15 = 25$; balance $= 75 - 25 = 50$. ✔

**Answer.** Closing balance 50 almirahs, valued at Rs. 3,00,000; total received 75, total issued 25.
**What it means.** The bin card on the almirah shelf must show exactly the same three numbers — 75 in, 25 out, 50 in hand. If it does not, either a receipt or an issue went unrecorded, and that is the beginning of a shortage.
:::

::: example Is this an irregularity?
**Problem.** A storekeeper has 12 reams of paper in the store. A clerk asks for 2 reams for the account section and says he will "sign the register tomorrow". The storekeeper hands over the paper. Two months later the store ledger shows a shortage of 2 reams. Decide whether the storekeeper acted correctly, and what he should have done.

**Solution.**
Step 1 — State the rule. No article may be issued from a government store without a written requisition and a signed **जिन्सी निकासा फाराम**.
Step 2 — What actually happened. The paper left the store without any document, so nothing in the records explains where it went. The store ledger and the bin card still show 12 reams while the shelf holds 10.
Step 3 — The consequence. The shortage of 2 reams is unexplained; if the clerk denies taking the paper, the storekeeper must make it good, because he is answerable for the goods in his charge.
Step 4 — What should have been done: insist on the requisition, fill the जिन्सी निकासा फाराम, obtain the receiving officer's signature, enter the issue in the store ledger and the bin card, and only then hand over the paper.

**Answer.** The storekeeper acted irregularly. He must have a written requisition and a signed issue form before any article leaves the store.
**What it means.** Every rule in store accounting exists to answer one question: who has the goods, and where is the paper that says so?
:::

::: example Bin card against store ledger
**Problem.** At the annual verification of the store of a District Office, the bin card on the shelf of electric fans shows a balance of 14, while the store ledger shows 15. The committee counts 13 fans on the shelves. Explain what has happened and what the committee should do.

**Solution.**
Step 1 — Compare the three figures. Count 13; bin card 14; store ledger 15. So at least one issue of 1 fan and probably another have gone unrecorded, or a fan has been removed without a document.
Step 2 — Check the issue forms against the ledger for the year. If an issue form for 1 fan exists which was not entered in the bin card, the bin card is wrong and must be corrected on the spot.
Step 3 — Trace the remaining difference. A shortage of 1 fan is still unexplained. The committee asks the storekeeper for an explanation and inspects the sections that received fans, because a fan may have been taken to a room without an issue form.
Step 4 — Record the result in the जिन्सी जाँच फाराम, with the reasons; the shortage of 1 fan is reported to the head of office, who will either recover its value from the person responsible or write it off with the approval of the prescribed authority.
Step 5 — Correct the records so that the store ledger, the bin card and the physical count all read 13.

**Answer.** The bin card is corrected to 13, the missing issue form is traced, and the unexplained shortage of 1 fan is reported for recovery or write-off with approval.
**What it means.** A bin card that has not been written up is worse than no bin card at all, because it looks like a record while it is not one. Every issue is entered on both the ledger and the card, on the same day.
:::

::: caution The common mistake
The commonest mistake is to keep the store ledger and the bin card separately and never compare them, and the second is to accept goods that do not match the purchase order. A short delivery signed for as complete is a loss that will be discovered only at the annual verification — and by then the supplier has been paid in full and the money cannot be recovered.
:::

## Chapter summary

- **Store accounting (जिन्सी लेखा)** records the receipt, storage, issue and balance of goods held by a government office, in quantity and in value. Goods are either **consumable** (stationery, fuel, medicines) or **non-consumable or durable** (furniture, computers, vehicles).
- Its **objectives** are to record every receipt and issue, to show the stock balance at any time, to prevent loss and misuse, to provide audit evidence and to help budgeting.
- Its **importance** is that public goods remain public property: the store account ties every article to a document and a person, and protects the honest officer by showing exactly what was received and what was issued.
- The **formats** are the जिन्सी दाखिला फाराम (goods received), the जिन्सी निकासा फाराम (issue), the store ledger, the bin card, the stock statement (जिन्सी मौज्दात फाँटबारी), the verification form and the accounting voucher.
- The **store ledger (जिन्सी खाता)** holds one account per article with receipts, issues and the balance, usually in the **continuous balance** form.
- The **bin card** is kept on the shelf with the article and must always agree with the store ledger; a difference between them is investigated at once.
- The store account is used by the **storekeeper** (what to requisition), the **accounts section** (valuation and entries) and the **auditor** (tracing a bill to the shelf).
- **Store verification** is a physical count, usually annual, by a store inspection committee of at least two officers, one unconnected with the store. Differences are explained — an excess brought into account, a shortage recovered or written off, and unserviceable goods written off and disposed of with the prescribed approval.

## Practice questions

**Group A — Very short answer (1 mark each)**

1. What is store accounting? <span class="marks">[1]</span>
2. Write any two importance of store accounting. <span class="marks">[1]</span>
3. What is जिन्सी? <span class="marks">[1]</span>
4. Write any two examples of durable store goods. <span class="marks">[1]</span>
5. What is a bin card? <span class="marks">[1]</span>
6. What is a store ledger? <span class="marks">[1]</span>
7. What is the जिन्सी दाखिला फाराम used for? <span class="marks">[1]</span>
8. What is a stock statement? <span class="marks">[1]</span>
9. Who conducts the physical verification of a government store? <span class="marks">[1]</span>
10. May an article be issued from a store without a requisition? <span class="marks">[1]</span>
11. With which record must the bin card always agree? <span class="marks">[1]</span>

::: note Answers to Group A
**1.** Store accounting is the branch of government accounting that records the receipt, storage, issue and balance of goods held by a government office, in quantity and in value.
**2.** Any two of: to record every receipt and issue; to show the stock balance at any time; to prevent loss, misuse and theft; to provide audit evidence; to help budgeting; to prove that public goods remain public property.
**3.** जिन्सी means the goods and articles held by a government office — both consumable goods such as stationery and fuel and durable goods such as furniture and computers.
**4.** Any two of: furniture, computers, vehicles, machines, musical instruments.
**5.** A bin card is a small card kept on the shelf or bin with the article, showing receipts, issues and the balance in hand.
**6.** The store ledger is the main store book, with one account or page for each article, showing the date, particulars, receipts, issues and the balance.
**7.** For recording goods received into the store — date, description, specification, quantity, value and supplier.
**8.** The stock statement (जिन्सी मौज्दात फाँटबारी) is the periodic statement of goods in hand, by head, sent to the higher office and used for reporting and budgeting.
**9.** A store inspection committee of at least two officers, one of whom is not connected with the store.
**10.** No. A written requisition and a signed जिन्सी निकासा फाराम are required before any article leaves a government store.
**11.** With the store ledger (जिन्सी खाता).
:::

**Group B — Short answer (5 marks each)**

1. What is store accounting? Explain its objectives and importance. <span class="marks">[5]</span>
2. Explain the main formats used in store accounting. <span class="marks">[5]</span>
3. What is a store ledger? Explain its form with a suitable example. <span class="marks">[5]</span>
4. Explain the use of the store account and the procedure of store verification. <span class="marks">[5]</span>
5. The store of a government office holds steel chairs. On Kartik 1, 40 chairs were received at Rs. 2,500 each. On Kartik 8, 12 were issued to the administration section; on Kartik 18, 20 more were received; on Kartik 25, 8 were issued to the examination section. Prepare the store ledger and find the value of the closing stock. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Definition as in Group A answer 1. Objectives: to record every receipt with quantity, specification, value, supplier and voucher; to record every issue with date, quantity and receiver; to show the balance at any time; to prevent loss and misuse; to provide audit evidence; to help budgeting. Importance: public goods remain public property; the record ties each article to a document and a person; it protects the honest officer against later allegations; it supports the annual verification and the stock statement.
**2.** जिन्सी दाखिला फाराम — goods received, with specification, quantity, value, supplier and purchase voucher; जिन्सी निकासा फाराम — goods issued, with the requisition and the receiver's signature; store ledger — one account per article with receipts, issues and balance; bin card — the same record kept at the shelf; जिन्सी मौज्दात फाँटबारी — the periodic stock statement; जिन्सी जाँच फाराम — the physical verification record; and the voucher that brings the store figures into the accounts. State the rule that only the prescribed form, signed by the authorised officer, is acceptable.
**3.** The store ledger is the principal store book with one account or page per article. It carries the date, the particulars, the receipt quantity, the issue quantity and the balance, and it is usually kept in the continuous balance form so that the balance is visible after every entry. Give an example: receive 50 units, issue 10 (balance 40), receive 25 (balance 65), issue 15 (balance 50), and value the closing stock at the purchase rate.
**4.** Use: the storekeeper reads it to know what is in stock and what to requisition; the accounts section reads it to value the goods and to enter them in the accounts; the auditor reads it to trace an article from the purchase bill to the store ledger, to the bin card and to the shelf, and to see whether the article issued is still with the section that received it. Verification: an annual physical count by a store inspection committee of at least two officers, one unconnected with the store; the count is compared with the ledger and the bin card; differences are recorded in the verification form; an excess is brought into account, a shortage is recovered from the person responsible or written off by the competent authority after investigation; unserviceable goods are written off with approval and disposed of in the prescribed manner.
**5.**

| Date | Particulars | Receipt | Issue | Balance |
|---|---|---|---|---|
| Kartik 1 | Received from supplier | 40 | | 40 |
| Kartik 8 | Issued to administration section | | 12 | 28 |
| Kartik 18 | Received from supplier | 20 | | 48 |
| Kartik 25 | Issued to examination section | | 8 | 40 |

Closing stock $= 40 \times 2{,}500 = Rs.\ 1{,}00{,}000$. Total received 60, total issued 20, balance 40. ✔
:::

**Group C — Long answer (8 marks each)**

1. What is store accounting? Explain its objectives, importance and the main store formats, and describe how a government store is verified. <span class="marks">[8]</span>
2. Explain the meaning of जिन्सी, the two kinds of store goods, and the procedure by which goods are received into and issued from a government store. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** *Definition (1).* As in Group A answer 1.
*Objectives and importance (3).* Record every receipt and issue with evidence; show the balance at any time; prevent loss and misuse; provide audit evidence; help budgeting. Importance: public goods stay public property; each article is tied to a document and a person; the honest officer is protected; the annual verification and the stock statement rest on it.
*Formats (2).* जिन्सी दाखिला फाराम, जिन्सी निकासा फाराम, store ledger, bin card, stock statement, verification form and the voucher — one line each.
*Verification (2).* Annual physical count by a store inspection committee of at least two officers, one unconnected with the store; comparison with the ledger and bin card; differences recorded in the verification form; excess brought into account, shortage recovered or written off with approval; unserviceable goods written off and disposed of in the prescribed manner.
**2.** *Meaning (1).* जिन्सी means the goods and articles held by a government office, and जिन्सी लेखा is the account of their receipt, storage, issue and balance in quantity and value.
*Two kinds (2).* Consumable goods, used up in the course of work — stationery, ink, cleaning materials, medicines, fuel; and non-consumable or durable goods, which keep their identity and are used over years — furniture, computers, vehicles, machines. Consumable goods are expensed, while durable goods are capital expenditure and remain on the store record.
*Receipt (2).* Goods are bought by a payment order against a budget head; on arrival the storekeeper compares them with the purchase order and the bill, fills the जिन्सी दाखिला फाराम with the description, specification, quantity and value, enters the receipt in the store ledger and the bin card, and passes the bill for payment. Goods not matching the order are not accepted, or accepted in part with the supplier informed in writing.
*Issue (2).* A section sends a written requisition; the storekeeper fills the जिन्सी निकासा फाराम; the receiving officer signs it; the issue is entered in the store ledger and the bin card; and the form is filed as the evidence that the article left the store. No article may leave without a document.
*Control (1).* The bin card and the store ledger are compared periodically, and the store is verified annually by a committee.
:::


## Retrieval practice and investigation

::: key Work before reading the key
Answer these short retrieval questions without consulting the chapter. Explain the reason, not only the result. These are revision checks, not a prediction of the examination paper.
:::

**1.** What is the book balance?

**2.** What is the shortage if physical stock is 22?

**3.** Does a store issue form prove a new purchase?

::: note Reasoned key
**1.** 20 + 15 − 12 = 23 notebooks.

**2.** 1 notebook. Investigate before deciding its cause or writing it off.

**3.** No. It documents goods leaving the store; a receipt record documents goods received.

:::

::: tip Investigation — Reconcile a stock card
Start with 20 notebooks, receive 15 and issue 12. Prepare a stock card showing each movement and the running balance. Compare the final balance with a fictional physical count of 22 and record the discrepancy for investigation.

Submit a one-page record: your method, working or evidence, conclusion, and one limitation. Exchange it with a classmate and check the reasoning against the chapter.
:::
