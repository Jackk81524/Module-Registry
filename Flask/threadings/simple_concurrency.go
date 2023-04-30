package threadings

import (
	"fmt"
	"sync"
)

// Global slice (when we add data from running analysis)
var global_slice []int

// Frame to set up simple concurrency
func Setup_simple_routine(events *[]string) {
	var number_of_events = len(*events)

	// Waitgroup means function won't exit until all routines finish
	var wg sync.WaitGroup
	wg.Add(number_of_events)

	// Loop for each thread event
	for i := 0; i < number_of_events; i++ {
		go func(i_cpy int) {
			do_event((*events)[i_cpy], i_cpy)
			wg.Done()
		}(i)
	}

	wg.Wait()
}

// Concurrency / thread, for each event
// Should be able to drop functions here
func do_event(parameter string, iter int) {
	fmt.Println(parameter, iter)
	global_slice = append(global_slice, iter)
}

// Returns final result
func Get_global() []int {
	return global_slice
}
