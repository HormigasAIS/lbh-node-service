package main

import (
    "bufio"
    "bytes"
    "crypto/hmac"
    "crypto/sha256"
    "encoding/hex"
    "fmt"
    "net"
    "net/http"
    "strings"
)

const CLAVE_COLONIA = "HORMIGA_SECRET_KEY_2026" 

func validarFirma(mensaje, firmaHex string) bool {
    h := hmac.New(sha256.New, []byte(CLAVE_COLONIA))
    h.Write([]byte(mensaje))
    expectedFirma := hex.EncodeToString(h.Sum(nil))
    return hmac.Equal([]byte(expectedFirma), []byte(strings.TrimPrefix(firmaHex, "SIG:")))
}

func handleCentinela(conn net.Conn) {
    defer conn.Close()
    scanner := bufio.NewScanner(conn)
    for scanner.Scan() {
        raw := scanner.Text()
        parts := strings.Split(raw, "|")
        if len(parts) == 3 {
            mensaje := parts[0] + "|" + parts[1]
            if validarFirma(mensaje, parts[2]) {
                fmt.Printf("🛡️ Firma validada para %s\n", parts[0])
                jsonPayload := fmt.Sprintf(`{"nodo":"CENTINELA_V24","payload":"%s","firma":"%s"}`, parts[0], parts[2])
                resp, err := http.Post("http://localhost:8100/feromona", "application/json", bytes.NewBuffer([]byte(jsonPayload)))
                if err == nil {
                    resp.Body.Close()
                    fmt.Printf("✅ Feromona retransmitida: %s\n", parts[0])
                }
            } else {
                fmt.Println("❌ ALERTA: Firma inválida detectada.")
            }
        }
    }
}

func main() {
    ln, err := net.Listen("tcp", ":9001")
    if err != nil {
        panic(err)
    }
    fmt.Println("📡 Bridge Centinela (Seguridad HMAC) activo en :9001...")
    for {
        conn, err := ln.Accept()
        if err != nil { continue }
        go handleCentinela(conn)
    }
}
