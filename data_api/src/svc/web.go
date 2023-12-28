package svc

import (
	"github.com/gin-gonic/gin"
	"strconv"
)

type WebOptions struct {
	Port         int               `mapstructure:"port"`
	TableQueries map[string]string `mapstructure:"tables"`
}

type Web struct {
	db           *SqlDatabase
	port         int
	tableQueries map[string]string
}

func NewWeb(db *SqlDatabase, opts *WebOptions) (*Web, error) {
	return &Web{
		db:           db,
		port:         opts.Port,
		tableQueries: opts.TableQueries,
	}, nil
}

func (web *Web) Start() error {
	r := gin.Default()
	r.GET("/ping", func(c *gin.Context) {
		c.String(200, "pong")
	})
	r.GET("/:table", func(c *gin.Context) {
		tableName := c.Param("table")
		query, ok := web.tableQueries[tableName]
		if !ok {
			c.JSON(404, gin.H{"error": "table not found"})
			return
		}

		pageString := c.DefaultQuery("page", "0")
		pageSizeString := c.DefaultQuery("size", "100")
		page, _ := strconv.Atoi(pageString)
		if page < 1 {
			page = 1
		}
		pageSize, _ := strconv.Atoi(pageSizeString)
		if pageSize < 1 {
			pageSize = 100
		}
		args := make([]interface{}, 0)
		args = append(args, pageSize+1, (page-1)*pageSize)

		rows, err := web.db.Query(c, "SELECT json_agg(t) FROM ("+query+" LIMIT $1 OFFSET $2) as t", args...)
		if err != nil {
			c.JSON(500, gin.H{"error": err.Error()})
			return
		}
		defer rows.Close()

		var result interface{}
		var hasMore bool
		if rows.Next() {
			if err := rows.Scan(&result); err != nil {
				c.JSON(500, gin.H{"error": err.Error()})
				return
			}
			// if empty array, return empty array
			if result == nil {
				result = []interface{}{}
			} else {
				arr := result.([]interface{})
				if len(arr) > pageSize {
					result = arr[:pageSize]
					hasMore = true
				}
			}
		}

		c.JSON(200, gin.H{"result": result, "hasMore": hasMore, "page": page, "pageSize": pageSize})
	})
	return r.Run(":" + strconv.Itoa(web.port))
}
