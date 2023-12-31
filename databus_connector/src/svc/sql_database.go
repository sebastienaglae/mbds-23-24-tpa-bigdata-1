package svc

import (
	"context"
	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/pkg/errors"
	"github.com/rs/zerolog/log"
	"sync"
	"time"
)

type SqlOptions struct {
	ConnectionString string `mapstructure:"connectionString"`
}

type queuedSql struct {
	query string
	args  []interface{}
	f     func(err error)
}

type SqlDatabase struct {
	*pgxpool.Pool

	running bool
	mu      sync.Mutex
	queued  []queuedSql
}

func NewSql(opts *SqlOptions) (*SqlDatabase, error) {
	conn, err := pgxpool.New(context.Background(), opts.ConnectionString)
	if err != nil {
		return nil, err
	}
	return &SqlDatabase{conn, false, sync.Mutex{}, make([]queuedSql, 0)}, nil
}

func (s *SqlDatabase) Start() error {
	if s.running {
		return errors.New("sql database already running")
	}
	s.running = true
	go func() {
		tmp := make([]queuedSql, 0)
		for {
			if !s.running {
				return
			}
			s.mu.Lock()
			if len(s.queued) == 0 {
				s.mu.Unlock()
				time.Sleep(1 * time.Millisecond)
				continue
			}
			reqs := s.queued
			s.queued = tmp
			s.mu.Unlock()

			start := time.Now()
			batch := &pgx.Batch{}
			for _, req := range reqs {
				batch.Queue(req.query, req.args...)
			}

			br := s.Pool.SendBatch(context.Background(), batch)
			for i := 0; i < len(reqs); i++ {
				_, err := br.Exec()
				reqs[i].f(err)
			}
			_ = br.Close()

			log.Debug().Int("num", len(reqs)).Dur("dur", time.Since(start)).Msg("sql batch")

			tmp = reqs[:0]
		}
	}()
	return nil
}

func (s *SqlDatabase) Close() {
	s.Pool.Close()
}

func (s *SqlDatabase) Queue(query string, args []interface{}, f func(err error)) {
	// block if too many requests are queued
	for {
		s.mu.Lock()
		numQueued := len(s.queued)
		if numQueued < 50000 {
			s.queued = append(s.queued, queuedSql{query, args, f})
			s.mu.Unlock()
			return
		}
		s.mu.Unlock()
		log.Warn().Msg("sql database queue full")
		time.Sleep(100 * time.Millisecond)
	}
}
