package handler

import (
        "context"
        "time"

        genproto "lbh-node-service/interface/grpc/proto"
        "lbh-node-service/usecase"
)

type FeromonaGrpcHandler struct {
        genproto.UnimplementedFeromonaServiceServer
        Ucase *usecase.FeromonaUcase
}

func NewFeromonaGrpcHandler(u *usecase.FeromonaUcase) *FeromonaGrpcHandler {
        return &FeromonaGrpcHandler{Ucase: u}
}

func (h *FeromonaGrpcHandler) EmitirFeromona(ctx context.Context, req *genproto.FeromonaLBH) (*genproto.FeromonaRespuesta, error) {
        f, err := h.Ucase.Emitir(req.Nodo, req.Payload, req.Firma)
        if err != nil {
                return &genproto.FeromonaRespuesta{Code: 500, Message: err.Error()}, err
        }
        return &genproto.FeromonaRespuesta{
                Code:    200,
                Message: "feromona_aceptada",
                Nodo:    f.Nodo,
                Payload: f.Payload,
                Ts:      f.TS,
        }, nil
}

func (h *FeromonaGrpcHandler) ListarFeromonas(req *genproto.Vacio, stream genproto.FeromonaService_ListarFeromonasServer) error {
        feromonas, err := h.Ucase.Listar()
        if err != nil {
                return err
        }
        for _, f := range feromonas {
                stream.Send(&genproto.FeromonaRespuesta{
                        Code:    200,
                        Message: "ok",
                        Nodo:    f.Nodo,
                        Payload: f.Payload,
                        Ts:      f.TS,
                })
                time.Sleep(10 * time.Millisecond)
        }
        return nil
}
