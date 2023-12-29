package svc

import (
	"github.com/gin-contrib/cors"
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
	r.Use(cors.Default())
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
	r.GET("/api/:table", func(c *gin.Context) {
		tableName := c.Param("table")

		defaultQuery := "SELECT * FROM " + tableName

		filter := c.DefaultQuery("where", "")
		sort := c.DefaultQuery("sortby", "")
		order := c.DefaultQuery("orderby", "asc")
		limit := c.DefaultQuery("limit", "100")
		having := c.DefaultQuery("having", "")

		query := addFilter(defaultQuery, filter)
		query = addSort(query, sort, order)
		query = addLimit(query, limit)
		query = addHaving(query, having)

		rows, err := web.db.Query(c, "SELECT json_agg(t) FROM ("+query+") as t")
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
			if result == nil {
				result = []interface{}{}
			}
		}

		c.JSON(200, result)
	})

	return r.Run(":" + strconv.Itoa(web.port))
}

func addFilter(query, filter string) string {
	if filter != "" {
		query += " WHERE " + filter
	}

	return query
}

func addSort(query, sort, order string) string {
	if sort != "" {
		query += " ORDER BY " + sort + " " + order
	}

	return query
}

func addLimit(query, limit string) string {
	if limit != "" {
		query += " LIMIT " + limit
	}

	return query
}

func addHaving(query, having string) string {
	if having != "" {
		query += " HAVING " + having
	}

	return query
}
