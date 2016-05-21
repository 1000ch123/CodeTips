package main

import (
	"encoding/json"
	"fmt"
	"github.com/syndtr/goleveldb/leveldb"
)

type Message struct {
	Id   int
	Body string
}

func main() {
	// connection
	db, err := leveldb.OpenFile("./level", nil)
	if err != nil {
		return
	}
	defer db.Close()

	// data
	m := &Message{1, "message"}
	json_data, err := json.Marshal(m)
	if err != nil {
		return
	}

	// insert
	err = db.Put([]byte("key"), json_data, nil)
	if err != nil {
		return
	}

	// fetch
	data, err := db.Get([]byte("key"), nil)
	if err != nil {
		return
	}
	fmt.Println(string(data))
}
