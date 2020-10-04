a=11
b=a<<3                  # 将 a 左移三位
print("下面是十进制")
print(a)
print(b)                # b=a*(2**3)
print("下面是二进制")
print(bin(a))          # 转化为二进制显示
print(bin(a)[2:])       # 切片，去掉前面的：0b
print(bin(b)[2:])       # 二进制右边补上三个000

a=3
b=2
print("二进制："+bin(a)[2:]+" a十进制：%d"%a)       # 显示二进制数
print("二进制："+bin(b)[2:]+" b十进制：%d"%b)
print("按位与："+bin(a&b)+"  位与后是：%d"%(a&b))  # 都是1才是1
print("按位或："+bin(a|b)+"  位或后是：%d"%(a|b))  # 有1就是1
print("按位取反"+bin(~a)+"  位反后是：%d"%~a)   # 结果是：a 的倒数-1

