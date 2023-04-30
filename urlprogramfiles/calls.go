package urlprogramfiles

import (
	"fmt"
	"strings"
)

// Function to check if the given URL is from
// npmjs.com domain or directly from GitHub
func Check_valid_url(given_url string) bool {
	given_url = strings.ToLower(given_url)

	if !strings.Contains(given_url, "npmjs.com") && !strings.Contains(given_url, "github.com") {
		fmt.Println("Invalid URL given (not from npmjs.com or GitHub)")
		return false
	}

	return true
}
