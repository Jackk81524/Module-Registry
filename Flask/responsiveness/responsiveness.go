package responsiveness

import (
	"encoding/json"
	"fmt"
	"net/http"
	. "github.com/KevinMi2023p/ECE461_TEAM33/common"
	. "github.com/KevinMi2023p/ECE461_TEAM33/npm"
)

// used to make the request string
const github_issues_url_part string = "%s/issues?filter=all&state=all&per_page=100&page=%d"

// alias of map[string]any (same as map[string]interface{}) because typing that is annoying
type RepoIssue = map[string]any;

// performs the get request and parses the json
func Get_issues(repo_api string, token string, client *http.Client) *[]RepoIssue {
	request_url := fmt.Sprintf(github_issues_url_part, repo_api, 1)
	body_bytes := Get_body_from_github_api(request_url, token, client)
	if (body_bytes == nil || len(body_bytes) == 0) {
		return nil
	}

	var data *[]RepoIssue = new([]RepoIssue)
	var data_all *[]RepoIssue

	// parse json from the response body
	json_error := json.Unmarshal(body_bytes, data)

	if (json_error != nil) {
		// fmt.Print("Json Error:\t")
		// fmt.Println(json_error)
		return nil
	}

	data_all = data

	for n := 2; data != nil && len(*data) == 100; n++ {
		request_url = fmt.Sprintf(github_issues_url_part, repo_api, n)
		body_bytes = Get_body_from_github_api(request_url, token, client)
		if (body_bytes == nil || len(body_bytes) == 0) {
			break
		}
	
		data = new([]RepoIssue)
	
		// parse json from the response body
		json_error = json.Unmarshal(body_bytes, data)
	
		if (json_error != nil) {
			// fmt.Print("Json Error:\t")
			// fmt.Println(json_error)
			break
		}
		
		*data_all = append(*data_all, *data...)
	}

	return data_all
}

// calculate responsiveness from repo issues
func Responsiveness(issues *[]RepoIssue) float32 {
	if (issues == nil) {
		return 0
	}

	bugCount := 0
	closedBugs := 0

	for _, issue := range *issues {
		// check whether the issue is a bug
		labels := Get_value_from_info(issue, "labels").([]interface{})

		for i := 0; i < len(labels); i++ {
			name := Get_value_from_info(labels[i], "name")

			// if this label is "Bug"
			if (name != nil) {
				if (name.(string) == "Bug") {
					i = len(labels)
					bugCount += 1

					// check whether the issue is no longer open
					state := Get_value_from_info(issue, "state")
					if (state != nil) {
						if (state != "open") {
							closedBugs += 1
						}
					}
				}
			}
		}
	}

	if (bugCount > 0) {
		return float32(closedBugs) / float32(bugCount)
	}
	
	return 0.5
}
