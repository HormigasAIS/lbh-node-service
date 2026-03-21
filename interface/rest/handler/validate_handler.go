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
	"sync"
	"time"

	"github.com/gin-gonic/gin"
)

const (
	secretKey   = "hormigasais-soberano-2026"
	validatorPy = "/data/data/com.termux/files/home/hormigasais-lab/lbh-image-validator/lbh_sello.py"
	maxTTL      = 3600
	minTTL      = 10
	rateLimit   = 10
	rateWindow  = 60
)

var tiposValidos = map[string]bool{
	"SENSOR":   true,
	"DRONE":    true,
	"CONTRACT": true,
	"INTERNAL": true,
	"IMAGE":    true,
	"DEFAULT":  true,
}

type rateLimiter struct {
	mu      sync.Mutex
	counter map[string][]int64
}

var limiter = &rateLimiter{
	counter: make(map[string][]int64),
}

func (r *rateLimiter) allow(nodo string) bool {
	r.mu.Lock()
	defer r.mu.Unlock()
	now := time.Now().Unix()
	window := now - rateWindow
	hits := r.counter[nodo]
	var validos []int64
	for _, t := range hits {
		if t > window {
			validos = append(validos, t)
		}
	}
	r.counter[nodo] = validos
	if len(validos) >= rateLimit {
		return false
	}
	r.counter[nodo] = append(r.counter[nodo], now)
	return true
}

type ValidateRequest struct {
	URL  string `json:"url" binding:"required"`
	Nodo string `json:"nodo"`
	Type string `json:"type"`
	TTL  int    `json:"ttl"`
	Sig  string `json:"sig"`
}

type FeromonaLBH struct {
	Version   string `json:"version"`
	Node      string `json:"node"`
	Action    string `json:"action"`
	Asset     string `json:"asset"`
	Estado    string `json:"estado"`
	Type      string `json:"type"`
	Hash      string `json:"hash"`
	Timestamp int64  `json:"timestamp"`
	TTL       int    `json:"ttl"`
	Sig       string `json:"sig"`
	IssuedBy  string `json:"issued_by"`
}

type ValidateResponse struct {
	Code     int         `json:"code"`
	Version  string      `json:"api_version"`
	Message  string      `json:"message"`
	Feromona FeromonaLBH `json:"feromona"`
}

type ErrorResponse struct {
	Code    int    `json:"code"`
	Version string `json:"api_version"`
	Error   string `json:"error"`
	Detail  string `json:"detail"`
}

func firmarLBH(action, asset, estado, hashImg, tipo string) string {
	ts := strconv.FormatInt(time.Now().Unix(), 10)
	payload := strings.Join([]string{action, asset, estado, hashImg, tipo, ts}, "|")
	mac := hmac.New(sha256.New, []byte(secretKey))
	mac.Write([]byte(payload))
	return fmt.Sprintf("%x", mac.Sum(nil))[:16]
}

func verificarFirmaRequest(req ValidateRequest) bool {
	if req.Sig == "" {
		return true
	}
	payload := strings.Join([]string{req.URL, req.Nodo, req.Type}, "|")
	mac := hmac.New(sha256.New, []byte(secretKey))
	mac.Write([]byte(payload))
	esperada := fmt.Sprintf("%x", mac.Sum(nil))[:16]
	return hmac.Equal([]byte(req.Sig), []byte(esperada))
}

func hashSHA256(data []byte) string {
	h := sha256.Sum256(data)
	return fmt.Sprintf("%x", h)
}

func validarTTL(ttl int) (int, error) {
	if ttl == 0 {
		return 300, nil
	}
	if ttl < minTTL {
		return 0, fmt.Errorf("TTL %d menor al minimo %d", ttl, minTTL)
	}
	if ttl > maxTTL {
		return 0, fmt.Errorf("TTL %d mayor al maximo %d", ttl, maxTTL)
	}
	return ttl, nil
}

func validarOrigen(nodo string) bool {
	bloqueados := []string{"unknown", "anonymous", "test_attack"}
	for _, b := range bloqueados {
		if strings.EqualFold(nodo, b) {
			return false
		}
	}
	return true
}

func descargarImagen(url string) (string, error) {
	resp, err := http.Get(url)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	if resp.StatusCode != 200 {
		return "", fmt.Errorf("HTTP %d", resp.StatusCode)
	}
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

func verificarSello(rutaImg string) (string, string, map[string]interface{}) {
	manifestPath := rutaImg + ".manifest.json"
	data, err := os.ReadFile(rutaImg)
	hashImg := ""
	if err == nil {
		hashImg = hashSHA256(data)[:16] + "..."
	}
	if _, err := os.Stat(validatorPy); err == nil {
		cmd := exec.Command("python3", validatorPy, "verificar", rutaImg)
		cmd.Run()
	}
	if data, err := os.ReadFile(manifestPath); err == nil {
		var manifest map[string]interface{}
		if json.Unmarshal(data, &manifest) == nil {
			return "VALIDADO", hashImg, manifest
		}
	}
	return "FEROMONA_PENDIENTE", hashImg, nil
}

func notificarEspejo(feromona FeromonaLBH) {
	webhook := os.Getenv("SLACK_WEBHOOK")
	if webhook == "" {
		return
	}
	icon := "LBH"
	if feromona.Estado == "VALIDADO" {
		icon = "OK"
	}
	asset := feromona.Asset
	if len(asset) > 40 {
		asset = asset[:40]
	}
	texto := fmt.Sprintf("%s LBH://%s [%s] asset:%s sig:%s",
		icon, feromona.Action, feromona.Type, asset, feromona.Sig)
	body := fmt.Sprintf(`{"text":"%s"}`, texto)
	req, err := http.NewRequest("POST", webhook, strings.NewReader(body))
	if err != nil {
		return
	}
	req.Header.Set("Content-Type", "application/json")
	client := &http.Client{Timeout: 5 * time.Second}
	client.Do(req)
}

func lbhError(c *gin.Context, code int, errMsg, detail string) {
	c.JSON(code, ErrorResponse{
		Code:    code,
		Version: "v1",
		Error:   errMsg,
		Detail:  detail,
	})
}

func keys(m map[string]bool) []string {
	var k []string
	for key := range m {
		k = append(k, key)
	}
	return k
}

type ValidateHandler struct{}

func NewValidateHandler() *ValidateHandler {
	return &ValidateHandler{}
}

func (h *ValidateHandler) Validate(c *gin.Context) {
	var req ValidateRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		lbhError(c, 400, "request_invalido", err.Error())
		return
	}
	if req.Nodo == "" {
		req.Nodo = "hormiga_api"
	}
	if req.Type == "" {
		req.Type = "IMAGE"
	}
	if !tiposValidos[strings.ToUpper(req.Type)] {
		lbhError(c, 400, "tipo_invalido",
			fmt.Sprintf("type debe ser: %v", keys(tiposValidos)))
		return
	}
	req.Type = strings.ToUpper(req.Type)
	if !validarOrigen(req.Nodo) {
		lbhError(c, 403, "origen_bloqueado", "nodo no autorizado")
		return
	}
	if !verificarFirmaRequest(req) {
		lbhError(c, 401, "firma_invalida", "sig no coincide con HMAC-SHA256")
		return
	}
	ttl, err := validarTTL(req.TTL)
	if err != nil {
		lbhError(c, 400, "ttl_invalido", err.Error())
		return
	}
	if !limiter.allow(req.Nodo) {
		lbhError(c, 429, "rate_limit_excedido",
			fmt.Sprintf("maximo %d requests por %ds", rateLimit, rateWindow))
		return
	}
	rutaImg, err := descargarImagen(req.URL)
	if err != nil {
		lbhError(c, 400, "descarga_fallida", err.Error())
		return
	}
	defer os.Remove(rutaImg)
	defer os.Remove(rutaImg + ".manifest.json")
	estado, hashImg, manifest := verificarSello(rutaImg)
	action := "validacion_requerida"
	if estado == "VALIDADO" {
		action = "imagen_validada"
	}
	ts := time.Now().Unix()
	sig := firmarLBH(action, req.URL, estado, hashImg, req.Type)
	feromona := FeromonaLBH{
		Version:   "1.1",
		Node:      req.Nodo,
		Action:    action,
		Asset:     filepath.Base(req.URL),
		Estado:    estado,
		Type:      req.Type,
		Hash:      hashImg,
		Timestamp: ts,
		TTL:       ttl,
		Sig:       sig,
		IssuedBy:  "CLHQ",
	}
	msg := "LBH://" + strings.ToUpper(estado)
	if manifest != nil {
		if prop, ok := manifest["propietario"].(string); ok {
			msg += " | propietario: " + prop
		}
	}
	go notificarEspejo(feromona)
	c.JSON(http.StatusOK, ValidateResponse{
		Code:     200,
		Version:  "v1",
		Message:  msg,
		Feromona: feromona,
	})
}
