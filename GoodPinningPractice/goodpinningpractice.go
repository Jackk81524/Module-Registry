package GoodPinningPractice

import (
	"regexp"
)

func GoodPinningPractice(dependencies map[string]string) float32 {
	count := 0
	total := 0

	for _, v := range dependencies {
		total++
		if checkDependency(v) {
			count++
		}
	}

	if total == 0 {
		return 1.0
	}

	return float32(count) / float32(total)
}

func checkDependency(dep string) bool {
	if dep[0] == '^' {
		return false
	}

	if dep[0] == '<' || dep[0] == '>' || dep[:2] == ">=" || dep[:2] == "<=" {
		return false
	}

	r := regexp.MustCompile(`=*[\d]+\.[\d]+\.[\d]+`)
	if r.MatchString(dep) {
		return true
	}

	if dep[0] == '~' {
		r = regexp.MustCompile(`~[\d]+\.[\d]+`)
		if r.MatchString(dep) {
			return true
		}
	}

	return false
}
