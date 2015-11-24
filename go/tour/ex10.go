package main

//import "code.google.com/p/go-tour/tree"
import "fmt"

// Walk walks the tree t sending all values
// from the tree to the channel ch.
func Walk(t *tree.Tree, ch chan int) {

	step(t, ch)
	close(ch)

}

func step(t *tree.Tree, ch chan int) {
	if t.Left != nil {
		step(t.Left, ch)
	}

	ch <- t.Value

	if t.Right != nil {
		step(t.Right, ch)
	}

	return
}

// Same determines whether the trees
// t1 and t2 contain the same values.
func Same(t1, t2 *tree.Tree) bool {
	ch1 := make(chan int)
	ch2 := make(chan int)
	go Walk(t1, ch1)
	go Walk(t2, ch2)

	for v1 := range ch1 {
		v2 := <-ch2
		fmt.Println(v1, v2)

		if v1 != v2 {
			return false
		}
	}

}

func main() {
	size := 10
	ch := make(chan int, size)
	t := tree.New(size)

	go Walk(t, ch)

	for v := range ch {
		fmt.Println(v)
	}

	fmt.Println(Same(tree.New(10), tree.New(10)))
}
