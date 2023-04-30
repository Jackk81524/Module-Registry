package common

import (
	"fmt"
	"io"
	"net/http"
)

const bearer_auth_part string = "Bearer %s"

// creates a get request or returns nil
func Create_get_request(request_url string) *http.Request {
	// create new request
	request, request_error := http.NewRequest("GET", request_url, nil)

	if (request_error != nil) {
		// fmt.Print("Request Error:\t")
		// fmt.Println(request_error)
		return nil
	}

	return request
}

// gets bytes from request
func Get_body_from_request(request *http.Request, client *http.Client) []byte {
	response, response_error := client.Do(request)

	if (response_error != nil) {
		// fmt.Print("Response Error:\t")
		// fmt.Println(response_error)
		return nil
	}

	// read response body
	defer response.Body.Close()
	body_bytes, read_error := io.ReadAll(response.Body)

	if (read_error != nil) {
		// fmt.Print("Read Error:\t")
		// fmt.Println(read_error)
		return nil
	}

	return body_bytes
}

// gets the body at the url
func Get_body_from_url(request_url string, client *http.Client) []byte {
	request := Create_get_request(request_url)
	if (request == nil) {
		return nil
	}

	return Get_body_from_request(request, client)
}

// gets bytes from github request
func Get_body_from_github_request(request *http.Request, token string, client *http.Client) []byte {
	auth := fmt.Sprintf(bearer_auth_part, token)

	// add bearer token to the header
	request.Header.Add("Accept", "application/vnd.github+json")
	request.Header.Add("Authorization", auth)
	request.Header.Add("X-GitHub-Api-Version", "2022-11-28")

	// do request
	return Get_body_from_request(request, client)
}

// gets the response body from a get request on the github rest api
func Get_body_from_github_api(request_url string, token string, client *http.Client) []byte {
	request := Create_get_request(request_url)
	if (request == nil) {
		return nil
	}

	return Get_body_from_github_request(request, token, client)
}
