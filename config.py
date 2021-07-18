import json
import os
import sys
import pandas as pd

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




def createConfig(table_name, datatype, df):
	'''
	creates config file using the parameters passed, table name, filetype, and the pandas dataframe df and stores it as config.json
	the user will have to manually edit config.json with the appropriate filters
	'''
	
	print("\n\n\t\t\t\t\t----------CONFIG CREATOR----------\n")

	config['table_name'] = table_name

	config["filetype"] = filetype
	
	config['num_columns'] = len(df.columns)

	config['columns'] = [] 
	for i in range(len(num_columns)):
		col_name = df.column[i]

		filter_choices = ""

		config['columns'].append({
			'name': col_name,
			'filters': filter_choices
			})

	# script_dir = os.path.dirname(__file__)
	# rel_path = "configs/user_defined/" + config_name + ".json" 
	# abs_file_path = os.path.join(script_dir, rel_path)
	with open(config.json, 'a') as config_file:
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
