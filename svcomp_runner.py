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
        output = process.stdout.read() + process.stderr.read()
        if re.search(error_regex, output):
            return True, output
        return False, ""
    except subprocess.TimeoutExpired:
        return False, ""
    finally:
        process.kill()


location = sys.argv[1]


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
    os.chdir(os.path.join(location, "bin", example_folder))
    print("In Directory - " + os.getcwd())
    output_file = open("results.txt", "w+")
    correct_count = 0
    undef_count = 0
    for file in os.listdir(os.getcwd()):
        if "true" in file and file.endswith(".oc"):
            correct_count += 1
            result, output = find_undef_behavior(["./" + file])
            log_result(output_file, file, result, output)
            if result:
                undef_count += 1
    output_file.write("Total Executables - " + str(correct_count) + "\n")
    output_file.write("Undefined - " + str(undef_count) + "\n")
    output_file.close()




def main():
    #run_example("array-examples")
    #run_example("bitvector")
    #run_example("bitvector-regression")
    #run_example("bitvector-loops")
    #run_example("signedintegeroverflow-regression")
    #run_example("list-properties")
    #run_example("ldv-regression")
    #run_example("ddv-machzwd")
    #run_example("list-ext-properties")
    #run_example("ldv-memsafety")
    #run_example("floats-cdfpl")
    #run_example("float-benchs")
    #run_example("ssh-simplified")
    #run_example("locks")
    #run_example("loop-acceleration")
    #run_example("loop-invgen")
    #run_example("loop-lit")
    #run_example("systemc")
    #run_example("termination-crafted")
    #run_example("termination-numeric")
    #run_example("termination-restricted-15")
    #run_example("pthread")
    #run_example("pthread-ext")
    #run_example("pthread-wmm")
    run_example("pthread-lit")

if __name__ == '__main__':
    main()
