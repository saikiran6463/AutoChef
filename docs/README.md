# AutoChef Documentation

This directory contains comprehensive documentation for the AutoChef project.

## Documents

### [API_DESIGN.md](./API_DESIGN.md)
Complete API specification for the AutoChef Java Spring Boot gateway service, including:
- Endpoint specifications
- Request/response schemas
- Error handling patterns
- Future enhancements roadmap

### [AWS_BEDROCK_INTEGRATION.md](./AWS_BEDROCK_INTEGRATION.md)
Technical implementation guide for AWS Bedrock Claude 3 Haiku integration, covering:
- Phase 1: AWS foundation and connectivity setup
- Phase 2: Production implementation with microservices architecture
- System architecture and data flow
- Production quality examples and performance characteristics

## Architecture Overview

```
Client → Java Spring Boot (Gateway) → Python FastAPI (LLM) → AWS Bedrock Claude
```

The documentation provides both API consumer guidance and technical implementation details for developers.