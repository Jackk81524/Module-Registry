package npm

import (
	"testing"
)

func TestGet_NpmInfo(t *testing.T) {
	pkgs := []string{ "xml2js" }

	for _, pkg := range pkgs {
		info := Get_NpmInfo(pkg)
	
		if (info == nil) {
			t.Errorf("Could not get npm registry info about the package %s\n", pkg)
		}
	
		// get repo type
		repoTypeKeys := []string{ "repository", "type" }
		repoType := Get_nested_value_from_info(info, repoTypeKeys)
		if (repoType != nil) {
			if (repoType == "git") {
				// get repo address
				repoUrlKeys := []string{ "repository", "url" }
				repoUrl := Get_nested_value_from_info(info, repoUrlKeys)
				if (repoUrl == nil) {
					t.Error("Repo did not have a url")
				}
			} else {
				t.Error("Repo type was not git")
			}
		} else {
			t.Error("Repo type was nil")
		}
	
		// test nonexistent keys
		nonkeyTestKeys := []string{ "quirky", "keys", "go", "here", "asoignviohw98y4834oihkrn" }
		badKeyResult := Get_nested_value_from_info(info, nonkeyTestKeys)
		if (badKeyResult != nil) {
			t.Error("Bad keys had non-nil value")
		}
	}
}