package main

import (
	"fmt"
	"net/http"
)

// /view/<title> として渡すされたtitleのpageを読み込む
func viewHandler(w http.ResponseWriter, r *http.Request) {
	title := r.URL.Path[len("/view/"):]
	p, _ := loadPage(title)
	fmt.Fprintf(w, "<h1>%s</h1><div>%s</div>", p.Title, p.Body)
}

func main() {
	http.HandleFunc("/view/", viewHandler)
	http.ListenAndServe(":12345", nil)
}
