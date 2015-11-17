package main

import (
	"fmt"
	"strings"
)

func WordCount(s string) map[string]int {
	result := make(map[string]int)

	for _, v := range strings.Fields(s) {
		result[v]++
	}
	return result
}

func main() {
	text := "ah ah nya"
	fmt.Println(WordCount(text))
}
