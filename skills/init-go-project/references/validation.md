# Request Validation Reference

> **NOTE:** Code examples below use `Widget`/`CreateWidgetRequest`/`WidgetResponse`
> as placeholders. Replace with the actual domain entity from the project
> description (e.g., `Task`/`CreateTaskRequest`/`TaskResponse`). Adapt
> fields and validation rules to match the real entity's attributes.

Defines the request payload validation pattern using
`github.com/go-playground/validator/v10`.

## Why a separate DTO type?

Domain types in `pkg/domain/` are framework-free — they don't carry
`validate:` struct tags. Validation tags live on **request DTOs** in the
HTTP adapter. The handler:

1. Decodes JSON into the DTO
2. Validates the DTO via the shared validator instance
3. Maps the validated DTO to a domain value
4. Calls the service

This keeps validation rules close to the wire format and prevents the
domain from depending on a validation library.

## Files

### `internal/adapters/http/dto.go`

```go
package http

import (
    "time"

    "{{module}}/pkg/domain"
)

// CreateWidgetRequest is the JSON body for POST /api/v1/widgets.
type CreateWidgetRequest struct {
    Name        string `json:"name"        validate:"required,min=1,max=200"`
    Description string `json:"description" validate:"max=2000"`
}

func (r CreateWidgetRequest) ToDomain() domain.Widget {
    return domain.Widget{
        Name:        r.Name,
        Description: r.Description,
    }
}

// WidgetResponse is the JSON body returned for widget endpoints.
type WidgetResponse struct {
    ID          string    `json:"id"`
    Name        string    `json:"name"`
    Description string    `json:"description,omitempty"`
    CreatedAt   time.Time `json:"created_at"`
}

func widgetToResponse(w domain.Widget) WidgetResponse {
    return WidgetResponse{
        ID:          w.ID,
        Name:        w.Name,
        Description: w.Description,
        CreatedAt:   w.CreatedAt,
    }
}

// ErrorResponse is the standard error body.
type ErrorResponse struct {
    Error   string             `json:"error"`
    Message string             `json:"message,omitempty"`
    Fields  []FieldErrorDetail `json:"fields,omitempty"`
}

type FieldErrorDetail struct {
    Field   string `json:"field"`
    Rule    string `json:"rule"`
    Message string `json:"message"`
}
```

### `internal/adapters/http/decode.go`

```go
package http

import (
    "encoding/json"
    "errors"
    "fmt"
    "io"
    "net/http"

    "github.com/go-playground/validator/v10"
)

// validate is the shared, thread-safe validator instance. Use a single
// instance for the lifetime of the process — the validator caches reflection
// data per type internally.
var validate = validator.New(validator.WithRequiredStructEnabled())

// MaxBodyBytes is the default request body size limit. Override at
// the route level via http.MaxBytesHandler if a specific endpoint needs more.
const MaxBodyBytes = 1 << 20 // 1MB

// decodeAndValidate decodes the JSON request body into dst and runs
// struct validation against any `validate:"..."` tags. Returns:
//   - *DecodeError on JSON parse failure (HTTP 400)
//   - *ValidationError on validation rule violation (HTTP 400 with field details)
//   - *BodyTooLargeError if the body exceeds MaxBodyBytes (HTTP 413)
//
// The dst argument must be a non-nil pointer to a struct.
func decodeAndValidate(r *http.Request, dst any) error {
    r.Body = http.MaxBytesReader(nil, r.Body, MaxBodyBytes)
    dec := json.NewDecoder(r.Body)
    dec.DisallowUnknownFields()
    if err := dec.Decode(dst); err != nil {
        var maxErr *http.MaxBytesError
        if errors.As(err, &maxErr) {
            return &BodyTooLargeError{Limit: maxErr.Limit}
        }
        var syntaxErr *json.SyntaxError
        var unmarshalErr *json.UnmarshalTypeError
        switch {
        case errors.As(err, &syntaxErr):
            return &DecodeError{Reason: fmt.Sprintf("malformed JSON at byte %d", syntaxErr.Offset)}
        case errors.As(err, &unmarshalErr):
            return &DecodeError{Reason: fmt.Sprintf("field %q: expected %s", unmarshalErr.Field, unmarshalErr.Type)}
        case errors.Is(err, io.EOF):
            return &DecodeError{Reason: "request body required"}
        default:
            return &DecodeError{Reason: err.Error()}
        }
    }
    // Reject trailing data — JSON body should be a single object
    if dec.More() {
        return &DecodeError{Reason: "unexpected data after JSON object"}
    }
    if err := validate.Struct(dst); err != nil {
        return validationErrorFrom(err)
    }
    return nil
}

// --- error types ---

type DecodeError struct {
    Reason string
}
func (e *DecodeError) Error() string { return "decode: " + e.Reason }

type BodyTooLargeError struct {
    Limit int64
}
func (e *BodyTooLargeError) Error() string {
    return fmt.Sprintf("body exceeds %d bytes", e.Limit)
}

type ValidationError struct {
    Fields []FieldErrorDetail
}
func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed: %d field(s)", len(e.Fields))
}

func validationErrorFrom(err error) *ValidationError {
    ve := &ValidationError{}
    var fieldErrs validator.ValidationErrors
    if !errors.As(err, &fieldErrs) {
        ve.Fields = []FieldErrorDetail{{Field: "_", Rule: "_", Message: err.Error()}}
        return ve
    }
    for _, fe := range fieldErrs {
        ve.Fields = append(ve.Fields, FieldErrorDetail{
            Field:   fe.Field(),
            Rule:    fe.Tag(),
            Message: humanRuleMessage(fe),
        })
    }
    return ve
}

func humanRuleMessage(fe validator.FieldError) string {
    switch fe.Tag() {
    case "required": return fmt.Sprintf("%s is required", fe.Field())
    case "email":    return "must be a valid email"
    case "min":      return fmt.Sprintf("must be at least %s", fe.Param())
    case "max":      return fmt.Sprintf("must be at most %s", fe.Param())
    case "uuid":     return "must be a valid UUID"
    case "url":      return "must be a valid URL"
    case "oneof":    return fmt.Sprintf("must be one of: %s", fe.Param())
    default:         return fmt.Sprintf("failed rule %q", fe.Tag())
    }
}
```

### `internal/adapters/http/respond.go`

```go
package http

import (
    "encoding/json"
    "errors"
    "log/slog"
    "net/http"

    "{{module}}/pkg/domain"
)

func respondJSON(w http.ResponseWriter, status int, body any) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(status)
    if body != nil {
        if err := json.NewEncoder(w).Encode(body); err != nil {
            slog.Error("respond encode failed", slog.String("err", err.Error()))
        }
    }
}

func respondError(w http.ResponseWriter, r *http.Request, err error) {
    var dec *DecodeError
    var val *ValidationError
    var tooBig *BodyTooLargeError
    switch {
    case errors.As(err, &val):
        respondJSON(w, http.StatusBadRequest, ErrorResponse{
            Error:   "validation_failed",
            Message: val.Error(),
            Fields:  val.Fields,
        })
    case errors.As(err, &dec):
        respondJSON(w, http.StatusBadRequest, ErrorResponse{
            Error:   "bad_request",
            Message: dec.Error(),
        })
    case errors.As(err, &tooBig):
        respondJSON(w, http.StatusRequestEntityTooLarge, ErrorResponse{
            Error:   "body_too_large",
            Message: tooBig.Error(),
        })
    case errors.Is(err, domain.ErrNotFound):
        respondJSON(w, http.StatusNotFound, ErrorResponse{Error: "not_found"})
    case errors.Is(err, domain.ErrAlreadyExists):
        respondJSON(w, http.StatusConflict, ErrorResponse{Error: "already_exists"})
    default:
        slog.ErrorContext(r.Context(), "internal error",
            slog.String("path", r.URL.Path),
            slog.String("err", err.Error()))
        respondJSON(w, http.StatusInternalServerError, ErrorResponse{
            Error: "internal_error",
        })
    }
}
```

## Handler usage

```go
func (h *Handlers) CreateWidget(w http.ResponseWriter, r *http.Request) {
    var req CreateWidgetRequest
    if err := decodeAndValidate(r, &req); err != nil {
        respondError(w, r, err)
        return
    }
    widget, err := h.svc.Create(r.Context(), req.ToDomain())
    if err != nil {
        respondError(w, r, err)
        return
    }
    respondJSON(w, http.StatusCreated, widgetToResponse(widget))
}
```

## Validation tag cookbook

Common patterns to drop on DTO fields:

| Tag | Effect |
|-----|--------|
| `validate:"required"` | Field must be present and non-zero |
| `validate:"required,min=1,max=200"` | Required string with length bounds |
| `validate:"email"` | Valid RFC 5322 email |
| `validate:"uuid"` | Valid UUID v1-v5 |
| `validate:"url"` | Valid URL |
| `validate:"oneof=draft published archived"` | Enum |
| `validate:"gte=0,lte=100"` | Numeric range |
| `validate:"dive,required"` | Apply rules to slice/map elements |
| `validate:"omitempty,email"` | Skip if zero, validate if present |
| `validate:"required_if=Type premium"` | Conditional |

For custom rules (e.g., "must be a valid TN format"), register on the
shared validator:

```go
validate.RegisterValidation("tn_format", func(fl validator.FieldLevel) bool {
    return tnRegex.MatchString(fl.Field().String())
})
```

## Test pattern

```go
func TestDecodeAndValidate(t *testing.T) {
    cases := []struct {
        name      string
        body      string
        wantErr   bool
        wantFields []string
    }{
        {"valid", `{"name":"foo","description":"bar"}`, false, nil},
        {"missing name", `{"description":"bar"}`, true, []string{"Name"}},
        {"name too long", `{"name":"`+strings.Repeat("a", 201)+`"}`, true, []string{"Name"}},
        {"unknown field", `{"name":"foo","wat":1}`, true, nil},
        {"empty body", ``, true, nil},
    }
    for _, tc := range cases {
        t.Run(tc.name, func(t *testing.T) {
            var got CreateWidgetRequest
            req := httptest.NewRequest("POST", "/", strings.NewReader(tc.body))
            err := decodeAndValidate(req, &got)
            if tc.wantErr {
                require.Error(t, err)
                if len(tc.wantFields) > 0 {
                    var ve *ValidationError
                    require.ErrorAs(t, err, &ve)
                    fields := make([]string, len(ve.Fields))
                    for i, f := range ve.Fields { fields[i] = f.Field }
                    require.ElementsMatch(t, tc.wantFields, fields)
                }
            } else {
                require.NoError(t, err)
            }
        })
    }
}
```
