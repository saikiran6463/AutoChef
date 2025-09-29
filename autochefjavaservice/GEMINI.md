# GEMINI.MD: AI Collaboration Guide

This document provides essential context for AI models interacting with this project. Adhering to these guidelines will ensure consistency and maintain code quality.

## 1. Project Overview & Purpose

* **Primary Goal:** This project, "AutoChef," is a GenAI-powered recipe generation service. It functions as a Java-based API gateway that receives user prompts (e.g., ingredients) and communicates with a downstream Python LLM service to generate structured recipe data.
* **Business Domain:** Food Tech, Generative AI.
* **Current Status:** The Java API gateway is functionally complete. It has been implemented to call the downstream Python service using `WebClient` and includes robust error handling via a `@RestControllerAdvice` that correctly returns a `502 Bad Gateway` status when the downstream service is unavailable.

## 2. Core Technologies & Stack

* **Languages:** Java 17
* **Frameworks & Runtimes:** Spring Boot 3.5.5
* **Databases:** None are currently configured. The design document mentions DynamoDB as a future possibility for caching and recipe persistence.
* **Key Libraries/Dependencies:**
    * `spring-boot-starter-web`: For building RESTful APIs.
    * `spring-boot-starter-webflux`: Used for making non-blocking HTTP requests via `WebClient` to downstream services.
    * `spring-boot-starter-actuator`: Provides production-ready features like health checks.
    * `spring-boot-starter-validation`: Used for request payload validation.
    * `springdoc-openapi-starter-webmvc-ui`: For generating and serving OpenAPI (Swagger) documentation.
    * `lombok`: To reduce boilerplate code (e.g., getters, setters, constructors).
* **Package Manager(s):** Maven. The project uses the Maven Wrapper (`mvnw`), so no global installation is required.

## 3. Architectural Patterns

* **Overall Architecture:** The application follows a **Microservices Architecture** pattern, acting as a **Gateway** service. It is designed to be a lightweight Java service that handles client-facing API requests and delegates the core logic (recipe generation) to a separate Python service. Internally, it uses a standard **Model-View-Controller (MVC)** pattern for its REST endpoints.
* **Directory Structure Philosophy:** The project follows the standard Maven directory layout.
    * `/src/main/java`: Contains all primary Java source code.
        * `/controller`: Holds REST API controllers.
        * `/dto`: Contains Data Transfer Objects for API request/response models.
    * `/src/main/resources`: Contains non-Java files.
        * `/static`: For static assets like the `openapi.yaml` specification.
        * `application.properties`: For application configuration.
    * `/src/test/java`: Contains all unit and integration tests.
    * `/docs`: Contains high-level design documentation.

## 4. Coding Conventions & Style Guide

* **Formatting:** Standard Java style with 4-space indentation.
* **Naming Conventions:**
    * `classes`, `records`: PascalCase (`RecipeController`, `RecipeRequest`)
    * `methods`, `variables`: camelCase (`generateRecipe`, `dummyIngredients`)
    * `files`: PascalCase for Java source files (`RecipeController.java`).
* **API Design:** The project follows **RESTful principles** as defined in `openapi.yaml` and `docs/API_DESIGN.md`.
    * **Endpoints:** Versioned (`/api/v1`) and resource-oriented (`/generate-recipe`).
    * **Data Format:** JSON is used for all request and response bodies.
    * **Contracts:** DTOs define strict data contracts for requests (`RecipeRequest`), responses (`RecipeResponse`), and errors (`ErrorResponse`).
* **Error Handling:** A standardized error handling approach is defined.
    * Custom `ErrorResponse` DTO (`{ "code": "...", "message": "..." }`) is used for client-facing errors.
    * Specific HTTP status codes are used to indicate the nature of the error (e.g., 400 for bad requests, 502 for downstream service failures).

## 5. Key Files & Entrypoints

* **Main Entrypoint(s):** `src/main/java/com/autochef/autochefjavaservice/AutochefjavaserviceApplication.java` contains the `main` method that starts the Spring Boot application.
* **Configuration:**
    * `pom.xml`: Defines all project dependencies, plugins, and build settings.
    * `src/main/resources/application.properties`: Manages application-level settings, such as the location of the OpenAPI specification.
* **API Specification:** `src/main/resources/static/openapi.yaml` provides the formal OpenAPI 3.0 contract for the entire API.

## 6. Development & Testing Workflow

* **Local Development Environment:** To run the application locally, either execute the `main` method in `AutochefjavaserviceApplication.java` from an IDE or run `./mvnw spring-boot:run` from the command line. The service will be available at `http://localhost:8080`.
* **Testing:** The project is configured for testing with JUnit and the Spring Test framework. Run all tests using the command: `./mvnw test`. New features should be accompanied by corresponding tests in the `/src/test/java` directory.
* **CI/CD Process:** No CI/CD pipeline configuration (e.g., `.github/workflows`) was detected in the project.

## 7. Specific Instructions for AI Collaboration

* **Contribution Guidelines:** No `CONTRIBUTING.md` file was found. Assume standard practices: create feature branches, write clean code, and ensure tests pass before proposing changes.
* **Infrastructure (IaC):** No Infrastructure as Code (e.g., Terraform, CloudFormation) was detected.
* **Security:** Be mindful of security best practices. The current MVP has no authentication. Do not add hardcoded secrets or keys. Future security enhancements (API Keys, OAuth2) will be managed via an API Gateway, as noted in the design documents.
* **Dependencies:** To add a new dependency, add the required `<dependency>` block to the `pom.xml` file. Ensure it is a trusted and necessary library. Run `./mvnw dependency:analyze` to check for unused dependencies.
* **Commit Messages:** The git history was not analyzed. It is recommended to follow the **Conventional Commits** specification (e.g., `feat:`, `fix:`, `docs:`, `refactor:`) for all commit messages to maintain a clean and understandable history.

## 8. Next Steps

The next major phase of the project is to implement the downstream Python LLM service.

*   **Technology:** The service should be a web server built with a modern Python framework like **FastAPI** or **Flask**.
*   **Endpoint:** It must listen on `http://localhost:5001` and expose the following endpoint:
    *   `POST /api/v1/generate-recipe`
*   **Contract:** The service must strictly adhere to the JSON contract defined by the Java DTOs:
    *   It must **accept** a JSON body matching the `RecipeRequest` structure.
    *   It must **return** a JSON body matching the `RecipeResponse` structure.
