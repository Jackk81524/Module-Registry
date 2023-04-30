import os

needed_pip_libraries = ["GitPython", "truckfactor"]

try:
    terminal_output = os.popen("pip list")
    pip_list = terminal_output.read()

    packages = pip_list.splitlines()
    
    temp = set()
    for i in range(2, len(packages)):
        temp.add(packages[i].split()[0])
    
    packages = temp

    for lib in needed_pip_libraries:
        if lib in packages:
            print(f"PASS: {lib} installed on machine")
        else:
            print(f"FAIL: {lib} not found")

except:
    print("pip library not install yet")

