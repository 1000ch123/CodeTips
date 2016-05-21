package main

import (
	"net/http"
	"strconv"

	"github.com/labstack/echo"
	"github.com/labstack/echo/engine/standard"
	"github.com/labstack/echo/middleware"
)

type (
	message struct {
		Id   int    `json:"id"`
		Body string `json:"body"`
	}
)

var (
	messages = map[int]*message{}
	seq      = 0
	page_max = 100
)

func fetchMessage(id int) *message {
	return messages[id]
}

func getMessages(c echo.Context) error {
	if messages != nil {
		result := make([]*message, seq, page_max)
		for i := 0; i < seq; i++ {
			result[i] = messages[i]
		}
		return c.JSON(http.StatusOK, result)
	} else {
		return c.NoContent(http.StatusNoContent)
	}
}

func getMessage(c echo.Context) error {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		return err
	}
	m := fetchMessage(id)
	if m != nil {
		return c.JSON(http.StatusOK, m)
	} else {
		return c.String(http.StatusNoContent, "")
	}
}

func createMessage(c echo.Context) error {
	m := &message{
		Id: seq,
	}
	err := c.Bind(m)
	if err != nil {
		return err
	}
	messages[m.Id] = m
	seq += 1

	return c.JSON(http.StatusCreated, m)
}

func updateMessage(c echo.Context) error {
	return c.String(http.StatusOK, "update")
}

func deleteMessage(c echo.Context) error {
	return c.NoContent(http.StatusNoContent)
}

func main() {
	e := echo.New()

	// Middleware
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	// Route => handler
	e.GET("/", func(c echo.Context) error {
		return c.String(http.StatusOK, "Hello, World!\n")
	})

	e.GET("/messages", getMessages)
	e.GET("/messages/:id", getMessage)
	e.POST("/messages", createMessage)
	e.PUT("/messages/:id", createMessage)
	e.DELETE("/messages/:id", createMessage)

	// Start server
	e.Run(standard.New(":1323"))
}
