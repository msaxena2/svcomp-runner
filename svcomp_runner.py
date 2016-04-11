import sys
import os
import subprocess32 as subprocess
import re

total_tests = 0
total_undefined = 0
location = sys.argv[1]
log_location = sys.argv[2]
includes_location = os.path.join(location, "decls.h")
implementation_location = os.path.join(location, "implementations.c")


def check_result(output):
    error_regex = re.compile('(UB|CV|USP)\-([A-Z]+[0-9]*)')
    if re.search(error_regex, output):
        return True, output
    return False, ""


def log_result(file, executable, result, output):
    file.write("File " + executable + "\n")
    if result:
        sys.stdout.write("UNDEFINED!\n")
        file.write("Found Undefined Behavior! \n")
        file.write(output + "\n")
    else:
        sys.stdout.write("OK!\n")
        file.write("File was well defined \n")
    file.write("\n")


def run_command(command, timeout):
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait(timeout=timeout)
        output = subprocess.stderr.read()
        return check_result(output)
    except subprocess.TimeoutExpired:
        return False, ""
    finally:
        process.kill()


def run_example(example_folder):
    tests_run = 0
    undefined = 0
    global total_tests
    global total_undefined
    os.chdir(os.path.join(location, example_folder))
    print("In Directory - " + os.getcwd())
    output_file = open(os.path.join(log_location, example_folder + "-results.txt", "w+"))
    for file in os.listdir(os.getcwd()):
        if "true" in file and file.endswith(".c"):
            sys.stdout.write("Compiling File " + file + " -- ")
            sys.stdout.flush()
            tests_run += 1
            # compile the file
            executable_name = file.split(".c")[0] + ".out"
            result, output = run_command(
                    ["kcc", "-include", includes_location, file, implementation_location, "-o", executable_name], 10)
            if result:
                sys.stdout.write("UNDEFINED! \n");
                sys.stdout.flush()
                log_result(output_file, file, result, output)
                undefined += 1
                continue
            else:
                # run the executable
                sys.stdout.write("OK! \n");
                sys.stdout.flush()
                sys.stdout.write("Running " + executable_name + " -- ")
                sys.stdout.flush()
                result, output = run_command(["./", executable_name, 2])
                log_result(output_file, file, result, output)
                if result:
                    sys.stdout.write("UNDEFINED!\n")
                    sys.stdout.flush()
                    undefined += 1
                else:
                    sys.stdout.write("OK!\n")
                    sys.stdout.flush()

    output_file.write("Total Executables - " + str(tests_run) + "\n")
    output_file.write("Undefined - " + str(undefined) + "\n")
    output_file.close()
    total_tests += tests_run
    undefined += undefined


def main():
    test_file = open("tests.txt", 'r')
    map(lambda y: run_example(y), filter(lambda x: x.split(), test_file.split("\n")))
    print(str(total_undefined))
    print(str())


if __name__ == '__main__':
    main()
