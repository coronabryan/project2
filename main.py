LR_TABLE = [{'id': 's5', '(': 's4', 'E': 1, 'T': 2, 'F': 3}, # 0
            {'+': 's6', '$': 'acc'}, # 1
            {'+': 'r2', '*': 's7', ')': 'r2', '$': 'r2'}, # 2
            {'+': 'r4', '*': 'r4', ')': 'r4', '$': 'r4'}, # 3
            {'id': 's5', '(': 's4', 'E': 8, 'T': 2, 'F': 3}, # 4
            {'+': 'r6', '*': 'r6', ')': 'r6', '$': 'r6'}, # 5
            {'id': 's5', '(': 's4', 'T': 9, 'F': 3}, # 6
            {'id': 's5', '(': 's4', 'F': 10}, # 7
            {'+': 's6', ')': 's11'}, # 8
            {'+': 'r1', '*': 's7', ')': 'r1', '$': 'r1'}, # 9
            {'+': 'r3', '*': 'r3', ')': 'r3', '$': 'r3'}, # 10
            {'+': 'r5', '*': 'r5', ')': 'r5', '$': 'r5'}
            ]


def syntactic_analysis():
    step_out = []
    stack_out = []
    input_out = []
    action_out = []
    stack = [0]
    input = '(id+id)*id$'
    if input[-1] != '$':
        input += '$'
    i = 0
    res = calculate_action(stack, i, input, step_out, stack_out, input_out, action_out)
    print('Steps: ', step_out)
    print('Stack: ', stack_out)
    print('Input: ', input_out)
    print('Action: ', action_out)
    return res


def calculate_action(stack, i, input, step_out, stack_out, input_out, action_out):
    while i < len(input):
        print(stack)
        stack_out.append(stack.copy())
        print(input[i])
        input_out.append(input[i:])
        print(i)
        if isinstance(stack[-1], int):
            top = stack[-1]
            current = 'id' if input[i] == 'i' or input[i].isalpha() else input[i]
            if current in LR_TABLE[top]:
                step_out.append(LR_TABLE[top][current])
                if LR_TABLE[top][current][0] == 's':
                    do_shift(stack, top, current, action_out)
                    i += 2 if input[i] == 'i' else 1
                elif LR_TABLE[top][current][0] == 'r':
                    result = do_reduce(stack, action_out)
                    if not result:
                        return False
                elif LR_TABLE[top][current] == 'acc':
                    print('Input accepted')
                    return True
                else:
                    print('ERROR: Input not accepted. Path not available in table')
                    return False
            else:
                print('ERROR: Input not accepted. Not enough information on Table')
                return False
        else:
            break


def do_shift(stack, top, current, action_out):
    pushed = None
    if current == 'i' or current.isalpha():
        pushed = 'id'
        stack.append('id')
    else:
        pushed = current
        stack.append(current)
    stack.append(int(LR_TABLE[top][current][1:]))
    action_out.append('Push(' + pushed + ')' + ' Pushed(' + LR_TABLE[top][current][1:] + ')')


def do_reduce(stack, action_out):
    first = stack.pop()
    second = stack.pop()
    third = stack[-1]
    print(first, second, third)
    if second == 'T' and 'E' in LR_TABLE[third]:
        stack.append('E')
        stack.append(LR_TABLE[third]['E'])
        action_out.append('E -> T; Table[' + str(third) + ', E] = ' + str(LR_TABLE[third]['E']))
    elif second == 'F' and 'T' in LR_TABLE[third]:
        stack.append('T')
        stack.append(LR_TABLE[third]['T'])
        action_out.append('T -> F; Table[' + str(third) + ', T] = ' + str(LR_TABLE[third]['T']))
    elif second == 'T' or second == 'F' or second == ')':
        temp = []
        find_similar_grammar(stack, temp, second, action_out)
        if not stack:
            print('ERROR: Input not accepted. No Grammar works for this input.')
            return False
    elif second == 'id' or second.isalpha():
        stack.append('F')
        stack.append(LR_TABLE[third]['F'])
        action_out.append('F -> id; Table[' + str(third) + ', F] = ' + str(LR_TABLE[third]['F']))
    return True


def find_similar_grammar(stack, temp, second, action_out):
    while stack:
        temp.append(stack.pop())
        index = stack[-1]
        if second == 'T' and temp[-1] == 'E' and '+' in temp:
            stack.append('E')
            stack.append(LR_TABLE[index]['E'])
            action_out.append('E -> E + T; Table[' + str(index) + ', E] = ' + str(LR_TABLE[index]['E']))
            break
        if second == 'F' and temp[-1] == 'T' and '*' in temp:
            stack.append('T')
            stack.append(LR_TABLE[index]['T'])
            action_out.append('T -> T * F; Table[' + str(index) + ', T] = ' + str(LR_TABLE[index]['T']))
            break
        if second == ')' and temp[-1] == '(' and 'E' in temp:
            stack.append('F')
            stack.append(LR_TABLE[index]['F'])
            action_out.append('F -> (E); Table[' + str(index) + ', F] = ' + str(LR_TABLE[index]['F']))
            break


if __name__ == '__main__':
    syntactic_analysis()