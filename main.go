package main

import (
        "lbh-node-service/config"
        "lbh-node-service/repository"
        "lbh-node-service/usecase"
        "lbh-node-service/interface/rest"
)

func main() {
        config.InitDB()
        repo := repository.NewFeromonaRepo(config.DB)
        ucase := usecase.NewFeromonaUcase(repo)
        rest.SetupServer(ucase)
}
