package api

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

// used to make the request string
const issues_url string = "https://api.github.com/repos/KevinMi2023p/ECE461_team33/issues"

// alias of map[string]any (same as map[string]interface{}) because typing that is annoying
type IssuesInfo = map[string]any;

// performs the get request and parses the json
func Get_Issues_Info(pkg string) *IssuesInfo {
	// get request url
	requestUrl := fmt.Sprintf(issues_url, pkg)

	// send get request
	response, responseError := http.Get(requestUrl)

	if (responseError != nil) {
		return nil
	}

	// read response body
	bodyBytes, readError := io.ReadAll(response.Body)

	if (readError != nil) {
		return nil
	}

	var data *IssuesInfo = new(IssuesInfo)

	// parse json from the response body
	jsonError := json.Unmarshal(bodyBytes, data)

	if (jsonError != nil) {
		return nil
	}

	return data
}

// returns the value mapped to key, if info is *map[string]any. otherwise, returns nil
func Get_value_from_info(info any, key string) any {
	if (info == nil) {
		return nil
	}

	switch info.(type) {
		
		case NpmInfo:
			value, noError := info.(IssuesInfo)[key]
			if (noError) {
				return value
				} else {
					return nil
				}
				
		default:
			return nil
	
	}
}

// returns info's value at keys, since info is essentially a nested map with string keys
func Get_nested_value_from_info(info *IssuesInfo, keys []string) any {
	if (info == nil) {
		return nil
	}

	var result any = *info

	for i := 0; i < len(keys); i++ {
		result = Get_value_from_info(result, keys[i])
	}

	return result
}


