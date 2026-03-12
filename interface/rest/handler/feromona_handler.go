package handler

import (
        "lbh-node-service/domain/dto"
        "lbh-node-service/usecase"
        "net/http"

        "github.com/gin-gonic/gin"
)

type FeromonaHandler struct {
        Ucase *usecase.FeromonaUcase
}

func NewFeromonaHandler(u *usecase.FeromonaUcase) *FeromonaHandler {
        return &FeromonaHandler{Ucase: u}
}

func (h *FeromonaHandler) Emitir(c *gin.Context) {
        var req dto.FeromonaRequest
        if err := c.ShouldBindJSON(&req); err != nil {
                c.JSON(http.StatusBadRequest, dto.FeromonaResponse{
                        Code:    400,
                        Message: err.Error(),
                })
                return
        }
        f, err := h.Ucase.Emitir(req.Nodo, req.Payload, req.Firma)
        if err != nil {
                c.JSON(http.StatusInternalServerError, dto.FeromonaResponse{
                        Code:    500,
                        Message: err.Error(),
                })
                return
        }
        c.JSON(http.StatusOK, dto.FeromonaResponse{
                Code:    200,
                Message: "feromona_aceptada",
                Data:    f,
        })
}

func (h *FeromonaHandler) Listar(c *gin.Context) {
        feromonas, err := h.Ucase.Listar()
        if err != nil {
                c.JSON(http.StatusInternalServerError, dto.FeromonaResponse{
                        Code:    500,
                        Message: err.Error(),
                })
                return
        }
        c.JSON(http.StatusOK, dto.FeromonaResponse{
                Code:    200,
                Message: "ok",
                Data:    feromonas,
        })
}
