package license_compatibility

import (
	_"os"
	"strings"
	"github.com/KevinMi2023p/ECE461_TEAM33/npm"
)

func License_compatibity(json_data *npm.NpmInfo) float32 {
	if json_data == nil {
		// fmt.Println("NPM package doesn't exist or hasn't been called")
		return 0
	}

	// Get README data from map
	var github_readme_str = npm.Get_nested_value_from_info(json_data, []string{"readme"})
	if github_readme_str == nil {
		// fmt.Println("README file couldn't be read")
		return 0
	}

	return calculate_license_score(github_readme_str.(string))
}

// Checks the output of getLicenseScore and assigns score of 0 if no output and or 1.0 is license is read
func calculate_license_score(github_readme_str string) float32 {
	project_licenses := []string{"afl-3.0", "apache-2.0", "artistic-2.0", "bsl-1.0", "bsd-2-clause",
	"bsd-3-clause", "bsd-3-clause-clear", "cc", "cc0-1.0", "cc-by-4.0", "cc-by-sa-4.0", "wtfpl", 
	"ecl-2.0", "epl-1.0", "epl-2.0", "eupl-1.1", "agpl-3.0", "gpl", "gpl-2.0", "gpl-3.0", "lgpl", 
	"lgpl-3.0", "isc", "lppl-1.3c", "ms-pl", "mit", "mpl-2.0", "osl-3.0", "postgresql", "ofl-1.1", "ncsa", "unlicense", "zlib"}
	
	for _, license := range project_licenses {
		if strings.Contains(github_readme_str, license) {
			return 1.0
		}
	}
	return 0
}
