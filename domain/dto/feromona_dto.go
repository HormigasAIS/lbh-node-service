package dto

type FeromonaRequest struct {
        Nodo    string `json:"nodo" binding:"required"`
        Payload string `json:"payload" binding:"required"`
        Firma   string `json:"firma" binding:"required"`
}

type FeromonaResponse struct {
        Code    int         `json:"code"`
        Message string      `json:"message"`
        Data    interface{} `json:"data"`
}
