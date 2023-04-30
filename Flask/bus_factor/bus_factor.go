package bus_factor

import (
	"fmt"
	"os/exec"
	"strconv"
	"strings"
)

// uses the cloned repository to determine the bus size.
func Get_minimum_bus_size(git_path string) int {
	// analyze the cloned repository at gitPath
	repo_url := fmt.Sprintf("\"%s\"", git_path)
	cmd := exec.Command("python3", "bus_factor/bus_factor.py", repo_url)
	output, err := cmd.Output()
	if (err != nil) {
		return 0
	}

	// parse bus_size from python output
	// fmt.Print(output)
	outputLines := strings.Split(strings.TrimSpace(string(output)), "\r\n")
	// fmt.Println(outputLines)
	i, parseError := strconv.Atoi(outputLines[len(outputLines) - 1])

	if (parseError != nil) {
		return 0
	}

	return i
}

// calculates a bus factor (between 0 and 1) from the bus size
func calculate_bus_factor(bus_size int) float32 {
	if (bus_size < 1) {
		return 0.0
	}

	return (float32(bus_size) - 0.9) / float32(bus_size)
}

// calculates the bus factor by cloning the repo locally then using the truckfactor pyhton library
func Get_bus_factor(githubUrl string) float32 {
	bus_size := Get_minimum_bus_size(githubUrl)
	return calculate_bus_factor(bus_size)
}
