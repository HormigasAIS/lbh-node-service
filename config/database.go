package config

import (
        "lbh-node-service/domain/model"
        "gorm.io/driver/sqlite"
        "gorm.io/gorm"
)

var DB *gorm.DB

func InitDB() {
        db, err := gorm.Open(sqlite.Open("lbh_nodo.db"), &gorm.Config{})
        if err != nil {
                panic("Error al conectar SQLite: " + err.Error())
        }
        db.AutoMigrate(&model.Feromona{})
        DB = db
}
