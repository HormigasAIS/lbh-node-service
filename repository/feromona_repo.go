package repository

import (
        "lbh-node-service/domain/model"
        "gorm.io/gorm"
)

type FeromonaRepo struct {
        DB *gorm.DB
}

func NewFeromonaRepo(db *gorm.DB) *FeromonaRepo {
        return &FeromonaRepo{DB: db}
}

func (r *FeromonaRepo) Guardar(f *model.Feromona) error {
        return r.DB.Create(f).Error
}

func (r *FeromonaRepo) Listar() ([]model.Feromona, error) {
        var feromonas []model.Feromona
        err := r.DB.Find(&feromonas).Error
        return feromonas, err
}
