package usecase

import (
        "lbh-node-service/domain/model"
        "lbh-node-service/repository"
        "time"
)

type FeromonaUcase struct {
        Repo *repository.FeromonaRepo
}

func NewFeromonaUcase(repo *repository.FeromonaRepo) *FeromonaUcase {
        return &FeromonaUcase{Repo: repo}
}

func (u *FeromonaUcase) Emitir(nodo, payload, firma string) (*model.Feromona, error) {
        f := &model.Feromona{
                Nodo:    nodo,
                Payload: payload,
                Firma:   firma,
                TS:      time.Now().Unix(),
        }
        err := u.Repo.Guardar(f)
        return f, err
}

func (u *FeromonaUcase) Listar() ([]model.Feromona, error) {
        return u.Repo.Listar()
}
