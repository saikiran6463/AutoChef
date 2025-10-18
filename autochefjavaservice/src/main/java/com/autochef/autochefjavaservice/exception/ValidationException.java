package com.autochef.autochefjavaservice.exception;

import com.autochef.autochefjavaservice.constants.ErrorCode;

/**
 * Exception thrown when request validation fails.
 * This allows us to handle validation errors with specific error codes.
 */
public class ValidationException extends RuntimeException {
    
    private final ErrorCode errorCode;
    
    public ValidationException(ErrorCode errorCode) {
        super(errorCode.getMessage());
        this.errorCode = errorCode;
    }
    
    public ValidationException(ErrorCode errorCode, String customMessage) {
        super(customMessage);
        this.errorCode = errorCode;
    }
    
    public ErrorCode getErrorCode() {
        return errorCode;
    }
}