package rampuptime

import (
	"encoding/json"
	"fmt"
	"net/http"
	"regexp"

	. "github.com/KevinMi2023p/ECE461_TEAM33/common"
	. "github.com/KevinMi2023p/ECE461_TEAM33/npm"
)

const github_readme_url_part string = "%s/readme"

// This module uses the "npm" package that's created locally
func Ramp_up_score_npm(json_data *NpmInfo) float32 {
	//Below is a link of what <json_data> should be
	//https://github.com/npm/registry/blob/master/docs/responses/package-metadata.md

	if json_data == nil {
		// fmt.Println("NPM package hasn't been called yet or doesn't exist")
		return 0
	}

	//Look through map to get README data
	var readme_string = Get_nested_value_from_info(json_data, []string{"readme"})
	if readme_string == nil {
		// fmt.Println("Couldn't read README file")
		return 0
	}

	return calculate_score(readme_string.(string))
}

type ReadmeInfo = map[string]any

// gets a json with readme info from json
func get_readme_info_from_github(repo_api string, token string, client *http.Client) *ReadmeInfo {
	request_url := fmt.Sprintf(github_readme_url_part, repo_api)
	body_bytes := Get_body_from_github_api(request_url, token, client)
	if body_bytes == nil || len(body_bytes) == 0 {
		return nil
	}

	var data *ReadmeInfo = new(ReadmeInfo)

	// parse json from the response body
	json_error := json.Unmarshal(body_bytes, data)

	if json_error != nil {
		// fmt.Print("Json Error:\t")
		// fmt.Println(json_error)
		return nil
	}

	return data
}

// this uses the github api to get the readme, then calculate the score
func Ramp_up_score_github(repo_api string, token string, client *http.Client) float32 {
	// query github for the readme info
	info := get_readme_info_from_github(repo_api, token, client)
	if info == nil {
		return 0
	}

	// Look through map to get README url
	readme_url := Get_nested_value_from_info(info, []string{"download_url"})
	if readme_url == nil {
		return 0
	}

	// get the readme
	readme_bytes := Get_body_from_url(readme_url.(string), client)
	if readme_bytes == nil {
		return 0
	}

	return calculate_score(string(readme_bytes))
}

// Puts string of readme and returns the score
func calculate_score(readme string) float32 {
	reg, err := regexp.Compile("[^A-Za-z0-9]+")
	if err != nil {
		// fmt.Println("Regex failed to compile")
		return 0
	}

	var filter_readme string = reg.ReplaceAllString(readme, "")

	var len_filter int = len(filter_readme)
	var good_amount int = 1000 //if a README has a 1000 character, it should have enough information

	//Condition for perfect score
	if len_filter >= good_amount {
		return 1.0
	}

	return float32(len_filter) / float32(good_amount)
}
