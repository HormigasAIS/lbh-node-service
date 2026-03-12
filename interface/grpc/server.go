package grpc

import (
        "fmt"
        "net"

        grpc_handler "lbh-node-service/interface/grpc/handler"
        genproto "lbh-node-service/interface/grpc/proto"
        "lbh-node-service/usecase"

        "google.golang.org/grpc"
)

func SetupServer(ucase *usecase.FeromonaUcase) {
        lis, err := net.Listen("tcp", ":7100")
        if err != nil {
                panic("Error al iniciar gRPC: " + err.Error())
        }

        s := grpc.NewServer()
        h := grpc_handler.NewFeromonaGrpcHandler(ucase)
        genproto.RegisterFeromonaServiceServer(s, h)

        fmt.Println("🐜 LBH gRPC escuchando en :7100")
        if err := s.Serve(lis); err != nil {
                panic("Error en gRPC serve: " + err.Error())
        }
}
