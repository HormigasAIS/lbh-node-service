package model

type Feromona struct {
        ID      uint   `json:"id" gorm:"primaryKey"`
        Nodo    string `json:"nodo"`
        Payload string `json:"payload"`
        Firma   string `json:"firma"`
        TS      int64  `json:"ts"`
}
