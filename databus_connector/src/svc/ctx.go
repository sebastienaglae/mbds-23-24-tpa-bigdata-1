package svc

type Options struct {
	Sql       SqlOptions       `mapstructure:"sql"`
	Nats      NatsOptions      `mapstructure:"nats"`
	Connector ConnectorOptions `mapstructure:"connector"`
}

type Context struct {
	NatsStream  *NatsStream
	SqlDatabase *SqlDatabase
	Connector   *Connector
}

func NewContext(opts *Options) (*Context, error) {
	var ctx Context
	var err error
	if ctx.NatsStream, err = NewNatsStream(&opts.Nats); err != nil {
		return nil, err
	}
	if ctx.SqlDatabase, err = NewSql(&opts.Sql); err != nil {
		return nil, err
	}
	if ctx.Connector, err = NewConnectorService(&ctx, &opts.Connector); err != nil {
		return nil, err
	}
	return &ctx, nil
}

func (ctx *Context) Start() error {
	if err := ctx.Connector.Start(); err != nil {
		return err
	}
	return nil
}

func (ctx *Context) Stop() {
	ctx.NatsStream.Close()
}
