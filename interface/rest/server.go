package rest

import (
        "lbh-node-service/interface/rest/handler"
        "lbh-node-service/usecase"

        "github.com/gin-gonic/gin"
)

func SetupServer(ucase *usecase.FeromonaUcase) {
        h := handler.NewFeromonaHandler(ucase)
        r := gin.Default()

        r.GET("/ping", func(c *gin.Context) {
                c.JSON(200, gin.H{"code": 200, "message": "pong LBH"})
        })

        r.POST("/feromona", h.Emitir)
        r.GET("/feromonas", h.Listar)

        r.Run(":8100")
}
