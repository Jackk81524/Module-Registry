package clone_repo

import (
	"os/exec"
)

func CloneRepo(url string, dir string) error {
	// Clone the repository using Git
	cmd := exec.Command("git", "clone", url, dir)
	cmd.Stdout = nil
	cmd.Stderr = nil
	err := cmd.Run()
	//if command returns and error then this function returns and error
	return err
}
