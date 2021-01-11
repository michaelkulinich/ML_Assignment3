# Collaborators Brandon Kleinman

import xlrd
import numpy as np
from collections import defaultdict
import time

def read_excel(input_file):
    loc = (input_file)

    wb = xlrd.open_workbook(loc)

    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0,0)

# MAYBE MAKE TRANSACTIONS AS A SET OF TRANSACTIONS (aka set of lists)
    transactions = []
    items = []

    transaction_count = 0
    curr_transaction = sheet.cell_value(1,0)
    curr_itemset = []
    curr_itemset.append(sheet.cell_value(1,1))

    test_num_trans = [curr_transaction]
    count = 0
    for i in range(2, sheet.nrows):
        invoiceNo = sheet.cell_value(i,0)
        item = sheet.cell_value(i,1)
        # this is a return, ignore this row
        if type(invoiceNo) == str and invoiceNo[0] == 'C':
            # print(sheet.cell_value(i,0))
            continue

        # if we are still on the same transaction as previous row
        elif invoiceNo == curr_transaction:
            # this is a check, see else statement below
            # if item in curr_itemset:
            #     print(item)

            curr_itemset.append(item)

        # if we this row is new transaction, put the previous transaction into list and update curr_trans
        else:
            # append the transformed set to list because sometimes in a single transaction
            # the same item is rung up multiple times, multiple rows for single item
            # ex: In my transaction, the cashier scans 5 milks, then 1 beer, then 1 milk
            # this would happen when multiple of the same item are dispeared throughout the shopping cart
            # and the cashier doesn't group multiple of the same item together
            # in this dataset: stock codes: 71270, 90199c ...
            transactions.append(list(set(curr_itemset)))
            curr_transaction = invoiceNo
            curr_itemset = [item]
            transaction_count += 1

        count += 1
        test_num_trans.append(invoiceNo)
        items.append(item)

    # last row bound case. checks if itemset is non-empty
    if curr_itemset:
        transactions.append(list(set(curr_itemset)))
    # print("Num transactions", len(transactions))
    # print("Set len", len(set(test_num_trans)))
    # print("Num items", len(set(items)))
    # print("Num rows", sheet.nrows)
    len_itemsets = [len(itemsets) for itemsets in transactions]
    average_len = (lambda lst: sum(lst) / len(lst))(len_itemsets)
    # print("Average num unique items in transaction", average_len)
    # print("dict keys", transactions.keys())
    # print("set keys", set(test_num_trans))

    return set(items), transactions
# check if code is just D, remove those rows
# if transaction tum starts with c, remove that row, its just returns

def apriori(items, transactions, minsup, itemset_size = 3):
    # creates a dictionary of all the items as keys, and initialized to a default count of 0
    # zipe function used to group the keys and values together
    # inorder to create key value pair in the dictionary
    candidates_k1 = dict(zip(items, [0]*len(items)))

    fk_minus_1 = []
    a = time.time()
    # step: scan T and generate F_k portion
    for transaction in transactions:
        for item in transaction:
            # increment the count for each 1 itemset candidate
            candidates_k1[item] += 1

            # check if the itemset is frequent, if so add it to frequent itemsets
            # also make sure that item is not already in the set
            if candidates_k1[item]/len(transactions) >= minsup and {str(item)} not in fk_minus_1:
                fk_minus_1.append({str(item)})
    # print("first loop over transactions", time.time() - a)

    # print(fk_minus_1)
    # print(candidate_gen(fk_minus_1, 2))
    for k in range(2,itemset_size + 1):
        a = time.time()
        candidates_k = candidate_gen(fk_minus_1, k)
        # print("TIME OF CANGEn", time.time() - a)
        fk = set()
        # print("Length of fk-1", len(fk_minus_1))
        # print("Length of superset fk-1", len(candidates_k))

        for transaction in transactions:
            transaction_len = len(transactions)
            transaction_set = set(transaction)
            # candidate is a frozen set
            for candidate in candidates_k.keys():
                # diff from above for k1 because we are unsure if candidate is in the itemset
                if set(candidate) & transaction_set == set(candidate):
                    candidates_k[candidate] += 1
# THIS IS TAKING A LONG TIME
                if candidates_k[candidate]/transaction_len >= minsup:
                    fk.add(frozenset(candidate))
        fk_minus_1 = list(fk)
        # print("Frequent itemsets of size:", k, "\n", fk)
        # print("after for loop:", time.time())

    return fk_minus_1



# takes in fk-1 and returns a dictionary of candidates
def candidate_gen(fk_minus_1, k):
    # join, generate candidates by doing superset of all the fk-1's, with sets size k-1
    # make the candidates a dict with default values 0
    # this will be a set of (sets?, or lists?)
    # candidates = superset(fk_minus_1)

    candidates = []
    for i in range(len(fk_minus_1) - 1):
        for j in range(i + 1, len(fk_minus_1)):
            union = fk_minus_1[i] | fk_minus_1[j]
            # if len(union) == k and union not in candidates:
            if len(union) == k:
                candidates.append(union)
    candidates_k = {}
    for i in candidates:
        candidates_k[frozenset(i)] = 0

    return candidates_k
def main():
    out = open("output1.txt", "w")
    input_file = "RetailData3.xlsx"
    items, transactions = read_excel(input_file)

    # f1 = count_1_itemsets(items, transactions, .13)
    # print(f1)
    min_sups = [.01, .05, .1, .2, .3]
    for minsup in min_sups:

        f3 = apriori(items, transactions, minsup, itemset_size = 3)
        out.write("Minsup: ", minsup)
        out.write(f3)

    # f3 = apriori(items, transactions, .01, itemset_size = 3)
    # # f2 = apriori(test_items, test_transactions, .5, itemset_size=3)
    # print(f3)
    # out.write("Minsup: .01")
    # out.write(str(f3))
if __name__ == '__main__':
    main()
