import os

#	WELCOME--------------------------------------------------------------
print("\n -------------------------------------")
print("| Welcome to the repeated programmer! |")
print(" -------------------------------------\n")

#	INITIALIZATION-------------------------------------------------------
PATH = os.getcwd()

User = os.getlogin()
BUILD_PATH = "C:/Users/" +User+ "/Documents/Arduino/Builds"

my_programmer = "usbtiny"
my_mcu = "t85"

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


#	Programming routine of the chips
def programming_routine(counter):	#	The input needs a int. This number gives the program how many chips will be programmed
	hex_file = file_find()	#	Find the file first
	while counter > 0:	
		exit_status = programmer(hex_file)	#	Program each microcontroller independently
		match exit_status:
			case 0:
				counter -= 1
				input("OK.Press any key to continue!")
			case _:
				choise = input("Something gone wrong! (Press Any Key to Continue)(Press Q to Quit): ")
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


#	Utility function that take each kind of memory from the MCU and copies it to a folder
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
				os.system(command)
			return 0
		case _:
			print("The folder probably doesn't exist!")
			return 1


def main_menu():
	pass
	return 0
	
#	MAIN-----------------------------------------------------------------

mcu_backup("tested")

# programming_routine(choose_quantity())
input("Press Any Key to Quit!")