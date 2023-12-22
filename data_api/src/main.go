package main

import (
	"databus_connector/src/svc"
	"flag"
	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
	"github.com/rs/zerolog/pkgerrors"
	"github.com/spf13/viper"
	"os"
	"os/signal"
	"strings"
	"syscall"
)

var configFile = flag.String("c", "config.yaml", "the config file")

func main() {
	flag.Parse()

	zerolog.ErrorStackMarshaler = pkgerrors.MarshalStack
	log.Logger = log.Output(zerolog.ConsoleWriter{Out: os.Stderr}).With().Logger()

	viper.SetConfigFile(*configFile)
	viper.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))
	viper.AutomaticEnv()
	viper.SetEnvPrefix("CONFIG")

	var c svc.Options
	if err := viper.ReadInConfig(); err != nil {
		log.Fatal().Err(err).Msg("failed to read config file")
	}
	if err := viper.Unmarshal(&c); err != nil {
		log.Fatal().Err(err).Msg("failed to unmarshal config")
	}

	log.Info().Msg("Initializing connector")

	svcCtx, err := svc.NewContext(&c)
	if err != nil {
		log.Fatal().Err(err).Msg("failed to initialize connector")
	}
	if err = svcCtx.Start(); err != nil {
		log.Fatal().Err(err).Msg("failed to start connector")
	}

	log.Info().Msg("Connector started")

	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)
	<-sigs

	log.Info().Msg("Stopping connector")

	svcCtx.Stop()

	log.Info().Msg("Connector stopped")
}
