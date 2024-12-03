if __name__ == '__main__':
	lista = ['1', '2', '3', '4', '5']
	listb = ['10', '20', '30', '40', '50']
	for side, newside in zip(lista, listb):
		print(side, newside)