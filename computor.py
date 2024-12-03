#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re, sys

def printReduceForm(equation):

	reducedForm, polSup, polMax = '', False, 0
	print(equation)
	polVec = sorted(list(equation.keys()))
	print(polVec)
	for k in polVec:
		if int(k) > polMax:
			polMax = int(k)

		if equation[k] != 0:
			value = int(equation[k]) if equation[k] % int(equation[k]) == 0 else equation[k]
			if equation[k] < 0:
				reducedForm += ' - ' if polSup else '-'
			elif polSup:
				reducedForm += ' + '
			if int(k) > 1:
				reducedForm += str(abs(value)) + ' * X^' + str(k) if value != 1 else 'X^' + k
				polSup = True
			elif int(k) == 1:
				reducedForm += str(abs(value)) + ' * X' if value != 1 else 'X'
				polSup = True
			else:
				reducedForm += str(abs(value))
				polSup = True

	if len(reducedForm) > 0:
		print('Reduced From : ' + reducedForm + ' = 0')
	return polMax


def printResult(result):

	if result['solution'] is None:
		print('Solution is all real numbers')

	elif result['solution'] == False:
		print('There is no solution')

	else:
		if result['discriminant'] is None and result['degree'] == 1:
			print('Polynomial degree: 1')
			print('The solution is:\n{}'.format(result['solution1']))
		elif result['discriminant'] == 0 and result['degree'] == 2:
			print('Polynomial degree: 2')
			print('Discriminant is null, the solutions is:\n{}'.format(result['solution1']))
		elif result['discriminant'] < 0 and result['degree'] == 2:
			print('Polynomial degree: 2')
			print('Discriminant is strictly negative, the two solutions are:\n{}\n{}'.format(result['solution1'], result['solution2']))
		else:
			print('Polynomial degree: 2')
			print('Discriminant is strictly positive, the two solutions are:\n{}\n{}'.format(result['solution1'], result['solution2']))


def checkEquation(equation):
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

def checkSubElement(element, sign):
	result = dict()
	elementSplit = element.split('X')

	if len(elementSplit) > 2 or len(elementSplit) == 0:
		print('error in polynome')
		exit(1)

	if len(elementSplit) == 2:
		elementSplit[0] = '1*' if elementSplit[0] == '' else elementSplit[0]
		elementSplit[1] = '^1' if elementSplit[1] == '' else elementSplit[1]
		if elementSplit[0][-1] != '*' or elementSplit[1][0] != '^':
			print('Error in equation constrution')
			exit(1)
		else:
			try:
				result['denominateur'] = float(elementSplit[0][:-1]) if sign == '+' else -1 * float(elementSplit[0][:-1])
				pol = float(elementSplit[1][1:]) if elementSplit[1][1:] != '' else 1
				if not (pol).is_integer():
					print('We do not handle float as polynome.')
					exit(1)
				result['polynome'] = int(pol)

			except:
				print('Error in equation constrution')
				exit(1)

	else:
		try:
			result['denominateur'] = float(elementSplit[0]) if sign == '+' else -1 * float(elementSplit[0])
			result['polynome'] = 0
		except:
			print('Error in equation constrution')
			exit(1)
	return result

def computer(equation):
	result = {
		'solution': True,
		'solution2': None,
		'discriminant' : None,
		'polMax': 0
	}

	if not checkEquation(equation):
		exit(1)

	equation = equation.replace(' ','')

	equationEquality = equation.split('=')
	if len(equationEquality) != 2:
		print('Error on equality')
		exit(1)

	leftSide = re.split(r'([\+\-])', equationEquality[0]) if equationEquality != '0' else ['+', '0']
	rightSide = re.split(r'([\+\-])', equationEquality[1]) if equationEquality != '0' else ['+', '0']

	for side in [leftSide, rightSide]:
		if side[0] == '':
			side.remove(side[0])
		if side[0] != '-':
			side.insert(0, '+')

	if '' in leftSide or '' in rightSide:
		print('Negative number in equation')
		exit(1)

	sign = '+'
	leftSideClean = list()
	rightSideClean = list()
	for side, newSide in zip([leftSide, rightSide], [leftSideClean, rightSideClean]):
		for e in side:
			if e in ['-', '+']:
				sign = e
			else:
				temp = checkSubElement(e, sign)
				newSide.append(temp)

	firstStepEquation = leftSideClean
	for element in rightSideClean:
		element['denominateur'] *= -1
		firstStepEquation.append(element)

	equationDict = dict()
	for element in firstStepEquation:
		if 'denominateur' in element and 'polynome' in element:
			if str(element['polynome']) not in equationDict:
				equationDict[str(element['polynome'])] = element['denominateur']
			else:
				equationDict[str(element['polynome'])] += element['denominateur']

	result['polMax'] = printReduceForm(equationDict)
	if result['polMax'] > 2:
		print('Polynomial Degree : {}\nThe polynomial degree is stricly greater than 2, I can\'t solve.'.format(result['polMax']))
		result['solution'] = False
		return result

	# Check if all polynome are in the equation
	if len(equationDict) < result['polMax'] + 1:
		for i in range(0, result['polMax'] + 1):
			if str(i) not in equationDict:
				equationDict[str(i)] = 0


	if '2' in equationDict and equationDict['2'] != 0:
		result['degree'] = 2
		discriminant = equationDict['1'] ** 2 - 4 * equationDict['0'] * equationDict['2']
		result['discriminant'] = discriminant
		if discriminant > 0:
			result['solution1'] = (-1 * equationDict['1'] - discriminant**(1 / 2)) / (2 * equationDict['2'])
			result['solution2'] = (-1 * equationDict['1'] + discriminant**(1 / 2)) / (2 * equationDict['2'])
		elif discriminant == 0:
			result['solution1'] = (-1 * equationDict['1']) / (2 * equationDict['2'])
		else:
			result['solution1'] = str((-1 * equationDict['1']) / (2 * equationDict['2'])) + ' + i * ' + \
								  str(abs(discriminant**(1 / 2)) / (2 * equationDict['2']))
			result['solution2'] = str((-1 * equationDict['1']) / (2 * equationDict['2'])) + ' - i * ' + \
								  str(abs(discriminant**(1 / 2)) / (2 * equationDict['2']))

	elif '1' in equationDict and equationDict['1'] != 0:
		result['degree'] = 1
		result['solution1'] = -1 * equationDict['0'] / equationDict['1']

	elif '0' in equationDict and equationDict['0'] != 0:
		result['solution'] = False

	else:
		result['solution'] = None

	printResult(result)
	return result

if __name__ == '__main__':

	# if len(sys.argv) < 2:
	# 	print('Missing Equation')
	# 	exit(1)

	# elif len(sys.argv) > 2:
	# 	print("Equation not well formatted. Should be in one string.")
	# 	exit(1)

	# else:
	_ = computer("-5.2 + 4 * X - X^2= X^2")