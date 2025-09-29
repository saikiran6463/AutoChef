package com.autochef.autochefjavaservice.exception;

import com.autochef.autochefjavaservice.dto.ErrorResponse;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.reactive.function.client.WebClientRequestException;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(WebClientRequestException.class)
    @ResponseStatus(HttpStatus.BAD_GATEWAY)
    public ErrorResponse handleDownstreamServiceError(WebClientRequestException ex) {
        // Log the exception for debugging purposes (optional but recommended)
        // log.error("Downstream service connection error: {}", ex.getMessage());

        return new ErrorResponse(
                "DOWNSTREAM_SERVICE_UNAVAILABLE",
                "The recipe generation service is currently unavailable. Please try again later."
        );
    }
}
