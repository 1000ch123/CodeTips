package main

import (
	"fmt"
	"math"
)

func Sqrt(x float64) float64 {
	z := 1.0
	cnt := 0
	for math.Abs(z*z-x) > 0.00001 {
		z = z - (z*z-x)/(2*z)
		cnt++
	}
	fmt.Println(cnt)
	return z
}

func main() {
	fmt.Println(Sqrt(2))
}
