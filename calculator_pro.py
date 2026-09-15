def token(s):
    """
    将数字、运算符分装进tokens
    :param s: 输入的运算式
    :return: tokens
    """
    tokens = []
    num = ""
    for ch in s:
        if ch in "0123456789.":
            num+=ch
        else:
            if num:
                tokens.append(float(num))
                num = ""
            if ch.strip() != "":
                tokens.append(ch)
    if num:
        tokens.append(float(num))
    return tokens

def priority(op):
    """
    运算符优先级判断
    :param op: 运算符
    :return: 优先级
    """
    if op in "()":
        return 0
    if op in "+-":
        return 1
    if op in "*/":
        return 2
    #防止无意义字符
    return -1

def infix_to_postfix(tokens):
    """
    中缀转后缀，符合计算机读取
    :param tokens: 分装好的运算式
    :return: 有效的分装
    """
    postfix = []
    op_stack = []
    for t in tokens:
        if isinstance(t,float):
            postfix.append(t)
        #遇到左括号直接传入
        elif t == "(":
            op_stack.append(t)
        #遇到右括号，将两个括号内的所有运算符全部弹出
        elif t == ")":
            while op_stack and op_stack[-1] != "(":
                postfix.append(op_stack.pop())
            if not op_stack:
                raise ValueError("表达式错误：右括号前无左括号")
            op_stack.pop()
        else :
            #按优先级弹出，且一定要保证op_stack存在，不然会索引越界！！！
            while op_stack and priority(op_stack[-1]) >= priority(t):
                postfix.append(op_stack.pop())
            op_stack.append(t)
        #确保运算符都弹出，避免优先级一直往高走无法弹出的情况
    while op_stack:
        postfix.append(op_stack.pop())
    return  postfix

def calculate(postfix):
    """
    计算
    :param postfix: 有效封装了的运算逻辑
    :return: 结果
    """
    #储存数字，确保每次独立运算只有两个数字
    stack = []
    for t in postfix:
        if isinstance(t,float):
            stack.append(t)
        else:
            #一个运算符只能对两个数进行操作
            b = stack.pop()
            a = stack.pop()
            #识别运算符，运算并将结果传入
            if t == "+":
                stack.append(a+b)
            elif t == "-":
                stack.append(a-b)
            elif t == "*":
                stack.append(a*b)
            elif t == "/":
                if b==0:
                    raise ZeroDivisionError
                stack.append(a/b)
    return stack[0]

def calculator():
    """
    计算器（外壳）
    :return: 结果
    """
    while True:
        print("======欢迎使用计算器======")
        s = input("请输入运算式（输quit退出程序）").strip()
        if s.lower() == "quit":
            break
        try:
            tokens = token(s)
            postfix = infix_to_postfix(tokens)
            res = calculate(postfix)
            print(f"结果:{res:.2f}")
        except Exception as e:
            print(e)

if __name__ == "__main__":
    calculator()