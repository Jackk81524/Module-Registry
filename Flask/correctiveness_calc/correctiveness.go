package correctiveness

import (
	"fmt"
	"time"

	"github.com/KevinMi2023p/ECE461_TEAM33/npm"
	"github.com/KevinMi2023p/ECE461_TEAM33/responsiveness"
)

func Correctiveness(issues *[]responsiveness.RepoIssue) float32 {
	if issues == nil {
		return 0.5
	}
	var openedIssues []map[string]interface{}
	var closedIssues []map[string]interface{}

	for _, issue := range *issues {
		// check whether the issue is open
		labels := npm.Get_value_from_info(issue, "labels").([]interface{})

		for i := 0; i < len(labels); i++ {
			state := npm.Get_value_from_info(issue, "state")
			issuetime := npm.Get_value_from_info(issue, "created_at")
			createdAt, err := time.Parse(time.RFC3339, issuetime.(string))
			if err != nil {
				fmt.Println("Error parsing time of issue created", err)
				// Handle error
			}

			// Get the current time
			now := time.Now()

			// Calculate the duration between the "created_at" time and now
			duration := now.Sub(createdAt)

			// if this state is "open" and made in the past month
			if state != nil {
				if state == "open" && duration < (30*24*time.Hour) {
					i = len(labels)
					openedIssues = append(openedIssues, map[string]interface{}{
						"created_at": issuetime,
						"closed_at":  nil,
					})

					// check whether the issue is no longer open and made in the past month
					state := npm.Get_value_from_info(issue, "state")
					if state != nil {
						if state != "open" && duration < (30*24*time.Hour) {
							closedIssues = append(closedIssues, map[string]interface{}{
								"created_at": issuetime,
								"closed_at":  npm.Get_value_from_info(issue, "closed_at"),
							})
						}
					}
				}
			}
		}
	}

	// Calculate the correctness score using the opened and closed issues.
	return float32((calculateCorrectnessScoreFromIssues(openedIssues, closedIssues)))
}

func calculateCorrectnessScoreFromIssues(openedIssues []map[string]interface{}, closedIssues []map[string]interface{}) float64 {
	// Calculate the total duration of all opened issues.
	var totalOpenDuration float64
	for _, issue := range openedIssues {
		createdTime, _ := time.Parse(time.RFC3339, issue["created_at"].(string))
		closedTime := time.Now().UTC()
		if issue["closed_at"] != nil {
			closedTime, _ = time.Parse(time.RFC3339, issue["closed_at"].(string))
		}
		duration := closedTime.Sub(createdTime).Hours()
		totalOpenDuration += duration
	}

	// Calculate the total duration of all closed issues.
	var totalClosedDuration float64
	for _, issue := range closedIssues {
		createdTime, _ := time.Parse(time.RFC3339, issue["created_at"].(string))
		closedTime, _ := time.Parse(time.RFC3339, issue["closed_at"].(string))
		duration := closedTime.Sub(createdTime).Hours()
		totalClosedDuration += duration
	}

	// Calculate the average duration of opened and closed issues.
	var avgOpenDuration float64
	if len(openedIssues) > 0 {
		avgOpenDuration = ((totalClosedDuration + totalOpenDuration) / 2)
	}
	return (avgOpenDuration)
}
