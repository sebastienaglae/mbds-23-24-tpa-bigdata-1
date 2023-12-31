package svc

import (
	"fmt"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"strconv"
	"strings"
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
	r.Use(cors.Default())
	r.GET("/ping", func(c *gin.Context) {
		c.String(200, "pong")
	})
	r.GET("/metrics", func(c *gin.Context) {
		sb := strings.Builder{}
		for name, table := range web.tableQueries {
			rows, err := web.db.Query(c, "SELECT COUNT(*) FROM ("+table+") as t")
			if err != nil {
				c.JSON(500, gin.H{"error": err.Error()})
				return
			}
			defer rows.Close()

			var count int
			if rows.Next() {
				if err = rows.Scan(&count); err != nil {
					c.JSON(500, gin.H{"error": err.Error()})
					return
				}
			}
			rows.Close()

			sb.WriteString(fmt.Sprintf("# HELP table_%s_count The number of rows in table %s\n", name, name))
			sb.WriteString(fmt.Sprintf("table_%s_count %d\n", name, count))
		}
		c.String(200, sb.String())
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
			if err = rows.Scan(&result); err != nil {
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
	// 404 handler
	r.NoRoute(func(c *gin.Context) {
		c.JSON(404, gin.H{"error": "not found"})
	})
	r.GET("/api/:table", func(c *gin.Context) {
		tableName := c.Param("table")

		defaultQuery, ok := web.tableQueries[tableName]
		if !ok {
			c.JSON(404, gin.H{"error": "table not found"})
			return
		}

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
			if err = rows.Scan(&result); err != nil {
				c.JSON(500, gin.H{"error": err.Error()})
				return
			}
			if result == nil {
				result = []interface{}{}
			}
		}

		c.JSON(200, result)
	})
	r.POST("/query", func(c *gin.Context) {
		var json struct {
			Query string `json:"query"`
		}

		if err := c.BindJSON(&json); err != nil {
			c.JSON(500, gin.H{"error": err.Error()})
			return
		}

		rows, err := web.db.Query(c, "SELECT json_agg(t) FROM ("+json.Query+") as t")
		if err != nil {
			c.JSON(500, gin.H{"error": err.Error()})
			return
		}
		defer rows.Close()

		var result interface{}
		if rows.Next() {
			if err = rows.Scan(&result); err != nil {
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
