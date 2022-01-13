import numpy as np
import enquiries

alternatives_final_accuracy = 1

def input_count(s):
	if s == "criterions":
		s = "критеріїв"
	elif s == "alternatives":
		s = "альтернатив"

	count = int(input("Введіть кількість "+s+" (2 < ?): "))

	return count

def get_names(count, s):
	if s == "criterions":
		s = "-го критерію: "
	elif s == "alternatives":
		s = "-ї альтернативи: "

	names = []

	for i in range(count):
		name = input("Введіть назву для "+str(i+1)+s)
		names.append(name)

	return names 	

def get_matrix(count, names, criterion_name=""):
	matrix = np.zeros((count, count), float)
	np.fill_diagonal(matrix, 1)

	if criterion_name != "":
		criterion_name = "за критерієм "+"'"+criterion_name+"'"

	for i in range(1, count):
		for j in range(i, count):
			options = [names[i-1], names[j]]
			choice = enquiries.choose("Що важливіше "+criterion_name+" ?", options)

			if choice == names[i-1]:
				estimation = float(input("Оцініть перевагу "+"'"+names[i-1]+"'"+" над "+"'"+names[j]+"'"+" (1-9): "))
				matrix[i-1][j] = estimation
				matrix[j][i-1] = 1/estimation
			else:
				estimation = float(input("Оцініть перевагу "+"'"+names[j]+"'"+" над "+"'"+names[i-1]+"'"+" (1-9): "))
				matrix[i-1][j] = 1/estimation
				matrix[j][i-1] = estimation

	return matrix

def get_weights(count, matrix):
	roots_of_rows = []
	weights = []

	for i in range(count):
		mul_of_row = 1

		for j in range(count):
			mul_of_row *= matrix[i][j]
		
		roots_of_rows.append(pow(mul_of_row, 1/count))

	sum_of_roots = sum(roots_of_rows)

	for i in range(count):
		weights.append(roots_of_rows[i]/sum_of_roots)

	return weights

def get_accuracy(count, matrix, weights):
	lambda_max = 0

	for j in range(count):
		sum_of_column = 0

		for i in range(count):
			sum_of_column += matrix[i][j]

		lambda_max += sum_of_column*weights[j]

	ratio_index = (lambda_max-count)/(count-1)
	random_index = [0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49]
	ratio_estimation = abs(ratio_index/random_index[count-1])
	accuracy = abs(1-ratio_estimation)

	return accuracy

def print_weights(count, names, weights, accuracy, s, criterion=""):
	if s == "criterions":
		s = "критеріїв"
	elif s == "alternative":
		s = "альтернатив за критерієм "+"'"+criterion+"'" 
	elif s == "alternatives_final":
		s = "альтернатив за всіма критеріями"

	print("------------------------------")
	print("\033[1mКоефіцієнти для "+s+":"+"\033[0m")
	print()

	accuracy_int = round(accuracy*100)
	if accuracy_int >= 90:
		accuracy_str = "\033[32m\033[40m "+str(accuracy_int)
	elif accuracy_int >= 80 and accuracy_int < 90:
		accuracy_str = "\033[33m\033[40m "+str(accuracy_int)
	else:
		accuracy_str = "\033[31m "+str(accuracy_int)

	for i in range(count):
		print("\033[3m"+" - "+str(names[i])+": "+str(round(weights[i], 3))+"\033[0m")
	print()
	print("\033[1mТочність:\033[0m"+accuracy_str+"%"+"\033[0m")
	print("------------------------------")

def get_matrix_of_weights_for_alternatives(alternatives_count, alternatives_names, criterions_count, criterions_names):
	matrix_of_weights = []
	global alternatives_final_accuracy

	for i in range(criterions_count):
		alternatives_matrix = get_matrix(alternatives_count, alternatives_names, criterions_names[i])
		alternatives_weights = get_weights(alternatives_count, alternatives_matrix)
		alternatives_accuracy = get_accuracy(alternatives_count, alternatives_matrix, alternatives_weights)
		alternatives_final_accuracy *= alternatives_accuracy

		print_weights(alternatives_count, alternatives_names, alternatives_weights, alternatives_accuracy, "alternative", criterions_names[i])

		matrix_of_weights.append(alternatives_weights)

	return matrix_of_weights

def get_final_weights_of_alternatives(alternatives_matrix_of_weights, criterions_weights):
	return list(np.dot(np.array(alternatives_matrix_of_weights).transpose(), criterions_weights))

criterions_count = input_count("criterions")
criterions_names = get_names(criterions_count, "criterions")
criterions_matrix = get_matrix(criterions_count, criterions_names)
criterions_weights = get_weights(criterions_count, criterions_matrix)
criterions_accuracy = get_accuracy(criterions_count, criterions_matrix, criterions_weights)

print_weights(criterions_count, criterions_names, criterions_weights, criterions_accuracy, "criterions")

alternatives_count = input_count("alternatives")
alternatives_names = get_names(alternatives_count, "alternatives")
alternatives_matrix_of_weights = get_matrix_of_weights_for_alternatives(alternatives_count, alternatives_names, criterions_count, criterions_names)
alternatives_final_weights = get_final_weights_of_alternatives(alternatives_matrix_of_weights, criterions_weights)
final_accuracy = criterions_accuracy*alternatives_final_accuracy

print_weights(alternatives_count, alternatives_names, alternatives_final_weights, final_accuracy, "alternatives_final")