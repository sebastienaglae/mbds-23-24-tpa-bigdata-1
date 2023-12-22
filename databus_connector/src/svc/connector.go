package svc

import (
	"context"
	"encoding/json"
	"errors"
	"github.com/nats-io/nats.go/jetstream"
	"strings"
)

type ConnectorOptions struct {
	Event struct {
		Stream   string            `mapstructure:"stream"`
		Consumer map[string]string `mapstructure:"consumer"`
	} `mapstructure:"event"`
	Database string `mapstructure:"database"`
}

type Connector struct {
	nats *NatsStream
	db   *SqlDatabase

	stream   string
	consumer map[string]string
	database string

	consumeContexts []jetstream.ConsumeContext
}

func NewConnectorService(ctx *Context, opts *ConnectorOptions) (*Connector, error) {
	return &Connector{
		nats: ctx.NatsStream,
		db:   ctx.SqlDatabase,

		stream:   opts.Event.Stream,
		consumer: opts.Event.Consumer,
		database: opts.Database,
	}, nil
}

func (s *Connector) Start() error {
	for handlerType, cons := range s.consumer {
		handler := s.GetHandler(handlerType)
		if handler == nil {
			return errors.New("invalid consumer type: " + handlerType)
		}
		if ctx, err := s.nats.Consume(s.stream, cons, handler); err != nil {
			return err
		} else {
			s.consumeContexts = append(s.consumeContexts, ctx)
		}
	}
	return nil
}

func (s *Connector) Stop() {
	for _, ctx := range s.consumeContexts {
		ctx.Stop()
	}
}

func (s *Connector) GetHandler(handlerType string) func(msg jetstream.Msg) error {
	switch handlerType {
	case "new":
		return s.onNew
	case "update":
		return s.onUpdate
	case "delete":
		return s.onDelete
	default:
		return nil
	}
}

func (s *Connector) onNew(msg jetstream.Msg) error {
	tableName, dataKey, dataValue, err := parseMessageData(msg)
	if err != nil {
		return err
	}
	sb := strings.Builder{}
	sb.WriteString("INSERT INTO `")
	sb.WriteString(tableName)
	sb.WriteString("` (")
	for _, k := range dataKey {
		sb.WriteString("`")
		sb.WriteString(k)
		sb.WriteString("`,")
	}
	sb.WriteString(") VALUES (")
	for i := 0; i < len(dataValue); i++ {
		if i > 0 {
			sb.WriteByte(',')
		}
		sb.WriteString("?")
	}
	sb.WriteByte(')')

	_, err = s.db.Exec(context.Background(), sb.String(), dataValue...)
	if err != nil {
		return err
	}
	return nil
}

func (s *Connector) onUpdate(msg jetstream.Msg) error {
	tableName, dataKey, dataValue, err := parseMessageData(msg)
	if err != nil {
		return err
	}
	rowId := msg.Headers().Get("rowId")
	if rowId == "" {
		return errors.New("rowId not found")
	}
	sb := strings.Builder{}
	sb.WriteString("UPDATE `")
	sb.WriteString(tableName)
	sb.WriteString("` SET ")
	for i, k := range dataKey {
		if i > 0 {
			sb.WriteByte(',')
		}
		sb.WriteString("`")
		sb.WriteString(k)
		sb.WriteString("`=?")
	}
	sb.WriteString(" WHERE `id`=?")

	dataValue = append(dataValue, rowId)
	_, err = s.db.Exec(context.Background(), sb.String(), dataValue)
	if err != nil {
		return err
	}
	return nil
}

func (s *Connector) onDelete(msg jetstream.Msg) error {
	tableName, _, _, err := parseMessageData(msg)
	if err != nil {
		return err
	}
	rowId := msg.Headers().Get("rowId")
	if rowId == "" {
		return errors.New("rowId not found")
	}
	sb := strings.Builder{}
	sb.WriteString("DELETE FROM `")
	sb.WriteString(tableName)
	sb.WriteString("` WHERE `id`=?")

	_, err = s.db.Exec(context.Background(), sb.String(), rowId)
	if err != nil {
		return err
	}
	return nil
}

func parseMessageData(msg jetstream.Msg) (string, []string, []interface{}, error) {
	var data map[string]interface{}
	if err := json.Unmarshal(msg.Data(), &data); err != nil {
		return "", nil, nil, err
	}
	var dataKeys []string
	var dataValues []interface{}
	for k, v := range data {
		dataKeys = append(dataKeys, k)
		dataValues = append(dataValues, v)
	}
	tableName := msg.Headers().Get("table")
	if tableName == "" {
		return "", nil, nil, errors.New("table name not found")
	}
	return tableName, dataKeys, dataValues, nil
}
