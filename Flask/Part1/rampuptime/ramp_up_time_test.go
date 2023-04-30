package rampuptime

import (
	"fmt"
	"testing"

	"github.com/KevinMi2023p/ECE461_TEAM33/npm"
)

func TestMain(m *testing.M) {
	pkgs := []string{
		"https://registry.npmjs.org/xml2js",
		"https://registry.npmjs.org/bluebird",
		"https://registry.npmjs.org/aws-sdk",
		"https://registry.npmjs.org/ts-node",
		"https://registry.npmjs.org/tar",
		"https://registry.npmjs.org/fake",
	}

	for _, pkg := range pkgs {
		info := npm.Get_NpmInfo(pkg)
		fmt.Println("Package used:\t" + pkg)

		if info == nil {
			fmt.Println("Couldn't get npm registry")
		} else {
			fmt.Println(Ramp_up_score_npm(info))
			// fmt.Println((*info)["readme"])
		}
	}
}
