import os

#	WELCOME--------------------------------------------------------------
os.system('cls')	# Clear screen
print("\n -------------------------------------")
print("| Welcome to the batch programmer! |")
print(" -------------------------------------\n")


#	INITIALIZATION-------------------------------------------------------
PATH = os.getcwd()

User = os.getlogin()
BUILD_PATH = "C:/Users/" +User+ "/Documents/Arduino/Builds"

my_programmer = "usbtiny"
my_mcu = ""

MCU_s = { "ATtiny85":"t85", "ATMEGA328P":"m328p" }	# A dictionary with the mcu's we use


#	FUNCTIONS------------------------------------------------------------
#	This function returns how much chips you choose to program
def choose_quantity():
	while 1:
		while 1:
			count = input("How much do you want? [Give a number]: ")			
			try:
				count = int(count)
				break
			except ValueError:
				print("This is not a number")		
		
		print("You choose", count,"!")
		
		choise = input("Are you sure you need this much? (y/N)(Press Q to Quit): ")
		match choise:
			case "Y" | "y":
				return count
			case "Q" | "q":
				return 0 


#	This function return a string as a name for a folder
#	Takes as input a flag that let the function know if it needs to include in the menu the choice to create a new folder
def choose_folder(plus): # "plus" -> 0,1 // 0 = No new folder
	dir_list = list(filter(os.path.isdir, os.listdir())) # This is a list of the directory in the current path
	if plus == 1: # Check the flag 
		dir_list.append("Add a new folder")
	while 1:
		
		while 1:
			for i in range(len(dir_list)):
				print(i+1, ")", dir_list[i]) # Print all directories that you found
			try: 
				choose = int(input('\nChoose a number[1-{}]:'.format(i+1)))
				break
			except ValueError:
				os.system('cls')	# Clear screen
				print("\nThis is not a valid value!\n")
				
		if (1 <= choose) and (choose <= i+1):
			folder = dir_list[choose-1]
			break
	
	if os.path.isdir(folder) == False :
		folder = str(input("Choose a folder: "))
	return folder
	
	
#	Programming routine of the chips
def programming_routine(counter):	#	The input needs a int. This number gives the program how many chips will be programmed
	hex_file = file_find()	#	Find the file first
	batch = counter
	while counter > 0:	
		exit_status = programmer(hex_file)	#	Program each microcontroller independently
		match exit_status:
			case 0:
				counter -= 1
				input("OK.Press any key to continue! [{}/{}]".format(batch-counter, batch))
			case _:
				choise = input("\nSomething gone wrong! (Press Any Key to Continue)(Press Q to Quit): ")
				match choise:
					case "Q" | "q":
						return 1 

		
#	The actual programming of each chip
def programmer(file):	#	The input needs a *.ino.hex file to read from and write to the chip
	os.chdir(BUILD_PATH)	# Change to the build directory
	command = "avrdude -v -p "+my_mcu+" -c "+my_programmer+" -U lfuse:w:0xE2:m -U flash:w:"+file 
	print("Programming...")
	exit_status = os.system(command)
	return exit_status


#	Find the build file
def file_find():
	file = [x for x in os.listdir(BUILD_PATH) if x.endswith('.ino.hex')]
	return file[0]


#	Check if the directory that I give as attributes exists
def check_dir(dir):
	isdir = os.path.isdir(dir)
	match isdir:
		case True:
			return 0 
		case _:
			return 1


#	Utility function that backup each kind of memory from the MCU and copies it to a folder
def mcu_backup(restore_folder):	#	"restore_folder" is the folder that the files going to be saved
	isdir = check_dir(restore_folder)
	match isdir:
		case 0:	
			os.chdir(restore_folder)	#	change directory restore_folder you want to save the results 
			mem_type = ["eeprom", "flash", "signature", "lfuse", "hfuse", "efuse"]
			for m in mem_type:
				command = "avrdude -p "+my_mcu+" -c "+my_programmer+" -n -U "+m+":r:"+m+".hex:i"
				os.system(command)
			return 0
		case _:
			choise = input("Directory doesn't exists. Do you want to create it? (y/N)")
			match choise:
				case "Y" | "y":
					os.mkdir(restore_folder)
					mcu_backup(restore_folder)
				case _:
					return 1
		
		
#	Write the MCU's	default state in the MCU	
def mcu_restore(backup_folder):	#	"backup_folder" is the folder restore_folder are the saved files from the backup 
	isdir = check_dir(backup_folder)	#	Check if the folder exists
	match isdir:
		case 0:
			os.chdir(backup_folder)	#	In which folder you want to save the results 
			mem_type = ["eeprom", "flash", "lfuse", "hfuse", "efuse"]
			for m in mem_type:
				command = "avrdude -p "+my_mcu+" -c "+my_programmer+" -U "+m+":w:"+m+".hex"
				print(command)
				os.system(command)
			return 0
		case _:
			print("The folder probably doesn't exist!")
			return 1


#	Classes for the the main menu objects
class menu_object:
	def __init__(self, id, out, cmd):
		self.name = id
		self.output = out
		self.command = cmd
	

#	The Main Menu of the script
def main_menu():
	while 1:
		for i in range(len(menu_list)):
			print(i+1,")",menu_list[i].output)
		try:
			choose = int(input("\nWhat do you want to do? [1-{}]: ".format(i+1)))
			if 0 < choose & choose <= len(menu_list):
				break
		except ValueError:
			os.system('cls')	# Clear screen
			print("This is not a correct choise.\n")
	code_obj = compile(menu_list[choose-1].command, '<string>', 'exec')	# This command executes the command that the following objects are initialized with.
	exec(code_obj)
	

#	Function for choosing and saving the MCU that you want
def get_mcu():
	while 1:
		count = 1
		for i in list(MCU_s):
			print(count,")",i)
			count += 1
		try:
			choice = int(input("\nChoose what MCU you want to use: "))
			if choice > 0 and choice < count :
				break
		except ValueError:
			print("The value you gave is wrong!")
	
	os.system('cls')	# Clear screen
	return list(MCU_s)[choice-1]
	
	
# 	Objects initialization for the main menu.----------------------------
#	menu_object(name, output, command)
menu_list = [
	menu_object("at85", "Program ATtiny85", 'programming_routine(choose_quantity())'),
	menu_object("backup", "Backup a Chip",'mcu_backup(choose_folder(1))'),
	menu_object("restore", "Restore a Chip",'mcu_restore(choose_folder(0))'),
	menu_object("restore", "Restore ATtiny85 in it's default state",'mcu_restore("ATtiny_85_default_state")'),
	menu_object("quit", "Quit",'pass')]


#	MAIN-----------------------------------------------------------------	
my_mcu = get_mcu()
main_menu()
input("\n\nPress Any Key to Quit!")
os.system('cls')	# Clear screen
