// Copyright © 2016 Alan A. A. Donovan & Brian W. Kernighan.
// License: https://creativecommons.org/licenses/by-nc-sa/4.0/

// See page 58.
//!+

// Surface computes an SVG rendering of a 3-D surface function.
package main

import (
	"fmt"
	"math"
)

const (
	width, height = 600, 600            // canvas size in pixels
	cells         = 100                 // number of grid cells
	xyrange       = 30.0                // axis ranges (-xyrange..+xyrange)
	xyscale       = width / 2 / xyrange // pixels per x or y unit
	zscale        = height * 0.4        // pixels per z unit
	angle         = math.Pi / 6         // angle of x, y axes (=30°)
)

var sin30, cos30 = math.Sin(angle), math.Cos(angle) // sin(30°), cos(30°)

func main() {
	fmt.Printf("<svg xmlns='http://www.w3.org/2000/svg' "+
		"style='stroke: grey; fill: white; stroke-width: 0.7' "+
		"width='%d' height='%d'>", width, height)
	for i := 0; i < cells; i++ {
		for j := 0; j < cells; j++ {
			ax, ay, af := corner(i+1, j)
			bx, by, bf := corner(i, j)
			cx, cy, cf := corner(i, j+1)
			dx, dy, df := corner(i+1, j+1)

			r, g, b := polygonColor(i, j)

			if af && bf && cf && df {
				fmt.Printf("<polygon points='%g,%g %g,%g %g,%g %g,%g' fill='#%02x%02x%02x'/>\n",
					ax, ay, bx, by, cx, cy, dx, dy, r, g, b)
			}
		}
	}
	fmt.Println("</svg>")
}

func corner(i, j int) (float64, float64, bool) {
	// Find point (x,y) at corner of cell (i,j).
	x := xyrange * (float64(i)/cells - 0.5)
	y := xyrange * (float64(j)/cells - 0.5)

	// Compute surface height z.
	z := f(x, y) * 0.1

	// Project (x,y,z) isometrically onto 2-D SVG canvas (sx,sy).
	sx := width/2 + (x-y)*cos30*xyscale
	sy := height/2 + (x+y)*sin30*xyscale - z*zscale
	return sx, sy, !math.IsInf(z, 1)
}

func f(x, y float64) float64 {
	//r := math.Hypot(x, y)  // distance from (0,0)
	return math.Sin(x) * math.Cos(y) // r
}

func polygonColor(i, j int) (int, int, int) {
	// Find point (x,y) at corner of cell (i,j).
	x := xyrange * (float64(i)/cells - 0.5)
	y := xyrange * (float64(j)/cells - 0.5)

	// Compute surface height z.
	z := f(x, y)
	fmt.Println(z)
	r := int(255 * 0.5 * (1 + z))
	return r, 0, 255 - r
}

//!-
