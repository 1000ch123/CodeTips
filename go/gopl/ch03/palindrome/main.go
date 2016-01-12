package main

import (
	"fmt"
	"os"
)

func main() {
	for i := 1; i < len(os.Args); i++ {
		fmt.Println(IsPalindrome(os.Args[i]))
	}
}

func IsPalindrome(s string) bool {
	// 先頭から真ん中まで，対象位置の文字を比較する
	n := len(s)
	for i := 0; i < n/2; i++ {
		if s[i] != s[n-1-i] {
			return false
		}
	}
	return true
}
