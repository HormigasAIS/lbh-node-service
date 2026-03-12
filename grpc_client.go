package main

import (
        "context"
        "fmt"
        "log"

        genproto "lbh-node-service/interface/grpc/proto"
        "google.golang.org/grpc"
        "google.golang.org/grpc/credentials/insecure"
)

func main() {
        conn, err := grpc.NewClient("localhost:7100", grpc.WithTransportCredentials(insecure.NewCredentials()))
        if err != nil {
                log.Fatalf("Error conectando: %v", err)
        }
        defer conn.Close()

        client := genproto.NewFeromonaServiceClient(conn)
        res, err := client.EmitirFeromona(context.Background(), &genproto.FeromonaLBH{
                Nodo:    "A16-Soberano-Salvador",
                Payload: "ESTADO:OPERATIVO|GRPC",
                Firma:   "hmac-lbh-grpc-v1",
        })
        if err != nil {
                log.Fatalf("Error emitiendo: %v", err)
        }
        fmt.Printf("feromona gRPC: code=%d message=%s nodo=%s\n", res.Code, res.Message, res.Nodo)
}
