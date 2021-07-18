import json
import os
import sys

config = {}

def main():
	'''
	controls flow of program from selecting/creating config to active feedback
	'''
	
	# command line args
	argc = len(sys.argv)
	if argc>1:

		# call createConfig
		if sys.argv[1] == "-createConfig":
			createConfig()
			input("Press Enter to Exit\n")
			exit()

		# call selectConfig
		if sys.argv[1] == '-selectConfig':
			if selectConfig() == 1:
				print("Config Selection Cancelled, using last used config")
			input("Press Enter to Continue\n")
	
	# Getting absolute file path using relative path of script file
	script_dir = os.path.dirname(__file__)
	rel_path = "configs/config.json"
	abs_file_path = os.path.join(script_dir, rel_path)

	# Loading main config file
	with open(abs_file_path, 'r') as config_file:
		config = json.load(config_file)
	
	
	# call function to execute command on the column/row




def createConfig():
	'''
	creates config file taking input from user and stores it in configs/user_defined/ using the filename specified by the user
	asks user for the following
	- Config File name
	- DataBase Name (file name of csv) 
	- filepath to listen for when dump files come (optional)
	- database type (implementing csv currently)
	- number of columns
	- Column Info for each column (Name of Column and filters to apply (comma separated function names))
	'''
	
	print("\n\n\t\t\t\t\t----------CONFIG CREATOR----------\n")
	
	config_name = input("Enter name of this config\n")
	config["config_name"] = config_name

	config['db_name'] = input("Enter name of the Database\n")

	filename = input("Enter filepath for folder to listen to (enter \"default\" for default filepath = pwd -> dumps/)\n")
	if(filename == 'default'):
		script_dir = os.path.dirname(__file__)
		rel_path = "dump/" + config_name
		abs_file_path = os.path.join(script_dir, rel_path)
		config['infile_directory'] = abs_file_path
	else:
		config['infile_directory'] = filename

	config["filetype"] = "csv"
	filetype_num = input("What type of database is it intended to go to?\n" \
						"1) csv/xls file (current behavior)\n" \
						"2) MySQL\n" \
						"3) Apache\n" \
						"(enter a number)\n")
	if(filetype_num == 2):
		filetype = "MySQL"
	elif(filetype_num == 3):
		filetype = "Apache"

	num_columns = int(input("Enter Number of Columns in this File\n"))
	config['num_columns'] = num_columns

	config['columns'] = [] 
	for i in range(1,num_columns+1):
		
		col_name = input(f"Enter a name for Column {i}\n")

		filter_list = ["checkNull", "checkAllCaps", "checkAllLower", "checkProperCase", "checkEmail", "checkDateTime", "checkNChars"]
		num_filters = len(filter_list)
		print("List of all Available Filters:")
		for i in range(num_filters):
			print(f"{i+1}) {filter_list[i]}")
		print("0) Continue from this Menu")

		filter_choices = input("Enter all filters too apply separated by commas (e.g. \"checkNull,checkEmail,checkNChars\")\n")
		# filter_index -= 1
		# filter_choices_list = [filter_list[filter_index]]
		# filter_choices.append(filter_list[filter_index])

		config['columns'].append({
			'name': col_name,
			'filters': filter_choices
			})

	script_dir = os.path.dirname(__file__)
	rel_path = "configs/user_defined/" + config_name + ".json" 
	abs_file_path = os.path.join(script_dir, rel_path)
	with open(abs_file_path, 'w') as config_file:
		config_file.write(json.dumps(config, indent = 4))

def selectConfig():
	'''
	displays all files in the configs/user_defined/ folder and allows the user to select of the config to use
	The contents of the selected config file are put in configs/config.json (which is the config file loaded when running the program)
	'''
	relative_path = "\\configs\\user_defined"
	filepath = os.getcwd() + relative_path
	#filepath = os.getcwd()
	files = os.listdir(filepath)     #getting all files in the required folder
	print("---Avaliable Configs--- %s" %files)

	num_files = len(files)
	for i in range(num_files):
	    print(f"{i+1}) {files[i]}")

	infile_choice = int(input("enter index of the config file to select\n"))
	infile_choice -= 1

	with open(filepath + "\\" + files[infile_choice], 'r') as infile:
	    config = json.load(infile)

	default_config_path = os.getcwd() + "\\configs\\config.json"
	with open(default_config_path, 'w') as outfile:
	    outfile.write(json.dumps(config, indent = 4))



def filterSelect(func_name, column_name):
	'''
	Calls the function who's name is passed in the parameter as a string
	'''
	if(func_name == "checkNull"):
		checkNull(column_name)
	elif (func_name == "checkAllCaps"):
		checkAllCaps(column_name)
	elif (func_name == "checkAllLower"):
		checkAllLower(column_name)
	elif (func_name == "checkProperCase"):
		checkProperCase(column_name)
	elif (func_name == "checkEmail"):
		checkEmail(column_name)
	elif (func_name == "checkDateTime"):
		checkDateTime(column_name)
	elif (func_name == "checkNChars"):
		checkNChars(column_name)

if __name__ == "__main__":
	main()
