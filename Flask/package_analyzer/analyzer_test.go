package package_analyzer

import (
	"fmt"
	// "regexp"
	"testing"
)

func TestMain(m *testing.M) {
	urls := []string{
		"https://github.com/cloudinary/cloudinary_npm",
		"https://www.npmjs.com/package/express",
		"https://github.com/nullivex/nodist",
		"https://github.com/lodash/lodash",
		"https://www.npmjs.com/package/browserify",
		"https://github.com/KevinMi2023p/ECE461_team33",
	}

	for _, url := range urls {
		// if (Github_package_regex.MatchString(url)) {
		// 	fmt.Printf("%s\t:\t%s\t%s\n", url, Github_package_regex.FindAllStringSubmatch(url, -1)[0][1], Github_package_regex.FindAllStringSubmatch(url, -1)[0][2])
		// }
		metrics := Analyze(url)
		if (metrics != nil) {
			fmt.Println(Metrics_toString(*metrics))
		}

	}
}
