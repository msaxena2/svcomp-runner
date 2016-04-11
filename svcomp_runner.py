import sys
import os
import subprocess32 as subprocess
import re



def find_undef_behavior(command):
    sys.stdout.write(" ".join(command) + " --- ")
    sys.stdout.flush()
    error_regex = re.compile('(UB|CV|USP)\-([A-Z]+[0-9]*)')
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait(timeout=1)
        output = process.stderr.read()
        if re.search(error_regex, output):
            return True, output
        return False, ""
    except subprocess.TimeoutExpired:
        return False, ""
    finally:
        process.kill()


location = sys.argv[1]
log_location = sys.argv[2]
tests_run = 0
undefined = 0

def log_result(file, executable, result, output):
    file.write("Executable " + executable + "\n")
    if result:
        sys.stdout.write("UNDEFINED!\n")
        file.write("Found Undefined Behavior! \n")
        file.write(output + "\n")
    else:
        sys.stdout.write("OK!\n")
        file.write("Executable was well defined \n")
    file.write("\n")


def run_example(example_folder):
    global tests_run
    global undefined
    os.chdir(os.path.join(location, "bin", example_folder))
    print("In Directory - " + os.getcwd())
    output_file = open(os.path.join(log_location, example_folder + "-results.txt", "w+"))
    correct_count = 0
    undef_count = 0
    for file in os.listdir(os.getcwd()):
        if "true" in file and file.endswith(".oc"):
            correct_count += 1
            tests_run = tests_run + 1
            undefined = undefined + 1
            result, output = find_undef_behavior(["./" + file])
            log_result(output_file, file, result, output)
            if result:
                undef_count += 1
    output_file.write("Total Executables - " + str(correct_count) + "\n")
    output_file.write("Undefined - " + str(undef_count) + "\n")
    output_file.close()




def main():
    test_file = open("tests.txt", 'r')
    map(lambda y: run_example(y), filter(lambda x : x.split(), test_file.split("\n")))

if __name__ == '__main__':
    main()
