package svc

import (
	"github.com/gin-gonic/gin"
	"strconv"
)

type WebOptions struct {
	Port int `mapstructure:"port"`
}

type Web struct {
	db   *SqlDatabase
	port int
}

func NewWeb(db *SqlDatabase, opts *WebOptions) (*Web, error) {
	return &Web{
		db:   db,
		port: opts.Port,
	}, nil
}

func (web *Web) Start() error {
	r := gin.Default()
	r.GET("/ping", func(c *gin.Context) {
		c.String(200, "pong")
	})
	r.GET("/:table", func(c *gin.Context) {
		tableName := c.Param("table")
		rows, err := web.db.Query(c, "SELECT json_agg(t) FROM "+tableName+" as t")
		if err != nil {
			c.JSON(500, gin.H{"error": err.Error()})
			return
		}
		defer rows.Close()

		var result interface{}
		if rows.Next() {
			if err := rows.Scan(&result); err != nil {
				c.JSON(500, gin.H{"error": err.Error()})
				return
			}
			// if empty array, return empty array
			if result == nil {
				result = []interface{}{}
			}
		}

		c.JSON(200, result)
	})
	// 404 handler
	r.NoRoute(func(c *gin.Context) {
		c.JSON(404, gin.H{"error": "not found"})
	})
	return r.Run(":" + strconv.Itoa(web.port))
}
