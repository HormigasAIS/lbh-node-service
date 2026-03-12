package main

import (
    "context"
    "database/sql"
    "fmt"
    "log"
    "net"

    pb "lbh-node-service/interface/grpc/proto"
    _ "github.com/mattn/go-sqlite3"
    "google.golang.org/grpc"
)

type server struct {
    pb.UnimplementedFeromonaServiceServer
    db *sql.DB
}

func (s *server) EmitirFeromona(ctx context.Context, in *pb.FeromonaLBH) (*pb.RespuestaLBH, error) {
    fmt.Printf("🐜 Feromona recibida de %s: %s\n", in.Nodo, in.Payload)
    
    // HOOK: Guardar en DB
    _, err := s.db.Exec("INSERT INTO auditoria (nodo, payload, timestamp) VALUES (?, ?, datetime('now'))", in.Nodo, in.Payload)
    if err != nil {
        log.Printf("Error persistiendo feromona: %v", err)
    }

    return &pb.RespuestaLBH{Code: 200, Message: "feromona_aceptada", Nodo: in.Nodo}, nil
}

func main() {
    db, err := sql.Open("sqlite3", "./lbh_nodo.db")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    lis, err := net.Listen("tcp", ":7100")
    if err != nil {
        log.Fatalf("Fallo al escuchar: %v", err)
    }
    
    s := grpc.NewServer()
    pb.RegisterFeromonaServiceServer(s, &server{db: db})
    
    fmt.Println("🚀 Servidor gRPC de HormigasAIS activo con persistencia en puerto 7100")
    if err := s.Serve(lis); err != nil {
        log.Fatalf("Fallo al servir: %v", err)
    }
}
