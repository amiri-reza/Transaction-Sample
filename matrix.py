matrix = [[1,1,1],[1,0,1],[1,1,1]]

row_num = None
idx = None
for no,row in enumerate(matrix):
    # print(no, row)
    if 0 in row:
        idx = row.index(0)
        row_num = no
        # print(row_num, "_________", idx)


for no, row in enumerate(matrix):
    row[idx] = 0
    if no == row_num:
        print(no, "-------", row)
        for num in row:
            print(num, "________")
            num = 0
            print(num, "________aaa")
        print(row, "@@@@@@@@@@")

print(matrix)