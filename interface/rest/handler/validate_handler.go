package handler

import (
"crypto/hmac"
"crypto/sha256"
"encoding/json"
"fmt"
"io"
"net/http"
"os"
"os/exec"
"path/filepath"
"strconv"
"strings"
"time"

"github.com/gin-gonic/gin"
)

const (
secretKey    = "hormigasais-soberano-2026"
validatorPy  = "/data/data/com.termux/files/home/hormigasais-lab/lbh-image-validator/lbh_sello.py"
espejoWebhook = ""
)

// ─────────────────────────────────────────
// DTOs
// ─────────────────────────────────────────

type ValidateRequest struct {
URL  string `json:"url"  binding:"required"`
Nodo string `json:"nodo"`
}

type FeromonaLBH struct {
Version   string `json:"version"`
Node      string `json:"node"`
Action    string `json:"action"`
Asset     string `json:"asset"`
Estado    string `json:"estado"`
Hash      string `json:"hash"`
Timestamp int64  `json:"timestamp"`
TTL       int    `json:"ttl"`
Sig       string `json:"sig"`
IssuedBy  string `json:"issued_by"`
}

type ValidateResponse struct {
Code     int         `json:"code"`
Message  string      `json:"message"`
Feromona FeromonaLBH `json:"feromona"`
}

// ─────────────────────────────────────────
// UTILIDADES LBH
// ─────────────────────────────────────────

func firmarLBH(action, asset, estado, hashImg string) string {
ts := strconv.FormatInt(time.Now().Unix(), 10)
payload := strings.Join([]string{action, asset, estado, hashImg, ts}, "|")
mac := hmac.New(sha256.New, []byte(secretKey))
mac.Write([]byte(payload))
return fmt.Sprintf("%x", mac.Sum(nil))[:16]
}

func hashSHA256(data []byte) string {
h := sha256.Sum256(data)
return fmt.Sprintf("%x", h)
}

// ─────────────────────────────────────────
// DESCARGAR IMAGEN
// ─────────────────────────────────────────

func descargarImagen(url string) (string, error) {
resp, err := http.Get(url)
if err != nil {
return "", err
}
defer resp.Body.Close()

tmp, err := os.CreateTemp("", "lbh_validate_*.png")
if err != nil {
return "", err
}
defer tmp.Close()

if _, err := io.Copy(tmp, resp.Body); err != nil {
return "", err
}
return tmp.Name(), nil
}

// ─────────────────────────────────────────
// VERIFICAR SELLO LBH
// ─────────────────────────────────────────

func verificarSello(rutaImg string) (string, string, map[string]interface{}) {
manifestPath := rutaImg + ".manifest.json"

// Leer imagen para hash
data, err := os.ReadFile(rutaImg)
hashImg := ""
if err == nil {
hashImg = hashSHA256(data)[:16] + "..."
}

// Intentar verificar con lbh_sello.py
if _, err := os.Stat(validatorPy); err == nil {
cmd := exec.Command("python3", validatorPy, "verificar", rutaImg)
cmd.Run()
}

// Verificar manifest
if data, err := os.ReadFile(manifestPath); err == nil {
var manifest map[string]interface{}
if json.Unmarshal(data, &manifest) == nil {
return "VALIDADO", hashImg, manifest
}
}

return "FEROMONA_PENDIENTE", hashImg, nil
}

// ─────────────────────────────────────────
// NOTIFICAR ESPEJO SLACK
// ─────────────────────────────────────────

func notificarEspejo(feromona FeromonaLBH) {
webhook := os.Getenv("SLACK_WEBHOOK")
if webhook == "" {
return
}
icon := "🐜"
if feromona.Estado == "VALIDADO" {
icon = "✅"
}
texto := fmt.Sprintf("%s *LBH://%s* | asset: `%s` | sig: `%s`",
icon, feromona.Action, feromona.Asset[:min(40, len(feromona.Asset))], feromona.Sig)

body := fmt.Sprintf(`{"text":"%s"}`, texto)
req, err := http.NewRequest("POST", webhook, strings.NewReader(body))
if err != nil {
return
}
req.Header.Set("Content-Type", "application/json")
client := &http.Client{Timeout: 5 * time.Second}
client.Do(req)
}

func min(a, b int) int {
if a < b {
return a
}
return b
}

// ─────────────────────────────────────────
// HANDLER
// ─────────────────────────────────────────

type ValidateHandler struct{}

func NewValidateHandler() *ValidateHandler {
return &ValidateHandler{}
}

func (h *ValidateHandler) Validate(c *gin.Context) {
var req ValidateRequest
if err := c.ShouldBindJSON(&req); err != nil {
c.JSON(http.StatusBadRequest, gin.H{
"code":    400,
"message": "url requerida",
})
return
}

nodo := req.Nodo
if nodo == "" {
nodo = "hormiga_api"
}

// Descargar imagen
rutaImg, err := descargarImagen(req.URL)
if err != nil {
c.JSON(http.StatusBadRequest, gin.H{
"code":    400,
"message": "error descargando imagen: " + err.Error(),
})
return
}
defer os.Remove(rutaImg)
defer os.Remove(rutaImg + ".manifest.json")

// Verificar sello
estado, hashImg, manifest := verificarSello(rutaImg)

// Determinar action LBH
action := "validacion_requerida"
if estado == "VALIDADO" {
action = "imagen_validada"
}

// Construir feromona LBH
ts := time.Now().Unix()
sig := firmarLBH(action, req.URL, estado, hashImg)

feromona := FeromonaLBH{
Version:   "1.1",
Node:      nodo,
Action:    action,
Asset:     filepath.Base(req.URL),
Estado:    estado,
Hash:      hashImg,
Timestamp: ts,
TTL:       300,
Sig:       sig,
IssuedBy:  "CLHQ",
}

// Enriquecer con manifest si existe
msg := "LBH://" + strings.ToUpper(estado)
if manifest != nil {
if prop, ok := manifest["propietario"].(string); ok {
msg += " | propietario: " + prop
}
}

// Notificar espejo Slack
go notificarEspejo(feromona)

c.JSON(http.StatusOK, ValidateResponse{
Code:     200,
Message:  msg,
Feromona: feromona,
})
}
