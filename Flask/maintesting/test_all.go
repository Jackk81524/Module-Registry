package maintesting

import (
	"fmt"
	"os/exec"
)

func MainTest() {
	// fmt.Println("Testing has begun")
	// exitVal := m.Run()
	// fmt.Println("Testing has ended")

	// return exitVal

	var working = false
	if working {
		exec.Command("cd", "bus_factor/")
		cmd := exec.Command("go", "test")
		output, err := cmd.Output()
		exec.Command("cd..")

		if err != nil {
			fmt.Println("Certain test failed")
			return
		}

		fmt.Println(string(output))
		return
	}

	fmt.Println("Testing is done manually by going into each director and running:")
	fmt.Println("go test")
	fmt.Println("\nNote: not all directories have a testing function")
}
