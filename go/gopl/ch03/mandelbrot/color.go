package main

import (
	"fmt"
	"image/color"
)

func main() {
	var c color.RGBA
	c.R = 200
	fmt.Println(c.R, c.G, c.B, c.A)
}
