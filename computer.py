import sys
import re
from math import sqrt
from fractions import Fraction

def convert_float_to_coprime_fraction(x):
    return Fraction(x).limit_denominator()

def printResults(result):
    if result['solution'] == None:
        print('Solution is all real numbers')
    else:
        if result['discriminant'] is None and result['exponent'] == 1:
            if result['solution'] % 1 != 0:
                result['solution'] = result['solution']
            else:
                result['solution'] = int(result['solution'])
            print('Polynomial degree: 1')
            print('The solution is:\n{}'.format(result['solution']))
        elif result['discriminant'] == 0 and result['exponent'] == 2:
            print('Polynomial degree: 2')
            print('Discriminant is null, the solutions is:\n{}'.format(result['solution']))
        elif result['discriminant'] < 0 and result['exponent'] == 2:
            print('Polynomial degree: 2')
            print('Discriminant is strictly negative, the two solutions are:\n{}\n{}'.format(result['solution'], result['solution2']))
        else:
            if result['solution'] % 1 != 0:
                result['solution'] = convert_float_to_coprime_fraction(result['solution'])
            else:
                result['solution'] = int(result['solution'])
            if result['solution2'] % 1 != 0:
                result['solution2'] = convert_float_to_coprime_fraction(result['solution2'])
            else:
                result['solution2'] = int(result['solution2'])
            print('Polynomial degree: 2')
            print('Discriminant is strictly positive, the two solutions are:\n{}\n{}'.format(result['solution'], result['solution2']))

def solveEquation(equation, result):
    b = equation[1] if equation.get(1) is not None else 0
    a = equation[2] if equation.get(2) is not None else 0
    c = equation[0] if equation.get(0) is not None else 0
    if result['exponent'] == 2 and equation[2] != 0:
        result['discriminant'] = b ** 2 - (4 * a * c)
        print(f"the Discriminant is: {result['discriminant']}")
        if result['discriminant'] == 0:
            result['solution'] = -1 * b / (2 * a)
        elif result['discriminant'] > 0:
            result['solution'] = (-1 * b - sqrt(result['discriminant'])) / (2 * a)
            result['solution2'] = (-1 * b + sqrt(result['discriminant'])) / (2 * a)
        else:
            print(f"The discriminant is negative, so the quadratic equation has two complex solutions")
            result['solution'] = str(-1 * b / (2 * a)) + ' - i * ' + str(sqrt(-1 * result['discriminant']) / (2 * a))
            result['solution2'] = str(-1 * b / (2 * a)) + ' + i * ' + str(sqrt(-1 * result['discriminant']) / (2 * a))
    elif result['exponent'] == 1 and  b != 0:
        res = -1 * c / b
        if res % 1 != 0:
            res = convert_float_to_coprime_fraction(res)
        result["solution"] = res
    elif result['exponent'] == 0 and b != 0:
        result['solution'] = False
    else:
         print("there is no solution")
         exit(1)
    return result
def reducedForm(equation):
	sortedEquation = list(sorted(equation.keys()))
	polMax = sortedEquation[-1]
	firstElem = False
	reduceform = ''
	for i in sortedEquation:
		if equation[i] != 0:
			value = int(equation[i]) if equation[i] % int(equation[i]) == 0 else equation[i]
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
			polMax = i
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
        exit(1)
    if const is not None or const2 is not None or const3 is not None:
        print('Polynome not well formatted.')
        exit(1)
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
                value = float(splitelements[0][:-1]) if sign == '+' else -1 * float(splitelements[0][:-1])
                result['denominateur'] = value  if value != 0 and  value % int(value) != 0 else int(value) 
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
            value = float(splitelements[0]) if sign == '+' else -1 * float(splitelements[0])
            result['denominateur'] = value  if value != 0 and value % int(value) != 0 else int(value) 
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
    if len(equationsplited) != 2 or equationsplited[0] == '' or equationsplited[1] == '' :
        print('Polynome not well formatted.')
        exit(1)
    left = re.split(r'([\+\-])', equationsplited[0])
    right = re.split(r'([\+\-])', equationsplited[1])
    for i in [left, right]:
       	if i[0] == '':
            i.pop(0)
        if i[0] != '-':
           i.insert(0, '+')

    if "" in left or "" in right:
        print('Polynome not well formatted.')
        exit(1)
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
    equaDict = dict()
    for i in pureleftSide:
        if i['polynome'] in equaDict:
            equaDict[i['polynome']] += i['denominateur']
        else:
            equaDict[i['polynome']] = i['denominateur']        
    result["exponent"] = reducedForm(equaDict)
    if(result['exponent'] > 2):
        print('The polynomial degree is stricly greater than 2, I can\'t solve.')
        return result
    result = solveEquation(equaDict, result)
    return result

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print('Missing Equation')
		exit(1)

	elif len(sys.argv) > 2:
		print("Equation not well formatted. Should be in one string.")
		exit(1)

	else:
		result = HeadFunction(sys.argv[1])
		printResults(result)

# "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"
# "5 * X^0 + 4 * X^1 = 4 * X^0"
# "1 * X^0 + 4 * X^1 = 0"
# "1 * X^0 + 4 * X^1 - 4 * X^2 = 0"