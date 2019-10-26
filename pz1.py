arr = [[1, 50, 3], [3, 20, 2], [7, 5, 6]]
result_a = 1
result_b = 0
print('Введите строку:')
row = int(input())
print('Введите число:')
cond = int(input())

for i in arr:
    num_a = i[1]

    result_a *= num_a

for i in arr[row]:
    result_b += i

if result_a / 100 >= 1 and result_a / 100 < 10:
    print('Число трехзначное:' + str(result_a))
else:
    print('Число нетрехзначное:' + str(result_a))

if result_b > cond:
    print('Число больше, чем ' + str(cond))
else:
    print('Число меньше, чем ' + str(cond))
