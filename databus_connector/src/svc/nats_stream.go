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

func (s *NatsStream) InitStream(streamConfig jetstream.StreamConfig, consumerConfigs []jetstream.ConsumerConfig) error {
	if _, err := s.js.CreateStream(context.Background(), streamConfig); err != nil {
		log.Error().Err(err).Msg("failed to create stream")
		return err
	}
	for _, consumerConfig := range consumerConfigs {
		if _, err := s.js.CreateConsumer(context.Background(), streamConfig.Name, consumerConfig); err != nil {
			log.Error().Err(err).Msg("failed to create consumer")
			return err
		}
	}
	return nil
}

func (s *NatsStream) Consume(streamName, consumerName string, cb func(msg jetstream.Msg) error) (jetstream.ConsumeContext, error) {
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
		if err := cb(msg); err != nil {
			log.Error().Err(err).Msg("failed to consume message")
			msg.Nak()
			return
		} else {
			msg.Ack()
		}
	})
}
