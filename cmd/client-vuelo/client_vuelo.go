package main

import (
"context"
"fmt"
"log"
"time"

genproto "lbh-node-service/interface/grpc/proto"
"google.golang.org/grpc"
"google.golang.org/grpc/credentials/insecure"
)

func main() {
conn, err := grpc.Dial("localhost:7100", grpc.WithTransportCredentials(insecure.NewCredentials()))
if err != nil {
log.Fatalf("❌ Error de conexión: %v", err)
}
defer conn.Close()

client := genproto.NewFeromonaServiceClient(conn)

// Ajustado a la estructura real: Nodo, Payload, Firma, Ts
req := &genproto.FeromonaLBH{
Nodo:    "NODO-A16-MASTER",
Payload: "Hallazgo de recurso energético - Sector A20",
Firma:   "CLHQ-VALID-2026-XOXO",
Ts:      time.Now().Unix(),
}

ctx, cancel := context.WithTimeout(context.Background(), time.Second)
defer cancel()

fmt.Println("📡 Enviando feromona binaria (LBH) al puerto 7100...")
res, err := client.EmitirFeromona(ctx, req)
if err != nil {
log.Fatalf("❌ Error LBH: %v", err)
}

fmt.Printf("✅ Respuesta recibida del Nodo: %+v\n", res)
}
