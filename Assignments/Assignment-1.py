#5D Array Comparison & finding Common Values
# Given two 5D arrays, write a program to compare them and find common values.

Arr1 = [[[[[17, 32], [19, 13], [56, 89], [72, 20]]]]]
Arr2 = [[[[[32, 9], [17, 12], [72, 56], [20, 14]]]]]

common_values = []

for i in range(len(Arr1)):
    for j in range(len(Arr1[i])):
        for k in range(len(Arr1[i][j])):
            for l in range(len(Arr1[i][j][k])):
                for m in range(len(Arr1[i][j][k][l])):
                    val1 = Arr1[i][j][k][l][m]
                    for i2 in range(len(Arr2)):
                        for j2 in range(len(Arr2[i2])):
                            for k2 in range(len(Arr2[i2][j2])):
                                for l2 in range(len(Arr2[i2][j2][k2])):
                                    for m2 in range(len(Arr2[i2][j2][k2][l2])):
                                        val2 = Arr2[i2][j2][k2][l2][m2]
                                        if val1 == val2 and val1 not in common_values:
                                            common_values.append(val1)

print("Common values:", common_values)