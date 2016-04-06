import sys
import os
import subprocess32 as subprocess
import re


def find_total_file_number():
    total_files = 0
    i_total = 0
    c_total = 0
    for root, dir, files in os.walk(location):
        i_files = filter(lambda x : x.endswith(".i"), files)
        c_files = filter(lambda x: x.endswith(".c"), files)
        if len(c_files) == 0 and len(i_files) > 0:
            print root
            i_total += len(filter(lambda x : "true" in x, i_files))
        else:
            c_total += len(filter(lambda x : "true" in x, c_files))

    total_files = i_total + c_total
    print i_total
    print c_total
    print total_files


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
        sys.stdout.write("Undefined!\n")
        file.write("Found Undefined Behavior! \n")
        file.write(output + "\n")
    else:
        sys.stdout.write("OK!\n")
        file.write("Executable was well defined \n")
    file.write("\n")

total_files = 0
total_c_files = 0
total_i_files = 0
def run_example(example_folder):
    # os.chdir(os.path.join(location, "bin", example_folder))
    # print("In Directory - " + os.getcwd())
    # output_file = open("results.txt", "w+")
    # correct_count = 0
    # undef_count = 0
    # for file in os.listdir(os.getcwd()):
    #     if "true" in file and file.endswith(".oc"):
    #         correct_count += 1
    #         result, output = find_undef_behavior(["./" + file])
    #         log_result(output_file, file, result, output)
    #         if result:
    #             undef_count += 1
    # output_file.write("Total Executables - " + str(correct_count) + "\n")
    # output_file.write("Undefined - " + str(undef_count) + "\n")
    # output_file.close()
    global total_files
    global total_i_files
    global total_c_files
    os.chdir(os.path.join(location, example_folder))
    i_total = 0
    c_total = 0
    for root, dir, files in os.walk(os.getcwd()):
        i_files = filter(lambda x : x.endswith(".i"), files)
        c_files = filter(lambda x: x.endswith(".c"), files)
        if len(c_files) == 0 and len(i_files) > 0:
            print root
            total_i_files += len(filter(lambda x : "true" in x, i_files))
        else:
            total_i_files += len(filter(lambda x : "true" in x and ".i" in x, c_files))
            total_c_files += len(filter(lambda x : "true" in x and ".i" not in x, c_files))

    total_files += i_total + c_total





def main():
    run_example("array-examples")
    run_example("reducercommutativity")
    run_example("array-memsafety")
    run_example("bitvector")
    run_example("bitvector-regression")
    run_example("bitvector-loops")
    run_example("signedintegeroverflow-regression")
    run_example("heap-manipulation")
    run_example("memsafety")
    run_example("memsafety-ext")
    run_example("list-properties")
    run_example("ldv-regression")
    run_example("ddv-machzwd")
    run_example("list-ext-properties")
    run_example("memory-alloca")
    run_example("ldv-memsafety")
    run_example("floats-cdfpl")
    run_example("floats-cbmc-regression")
    run_example("float-benchs")
    run_example("ntdrivers-simplified")
    run_example("ssh-simplified")
    run_example("locks")
    run_example("ntdrivers")
    run_example("ssh")
    run_example("eca-rers2012")
    run_example("loops")
    run_example("loop-acceleration")
    run_example("loop-invgen")
    run_example("loop-lit")
    run_example("loop-new")
    run_example("recursive")
    run_example("recursive-simple")
    run_example("product-lines")
    run_example("systemc")
    run_example("seq-mthreaded")
    run_example("seq-pthread")
    run_example("termination-crafted")
    run_example("termination-crafted-lit")
    run_example("termination-libowfat")
    run_example("termination-memory-alloca")
    run_example("termination-numeric")
    run_example("termination-restricted-15")
    run_example("termination-15")
    run_example("pthread")
    run_example("pthread-atomic")
    run_example("pthread-ext")
    run_example("pthread-wmm")
    run_example("pthread-lit")
    run_example("ldv-races")
    run_example("ldv-linux-3.0")
    run_example("ldv-linux-3.4-simple")
    run_example("ldv-linux-3.7.3")
    run_example("ldv-commit-tester")
    run_example("ldv-consumption")
    run_example("ldv-linux-3.12-rc1")
    run_example("ldv-linux-3.16-rc1")
    run_example("ldv-validator-v0.6")
    run_example("ldv-validator-v0.8")
    run_example("ldv-linux-4.2-rc1")
    run_example("ldv-challenges")
    print total_files
    print total_i_files
    print total_c_files
    #find_total_file_number()

if __name__ == '__main__':
    main()
