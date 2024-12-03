import sys
import re

def solveEquation(equation):
    

def reducedForm(equation):

    sortedEquation = list(sorted(equation.keys()))
    polMax = sortedEquation[-1]
    firstElem = False
    reduceform = ''
    for i in sortedEquation:
        if equation[i] != 0:
            value = int(equation[i]) if equation[i] % equation[i] == 0 else equation[i]
            if equation[i] < 0:
                reduceform += ' - ' if firstElem else '-'
            elif equation[i] > 0 and firstElem:
                reduceform += ' + '
            if i > 1:
                reduceform += str(abs(value)) + ' * X^' + str(i) if value != 1 else 'X^' + str(i)
            
            elif i == 1:
                reduceform += str(abs(value)) + ' * X' if value != 1 else 'X'
            else:
                reduceform += str(abs(value))
        firstElem = True
    if len(reduceform) > 0:
        print('Reduced From : ' + reduceform + ' = 0')
    return polMax
    
def reviewEquation(equation):
    reg = re.compile(r'[0-9X\s\^\-\+\*\=\.\/]+$')
    const = re.search(r'(?<=[^X])\^', equation)
    const2 = re.search(r'\^(?![0-9])', equation)
    const3 = re.search(r'(?<=\d)\s(?=\d)', equation)
    if not reg.match(equation):
        print('Wrong caracters in equation.')
        return False
    if const is not None or const2 is not None or const3 is not None:
        print('Polynome not well formatted.')
        return False
    return True

def clearElement(j, sign):
    result = dict()
    splitelements = j.split('X')
    if len(splitelements) > 2 or len(splitelements) == 0:
        print('error in polynome')
        exit(1)
    
    if len(splitelements) == 2:
        splitelements[0] = '1*' if splitelements[0] == '' else splitelements[0]
        splitelements[1] = '^1' if splitelements[1] == '' else splitelements[1]
        if splitelements[0][-1] != '*' or splitelements[1][0] != '^':
            print('Error in equation constrution')
            exit(1)
        else:
            try:
                result['denominateur'] = float(splitelements[0][:-1]) if sign == '+' else -1 * float(splitelements[0][:-1])
                pol = float(splitelements[1][1:])
                if not (pol).is_integer():
                    print('i dont handle float as polynome.')
                    exit(1)
                result['polynome'] = int(pol)
            except:
                print('Error in equation constrution')
                exit(1)
    else:
        try:
            result['denominateur'] = float(splitelements[0]) if sign == '+' else -1 * float(splitelements[0])
            result['polynome'] = 0
        except:
            print('Error in equation constrution')
            exit(1)
    return result

def HeadFunction(equation):
    result = {
        'exponent': 0,
        'solution': None,
        'solution2': None,
        'discriminant': None,
    }
    if not reviewEquation(equation):
        return result
    
    equation = equation.replace(' ', '')
    equationsplited = equation.split('=')
    if len(equationsplited) != 2:
        print('Polynome not well formatted.')
        return result
    left = re.split(r'([\+\-])', equationsplited[0])
    right = re.split(r'([\+\-])', equationsplited[1])
    for i in [left, right]:
        if i[0] == '':
            i.pop(0)
        if i[0] != '-':
            i.insert(0, '+')

    if "" in left or "" in right:
        print('Polynome not well formatted.')
        return result
    sign = '+'
    pureleftSide = list()
    purerightSide = list()
    for side , newEquation in zip([left, right], [pureleftSide, purerightSide]):
        for e in side:
            if e in ['+', '-']:
                sign = e
            else:
                returnval = clearElement(e, sign)
                newEquation.append(returnval)
    #make it one line
    for i in purerightSide:
        i['denominateur'] = -1 * i['denominateur']
        pureleftSide.append(i)
    # print(pureleftSide)
    equaDict = dict()
    for i in pureleftSide:
        # print(i)
        if i['polynome'] in equaDict:
            equaDict[i['polynome']] += i['denominateur']
        else:
            equaDict[i['polynome']] = i['denominateur']
        
    print(equaDict)
    polMax = reducedForm(equaDict)
    if(polMax > 2):
        print('The polynomial degree is stricly greater than 2, I can\'t solve.')
        return result
    result = solveEquation(equaDict)


if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     print("Usage: python3 mycomputor.py <equation>")
    #     exit(1)
    
    # equation = sys.argv[1]
    result = HeadFunction("-5 + 4 * X - X^2= X^2")
    exit(0)