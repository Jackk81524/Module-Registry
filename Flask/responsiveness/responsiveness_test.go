package responsiveness

import (
	"fmt"
	"net/http"
	"os"
	"testing"
)

func TestMain(m *testing.M) {
	repos := []string{
		"https://api.github.com/repos/KevinMi2023p/ECE461_TEAM33",
		"https://api.github.com/repos/lodash/lodash",
	}

	token := os.Getenv("GITHUB_TOKEN")

	fmt.Printf("GitHub token:\t%s\n\n", token)
	
	client := &http.Client{}

	for _, repo := range repos {
		issues := Get_issues(repo, token, client)
		fmt.Printf("Responsiveness for %s:\t%f\n", repo, Responsiveness(issues))
	}
}
