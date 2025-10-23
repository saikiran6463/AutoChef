# ================================
# STAGE 1: BUILD
# ================================
# Use full JDK with build tools for compilation
FROM eclipse-temurin:17-jdk AS builder

# Set working directory for build
WORKDIR /build

# Copy Maven wrapper and pom.xml first (for layer caching)
# If pom.xml doesn't change, Maven won't re-download dependencies
COPY mvnw .
COPY mvnw.cmd .
COPY .mvn .mvn
COPY pom.xml .

# Download dependencies (this layer will be cached)
RUN ./mvnw dependency:go-offline -B

# Copy source code
COPY src src

# Build the application (creates JAR in target/)
RUN ./mvnw clean package -DskipTests -B

# ================================
# STAGE 2: RUNTIME
# ================================
# Use smaller JRE-only image for runtime
FROM eclipse-temurin:17-jre

# Set working directory
WORKDIR /app

# Copy only the JAR file from builder stage
COPY --from=builder /build/target/*.jar app.jar

# Expose port 8080 (Spring Boot default)
EXPOSE 8080

# Run the application with optimized JVM settings for containers
CMD ["java", "-jar", "app.jar"]