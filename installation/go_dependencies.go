package installation

import (
	"fmt"
	"os/exec"
)

func Go_get_install(url_link string) bool {
	cmd := exec.Command("go", "get", url_link)
	output, err := cmd.Output()

	if err != nil {
		fmt.Println("Go dependency failed to install: \n", err)
		return false
	}

	fmt.Println(string(output))
	return true
}
