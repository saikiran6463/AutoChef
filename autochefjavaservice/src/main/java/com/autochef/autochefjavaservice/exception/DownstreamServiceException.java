package com.autochef.autochefjavaservice.exception;

import com.autochef.autochefjavaservice.constants.ErrorCode;

/**
 * Exception thrown when downstream service calls fail.
 * This allows us to handle different types of downstream failures with specific error codes.
 */
public class DownstreamServiceException extends RuntimeException {
    
    private final ErrorCode errorCode;
    
    public DownstreamServiceException(ErrorCode errorCode) {
        super(errorCode.getMessage());
        this.errorCode = errorCode;
    }
    
    public DownstreamServiceException(ErrorCode errorCode, String customMessage) {
        super(customMessage);
        this.errorCode = errorCode;
    }
    
    public DownstreamServiceException(ErrorCode errorCode, Throwable cause) {
        super(errorCode.getMessage(), cause);
        this.errorCode = errorCode;
    }
    
    public ErrorCode getErrorCode() {
        return errorCode;
    }
}