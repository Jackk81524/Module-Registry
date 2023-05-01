package license_compatibility

import (
	_"os"
	"testing"
	"fmt"
	_"github.com/KevinMi2023p/ECE461_TEAM33/npm"
)

func TestMain(m *testing.M) {
	
	test1 := "afl-3.0"
	test2 := "mit"
	test3 := "bsd-3-clause-clear"
	test4 := "ncsa"
	test5 := "lppl-1.3c"
	test6 := " "
	test7 := "_afl_3.0_"
	test8 := " c c "
	test9 := "wtf-pl"
	test10 := "_-_-"
	
	// Outputs score of 0 or 1.0 depending on if license is detected
	
	if calculate_license_score(test1) == 1.0 {
		fmt.Printf("License compatibility score for %s: %.1f\n", test1, calculate_license_score(test1))
	}

	if calculate_license_score(test2) == 1.0 {
		fmt.Printf("License compatibility score for %s: %.1f\n", test2, calculate_license_score(test2))
	}

	if calculate_license_score(test3) == 1.0 {
		fmt.Printf("License compatibility score for %s: %.1f\n", test3, calculate_license_score(test3))
	}

	if calculate_license_score(test4) == 1.0 {
		fmt.Printf("License compatibility score for %s: %.1f\n", test4, calculate_license_score(test4))
	}

	if calculate_license_score(test5) == 1.0 {
		fmt.Printf("License compatibility score for %s: %.1f\n", test5, calculate_license_score(test5))
	}

	if calculate_license_score(test6) == 0 {
		fmt.Printf("License compatibility score for %s: %d\n", test6, int(calculate_license_score(test6)))
	}

	if calculate_license_score(test7) == 0 {
		fmt.Printf("License compatibility score for %s: %d\n", test7, int(calculate_license_score(test7)))
	}

	if calculate_license_score(test8) == 0 {
		fmt.Printf("License compatibility score for %s: %d\n", test8, int(calculate_license_score(test8)))
	}

	if calculate_license_score(test9) == 0 {
		fmt.Printf("License compatibility score for %s: %d\n", test9, int(calculate_license_score(test9)))
	}

	if calculate_license_score(test10) == 0 {
		fmt.Printf("License compatibility score for %s: %d\n", test10, int(calculate_license_score(test10)))
	}

}
