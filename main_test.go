package main

import (
	"fmt"
	"net/http"
	"os"
	"os/exec"
	"testing"

	"github.com/KevinMi2023p/ECE461_TEAM33/bus_factor"
	"github.com/KevinMi2023p/ECE461_TEAM33/npm"
	"github.com/KevinMi2023p/ECE461_TEAM33/rampuptime"
	"github.com/KevinMi2023p/ECE461_TEAM33/responsiveness"
)

func Test_all(t *testing.T) {

	// Initially starts with component testing

	pkgs := []string{
		"xml2js",
		"bluebird",
		"aws-sdk",
		"ts-node",
		"tar",
		"fake",
		"../../ECE461_team33",
	}

	for _, pkg := range pkgs {

		// Code from npm test section -----------------------------------------
		info := npm.Get_NpmInfo(pkg)

		if info == nil {
			t.Errorf("Could not get npm registry info about the package %s\n", pkg)
			// fmt.Println("Could not get npm registry info about the package %s\n", pkg)
		}

		// get repo type
		repoTypeKeys := []string{"repository", "type"}
		repoType := npm.Get_nested_value_from_info(info, repoTypeKeys)
		if repoType != nil {
			if repoType == "git" {
				// get repo address
				repoUrlKeys := []string{"repository", "url"}
				repoUrl := npm.Get_nested_value_from_info(info, repoUrlKeys)
				if repoUrl == nil {
					t.Error("Repo did not have a url")
					// fmt.Println("Repo did not have a url")
				}
			} else {
				t.Error("Repo type was not git")
				// fmt.Println("Repo type was not git")
			}
		} else {
			t.Error("Repo type was nil")
			// fmt.Println("Repo type was nil")
		}

		// test nonexistent keys
		nonkeyTestKeys := []string{"quirky", "keys", "go", "here", "asoignviohw98y4834oihkrn"}
		badKeyResult := npm.Get_nested_value_from_info(info, nonkeyTestKeys)
		if badKeyResult != nil {
			t.Error("Bad keys had non-nil value")
			// fmt.Println("Bad keys had non-nil value")
		}

		//npm section test end -----------------------------------------

		//code from bus_factor test section ----------------------------
		if info == nil {
			// fmt.Printf("Could not get npm registry info about the package %s\n", pkg)
			fmt.Printf("Bus size:\t%3d\n", bus_factor.Get_minimum_bus_size(pkg))
		} else {
			// printKeys(*info)			Private function called out for now
			fmt.Println(npm.Get_nested_value_from_info(info, []string{"maintainers"}))
			fmt.Println(npm.Get_nested_value_from_info(info, []string{"contributors"}))

			// fmt.Printf("Bus size:\t%3d\n", Get_minimum_bus_size(info))
		}

		//bus_factor test section ends ---------------------------------

		//Code from ranpuptime test section ---------------------------
		fmt.Println("Package used:\t" + pkg)

		if info == nil {
			fmt.Println("Couldn't get npm registry")
		} else {
			fmt.Println(rampuptime.Ramp_up_score(info))
			// fmt.Println((*info)["readme"])
		}

		//rampuptime test section ends ---------------------------------

	}

	// Code for responsiveness test begin (no loop needed) -------------

	repos := []string{"https://github.com/KevinMi2023p/ECE461_TEAM33/"}
	token := os.Getenv("GITHUB_TOKEN")

	fmt.Printf("GitHub token:\t%s\n\n", token)

	client := &http.Client{}

	for _, repo := range repos {
		issues := responsiveness.Get_issues(repo, token, client)
		fmt.Printf("Responsiveness for %s:\t%f\n", repo, responsiveness.Responsiveness(issues))
	}

	// responsiveness test section ends --------------------------------

	// Test to see if dependencies installed
	cmd := exec.Command("pip", "--version")
	output, err := cmd.Output()
	if err != nil {
		t.Error("pip isn't installed", output)
	}
}

//Old stuff here
// func MainTest() {
// 	// fmt.Println("Testing has begun")
// 	// exitVal := m.Run()
// 	// fmt.Println("Testing has ended")

// 	// return exitVal

// 	var working = false
// 	if working {
// 		exec.Command("cd", "bus_factor/")
// 		cmd := exec.Command("go", "test")
// 		output, err := cmd.Output()
// 		exec.Command("cd..")

// 		if err != nil {
// 			fmt.Println("Certain test failed")
// 			return
// 		}

// 		fmt.Println(string(output))
// 		return
// 	}

// 	fmt.Println("Testing is done manually by going into each director and running:")
// 	fmt.Println("go test")
// 	fmt.Println("\nNote: not all directories have a testing function")
// }
