import sys
import os

def print_list(std_or_log_file, service_name, file_name, list):
    if std_or_log_file is "std":
        _print_to_std(service_name,file_name, list)
    else:
        _print_to_log_file(service_name,file_name, list)



def _print_to_std(service_name,file_name, list):
     print("-------------------------------")
     print("------- %s -------" % service_name)
     print("---- %s ----" % file_name)
     print("-------------------------------")
     for item in list:
         print(item)
         print("\n")
     print("-------------------------------")
     print("-------------------------------")


# Based on https://stackabuse.com/writing-to-a-file-with-pythons-print-function/
def _print_to_log_file(service_name,file_name, list):
    original_stdout = sys.stdout  # Save a reference to the original standard output

    folder_path = 'inventory/summary/'+service_name+'/'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_name = file_name+'.txt'


    # mode = 'a' if os.path.exists(writepath) else 'w'

    with open(folder_path+file_name, 'w+') as f:
        sys.stdout = f  # Change the standard output to the file we created.
        _print_to_std(service_name, file_name, list)
        sys.stdout = original_stdout  # Reset the standard output to its original value