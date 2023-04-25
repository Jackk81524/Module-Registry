
package correctiveness

import (
	"fmt"
	"time"

	"github.com/KevinMi2023p/ECE461_TEAM33/npm"
	"github.com/KevinMi2023p/ECE461_TEAM33/responsiveness"
)

func Correctiveness(issues *[]responsiveness.RepoIssue) float32 {
	if issues == nil {
		return 0
	}
	open_issue_count := 0
	closed_issue_count := 0

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
					i = len(*issues)
					open_issue_count += 1

					// check whether the issue is no longer open and made in the past month
					state := npm.Get_value_from_info(issue, "state")
					if state != nil {
						if state != "open" && duration < (30*24*time.Hour) {
							closed_issue_count += 1
						}
					}
				}
			}
		}
	}

	if closed_issue_count+open_issue_count > 0 {
		return float32(float32(open_issue_count) / float32(open_issue_count+closed_issue_count))
	}

	return 0.5
}
