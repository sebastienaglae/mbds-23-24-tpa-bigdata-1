package svc

import (
	"encoding/json"
	"errors"
	"fmt"
	"github.com/nats-io/nats.go/jetstream"
	"strconv"
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

func (s *Connector) GetHandler(handlerType string) func(msg jetstream.Msg, cb func(err error)) error {
	switch handlerType {
	case "new":
		return s.onNew
	case "update":
		return s.onUpdate
	case "upsert":
		return s.onUpsert
	case "delete":
		return s.onDelete
	default:
		return nil
	}
}

func (s *Connector) onNew(msg jetstream.Msg, cb func(err error)) error {
	return errors.New("not implemented")
}

func (s *Connector) onUpdate(msg jetstream.Msg, cb func(err error)) error {
	return errors.New("not implemented")
}

func (s *Connector) onUpsert(msg jetstream.Msg, cb func(err error)) error {
	tableName, tablePks, attrs, err := parseMessageData(msg)
	if err != nil {
		return err
	}

	args := make([]interface{}, 0)
	reqStr := prepareInsertRequest(tableName, tablePks, attrs, true, "", &args)

	// log.Debug().Str("table", tableName).Str("pk", strings.Join(tablePks, ",")).Str("query", reqStr).Msg("upsert")
	s.db.Queue(reqStr, args, cb)
	return nil
}

func (s *Connector) onDelete(msg jetstream.Msg, cb func(err error)) error {
	return errors.New("not implemented")
}

func prepareInsertRequest(tableName string, tablePks []string, attrs map[string]interface{}, upsert bool, returnPk string, args *[]interface{}) string {
	subRequests := make([]string, 0)
	columns := make([]string, 0)
	values := make([]string, 0)
	updates := make([]string, 0)

	for k, v := range attrs {
		columns = append(columns, k)
		// if value is not a map, then it's a primitive type
		if valueInterface, ok := v.(map[string]interface{}); !ok {
			*args = append(*args, v)
			values = append(values, "$"+strconv.Itoa(len(*args)))
			updates = append(updates, k+"=$"+strconv.Itoa(len(*args)))
		} else {
			fromTable := valueInterface["from"].(string)
			fromTablePks := strings.Split(valueInterface["pk"].(string), ",")
			fromTableRef := valueInterface["ref"].(string)
			fromTableAttributes := valueInterface["match"].(map[string]interface{})
			allowUpdate := valueInterface["allowUpdate"].(bool)

			subRequests = append(subRequests, prepareInsertRequest(fromTable, fromTablePks, fromTableAttributes, allowUpdate, fromTableRef, args))
			if len(subRequests) > 1 {
				panic("multiple sub requests not supported")
			}
			values = append(values, fromTableRef)
		}
	}

	var reqStr string
	if len(subRequests) > 0 {
		reqStr = "WITH ins AS (" + subRequests[0] + ") INSERT INTO %s (%s) SELECT %s FROM ins"
	} else {
		reqStr = "INSERT INTO %s (%s) VALUES (%s)"
	}

	reqStr = fmt.Sprintf(reqStr,
		tableName,
		strings.Join(columns, ","),
		strings.Join(values, ","))

	if upsert {
		reqStr += " ON CONFLICT (%s) DO UPDATE SET %s"
		reqStr = fmt.Sprintf(reqStr,
			strings.Join(tablePks, ","),
			strings.Join(updates, ","))

		if returnPk != "" {
			reqStr += " RETURNING " + returnPk
		}
	} else if returnPk != "" {
		dummyUpdates := make([]string, len(tablePks))
		for i := range dummyUpdates {
			dummyUpdates[i] = tablePks[i] + "=excluded." + tablePks[i]
		}
		reqStr += " ON CONFLICT (%s) DO UPDATE SET %s RETURNING %s"
		reqStr = fmt.Sprintf(reqStr,
			strings.Join(tablePks, ","),
			strings.Join(dummyUpdates, ","))
	} else {
		reqStr += " ON CONFLICT (%s) DO NOTHING"
		reqStr = fmt.Sprintf(reqStr,
			strings.Join(tablePks, ","))
	}

	return reqStr
}

func parseMessageData(msg jetstream.Msg) (string, []string, map[string]interface{}, error) {
	var data map[string]interface{}
	if err := json.Unmarshal(msg.Data(), &data); err != nil {
		return "", nil, nil, err
	}
	tableName := msg.Headers().Get("table")
	if tableName == "" {
		return "", nil, nil, errors.New("table name not found")
	}
	tablePk := msg.Headers().Get("tablePk")
	if tablePk == "" {
		return "", nil, nil, errors.New("table primary key not found")
	}
	return tableName, strings.Split(tablePk, ","), data, nil
}
