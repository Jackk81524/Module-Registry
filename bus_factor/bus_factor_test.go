package bus_factor

import (
	"fmt"
	"testing"
	"github.com/KevinMi2023p/ECE461_TEAM33/npm"
)

func printKeys(m any) {
	mm := m.(map[string]any)
	for k, _ := range mm {
		fmt.Println(k)
	}
	fmt.Println("")
}

func TestMain(m *testing.M) {
	pkgs := []string{  }
	for _, pkg := range pkgs {
		info := npm.Get_NpmInfo(pkg)
		if (info == nil) {
			fmt.Printf("Could not get npm registry info about the package %s\n", pkg)
			fmt.Printf("Bus size:\t%3d\n", Get_minimum_bus_size(pkg))
		} else {
			printKeys(*info)
			fmt.Println(npm.Get_nested_value_from_info(info, []string{ "maintainers" }))
			fmt.Println(npm.Get_nested_value_from_info(info, []string{ "contributors" }))
			
			fmt.Printf("Bus size:\t%3d\n", Get_minimum_bus_size(pkg))
		}

	}
}