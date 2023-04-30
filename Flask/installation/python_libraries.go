package installation

import (
	"fmt"
	"os/exec"
)

func Python_pip_install(library string) bool {
	cmd := exec.Command("pip", "install", library)
	output, err := cmd.Output()

	if err != nil {
		fmt.Println("pip failed to install: \n", err)
		return false
	}

	fmt.Println(string(output))
	return true
}
