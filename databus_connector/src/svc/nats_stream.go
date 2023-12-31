package svc

import (
	"context"
	"github.com/nats-io/nats.go"
	"github.com/nats-io/nats.go/jetstream"
	"github.com/rs/zerolog/log"
)

type NatsOptions struct {
	URL string `mapstructure:"url"`
}

type NatsStream struct {
	conn *nats.Conn
	js   jetstream.JetStream
}

func NewNatsStream(opts *NatsOptions) (*NatsStream, error) {
	conn, err := nats.Connect(opts.URL)
	if err != nil {
		return nil, err
	}
	js, err := jetstream.New(conn)
	if err != nil {
		return nil, err
	}
	return &NatsStream{
		conn: conn,
		js:   js,
	}, nil
}

func (s *NatsStream) Close() {
	s.conn.Close()
}

func (s *NatsStream) Consume(streamName, consumerName string, h func(msg jetstream.Msg, cb func(err error)) error) (jetstream.ConsumeContext, error) {
	stream, err := s.js.Stream(context.Background(), streamName)
	if err != nil {
		return nil, err
	}
	cons, err := stream.Consumer(context.Background(), consumerName)
	if err != nil {
		return nil, err
	}
	log.Debug().Str("stream", streamName).Str("consumer", consumerName).Msg("start consuming")
	return cons.Consume(func(msg jetstream.Msg) {
		cb := func(err error) {
			if err != nil {
				log.Error().Err(err).Msg("failed to consume message")
				msg.Nak()
			} else {
				msg.Ack()
			}
		}
		if err := h(msg, cb); err != nil {
			cb(err)
		}
	}, jetstream.PullMaxMessages(50000))
}
