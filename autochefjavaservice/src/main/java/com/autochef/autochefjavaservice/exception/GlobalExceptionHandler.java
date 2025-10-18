package com.autochef.autochefjavaservice.exception;

import com.autochef.autochefjavaservice.dto.ErrorResponse;
import com.autochef.autochefjavaservice.constants.ErrorCode;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {

    /**
     * Handles validation errors (400 Bad Request)
     */
    @ExceptionHandler(ValidationException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(ValidationException ex) {
        ErrorResponse errorResponse = new ErrorResponse(
                HttpStatus.BAD_REQUEST.value(),        // 400
                ex.getErrorCode().getCode(),           // "INVALID_PROMPT"  
                ex.getMessage()                        // "Prompt is required and cannot be blank."
        );
        return ResponseEntity.badRequest().body(errorResponse);
    }

    /**
     * Handles malformed JSON requests (400 Bad Request)
     */
    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ResponseEntity<ErrorResponse> handleJsonParseError(HttpMessageNotReadableException ex) {
        ErrorResponse errorResponse = new ErrorResponse(
                HttpStatus.BAD_REQUEST.value(),        // 400
                ErrorCode.BAD_REQUEST.getCode(),       // "BAD_REQUEST"
                ErrorCode.BAD_REQUEST.getMessage()     // "Malformed request or invalid JSON."
        );
        return ResponseEntity.badRequest().body(errorResponse);
    }

    /**
     * Handles downstream service exceptions (502/504)
     */
    @ExceptionHandler(DownstreamServiceException.class)
    public ResponseEntity<ErrorResponse> handleDownstreamServiceException(DownstreamServiceException ex) {
        HttpStatus status = ex.getErrorCode() == ErrorCode.LLM_TIMEOUT ? 
                HttpStatus.GATEWAY_TIMEOUT : HttpStatus.BAD_GATEWAY;
        
        ErrorResponse errorResponse = new ErrorResponse(
                status.value(),                        // 502 or 504
                ex.getErrorCode().getCode(),           // "LLM_DOWN" or "LLM_TIMEOUT"
                ex.getMessage()                        // Message from ErrorCode
        );
        return ResponseEntity.status(status).body(errorResponse);
    }

    /**
     * Handles all other unexpected exceptions (500 Internal Server Error)
     */
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGenericException(Exception ex) {
        ErrorResponse errorResponse = new ErrorResponse(
                HttpStatus.INTERNAL_SERVER_ERROR.value(), // 500
                ErrorCode.INTERNAL_ERROR.getCode(),        // "INTERNAL_ERROR"
                ErrorCode.INTERNAL_ERROR.getMessage()      // "An unexpected error occurred."
        );
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
    }
}
