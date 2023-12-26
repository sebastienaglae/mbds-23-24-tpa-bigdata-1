package svc

import (
	"context"
	"github.com/jackc/pgx/v5/pgxpool"
)

type SqlOptions struct {
	ConnectionString string `mapstructure:"connectionString"`
}

type SqlDatabase struct {
	*pgxpool.Pool
}

func NewSql(opts *SqlOptions) (*SqlDatabase, error) {
	conn, err := pgxpool.New(context.Background(), opts.ConnectionString)
	if err != nil {
		return nil, err
	}
	return &SqlDatabase{conn}, nil
}
