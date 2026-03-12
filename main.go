package main

import (
        "lbh-node-service/config"
        "lbh-node-service/interface/grpc"
        "lbh-node-service/interface/rest"
        "lbh-node-service/repository"
        "lbh-node-service/usecase"
        "os"
)

func main() {
        config.InitDB()
        repo := repository.NewFeromonaRepo(config.DB)
        ucase := usecase.NewFeromonaUcase(repo)

        args := os.Args
        if len(args) > 1 && args[1] == "--server=grpc" {
                grpc.SetupServer(ucase)
        } else {
                rest.SetupServer(ucase)
        }
}
