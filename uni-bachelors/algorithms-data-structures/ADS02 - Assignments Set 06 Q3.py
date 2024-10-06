def optimalStrategyOfGame(arr, n):
    
    table = [[[0] for i in range(n)] for i in range(n)]

    for gap in range(n):
        for j in range(gap, n):
            i = j - gap

            x = 0
            xchoices = []
            if((i + 2) <= j):
                x = table[i + 2][j][0]
                xchoices = table[i + 2][j][1:]

            y = 0
            ychoices = []
            if((i + 1) <= (j - 1)):
                y = table[i + 1][j - 1][0]
                ychoices = table[i + 1][j - 1][1:]

            z = 0
            zchoices = []
            if(i <= (j - 2)):
                z = table[i][j - 2][0]
                zchoices = table[i][j - 2][1:]

            left = arr[i] + min(x, y)
            right = arr[j] + min(y, z)

            if left >= right:
                table[i][j] = [left, arr[i]]
                if x <= y:
                    table[i][j] += xchoices
                else:
                    table[i][j] += ychoices
            else:
                table[i][j] = [right, arr[j]]
                if y <= z:
                    table[i][j] += ychoices
                else:
                    table[i][j] += zchoices
                    
    return table[0][n - 1]

arr1 = [ 8, 15, 3, 7 ]
n = len(arr1)
print(optimalStrategyOfGame(arr1, n))

arr2 = [ 2, 2, 2, 2 ]
n = len(arr2)
print(optimalStrategyOfGame(arr2, n))

arr3 = [ 20, 30, 2, 2, 2, 10]
n = len(arr3)
print(optimalStrategyOfGame(arr3, n))

