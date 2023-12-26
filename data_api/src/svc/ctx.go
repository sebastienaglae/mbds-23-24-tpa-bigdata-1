package svc

type Options struct {
	Sql SqlOptions `mapstructure:"sql"`
}

type Context struct {
	SqlDatabase *SqlDatabase
	Web         *Web
}

func NewContext(opts *Options) (*Context, error) {
	var ctx Context
	var err error
	if ctx.SqlDatabase, err = NewSql(&opts.Sql); err != nil {
		return nil, err
	}
	if ctx.Web, err = NewWeb(ctx.SqlDatabase); err != nil {
		return nil, err
	}
	return &ctx, nil
}

func (ctx *Context) Start() error {
	return ctx.Web.Start()
}

func (ctx *Context) Stop() {
}
