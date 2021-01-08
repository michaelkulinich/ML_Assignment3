import xlrd
import numpy as np

def read_excel(input_file):
    loc = (input_file)

    wb = xlrd.open_workbook(loc)

    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0,0)

    # print(sheet.nrows)
    transactions = {}
    transaction_count = 0
    curr_transaction = sheet.cell_value(1,0)
    curr_itemset = []
    curr_itemset.append(sheet.cell_value(1,1))

    test_num_trans = [curr_transaction]

    for i in range(2, sheet.nrows):
        invoiceNo = sheet.cell_value(i,0)
        # this is a return, ignore this row
        if type(invoiceNo) == str and invoiceNo[0] == 'C':
            # print(sheet.cell_value(i,0))
            pass

        # if we reach a new transaction, put the previous transaction into dict and update curr_trans
        elif invoiceNo != curr_transaction:
            test_num_trans.append(invoiceNo)

            transactions[transaction_count] = curr_itemset
            curr_transaction = invoiceNo
            curr_itemset = [sheet.cell_value(i,1)]
            transaction_count += 1
        else:
            test_num_trans.append(invoiceNo)
            curr_itemset.append(sheet.cell_value(i,1))

    # last row bound case. checks if itemset is non-empty
    if curr_itemset:
        transactions[curr_transaction] = curr_itemset
    print("Dictionary len", len(transactions))
    print("Set len", len(set(test_num_trans)))

    len_itemsets = [len(itemsets) for itemsets in transactions.values()]
    average_len = (lambda lst: sum(lst) / len(lst))(len_itemsets)
    print(average_len)
    # print("dict keys", transactions.keys())
    # print("set keys", set(test_num_trans))

# check if code is just D, remove those rows
# if transaction tum starts with c, remove that row, its just returns

def main():
    input_file = "test.xlsx"
    read_excel(input_file)


if __name__ == '__main__':
    main()
