# Architecture Documentation

## Overview
This document provides detailed architecture documentation for the Clean/Hexagonal Architecture LLM Chat Application. The architecture is designed to demonstrate SOLID principles and Clean Architecture patterns while keeping the codebase maintainable and testable.

## Architecture Principles

### 1. Clean Architecture Layers

The application follows Clean Architecture principles with clear layer separation:

```
┌─────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Primary Adap-│  │ Secondary    │  │ Database     │     │
│  │ ters (Drive- │  │ Adapters     │  │ Adapters     │     │
│  │  ing)        │  │ (Driven)     │  │              │     │
│  │              │  │              │  │              │     │
│  │ • Chainlit   │  │ • OpenRouter │  │ • SQLite     │     │
│  │   Adapter    │  │ • z.AI       │  │ • User Repo  │     │
│  │ • CLI Adapter│  │ • Ollama     │  │ • Message Repo│    │
│  │              │  │ • AgentaAI   │  │              │     │
│  │              │  │ • Mem0       │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │          Use Cases / Application Services            │   │
│  │                                                      │   │
│  │ • SendMessageUseCase                                │   │
│  │ • LoadHistoryUseCase                                │   │
│  │ • SwitchProviderUseCase                             │   │
│  │ • ManagePromptsUseCase                              │   │
│  │ • ConfigureMemoryUseCase                            │   │
│  │                                                      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                        DOMAIN LAYER                          │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────┐ │
│  │    Entities      │  │    Value Objects │  │  Ports    │ │
│  │                  │  │                  │  │           │ │
│  │ • ChatMessage    │  │ • User           │  │  Repos-   │ │
│  │ • User           │  │ • Provider       │  │  itories  │ │
│  │ • Conversation   │  │ • Prompt         │  │           │ │
│  │ • MessageId      │  │ • MemoryConfig   │  │  (Abst.)  │ │
│  │ • Timestamp      │  │                  │  │           │ │
│  │                  │  │                  │  │  (Ports)  │ │
│  └──────────────────┘  └──────────────────┘  └───────────┘ │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Domain Services                     │   │
│  │              (No side effects)                    │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 2. SOLID Principles

#### Single Responsibility Principle (SRP)
- **Each class has one reason to change**
- Entities: Represent data
- Repositories: Handle data persistence
- Use Cases: Implement business logic
- Adapters: Handle external integrations

#### Open/Closed Principle (OCP)
- **Open for extension, closed for modification**
- Add new providers by implementing `IProvider` interface
- Add new repositories by implementing repository interfaces
- No changes needed to existing code

#### Liskov Substitution Principle (LSP)
- **All implementations can be substituted**
- All provider adapters implement `IProvider` interface
- All repositories implement their respective interfaces

#### Interface Segregation Principle (ISP)
- **Client depends only on interfaces it uses**
- Users only depend on `IUserRepository`
- Messages depend on `IMessageRepository`
- No unnecessary dependencies

#### Dependency Inversion Principle (DIP)
- **Depend on abstractions, not concretions**
- Use cases depend on repository interfaces
- Adapters implement interfaces
- High-level modules don't depend on low-level modules

### 3. Hexagonal Architecture

#### Ports (Interfaces)
Ports define the contract between layers:

**Domain Ports:**
- `IUserRepository` - User data access
- `IMessageRepository` - Message data access
- `IPromptRepository` - Prompt management
- `IMemoryRepository` - Memory management
- `IProvider` - LLM provider abstraction

#### Adapters
Adapters implement ports and interact with external systems:

**Driving Adapters (Internal):**
- `ChainlitAdapter` - Frontend UI
- `CLIAdapter` - Command line interface

**Driven Adapters (External):**
- `OllamaProviderAdapter` - Local Ollama service
- `OpenRouterProviderAdapter` - OpenRouter API
- `ZAIProviderAdapter` - z.AI API
- `AgentaAIPromptAdapter` - Prompt management service
- `Mem0MemoryAdapter` - Memory service

## Detailed Layer Descriptions

### 1. Domain Layer

**Purpose:** Core business logic and data models

**Components:**
- **Entities:** Data models representing business concepts
  - `ChatMessage` - Chat message entity
  - `User` - User entity
  - `Prompt` - Prompt template entity
  - `Memory` - Memory entry entity
  - `MessageRole` - Enum for message roles

- **Value Objects:** Immutable objects with value semantics
  - `User` (with normalized username property)
  - `MemoryConfig` - Memory configuration value object

- **Ports (Interfaces):** Abstractions for external concerns
  - `IUserRepository` - User data access interface
  - `IMessageRepository` - Message data access interface
  - `IPromptRepository` - Prompt management interface
  - `IMemoryRepository` - Memory management interface
  - `IProvider` - LLM provider interface

- **Domain Services:** Business logic without state
  - Message role validation
  - Username normalization
  - Prompt template validation

**Rules:**
- No external dependencies
- No framework-specific code
- Pure Python with typing
- Immutable data structures

### 2. Application Layer

**Purpose:** Orchestrates business logic and use cases

**Components:**
- **Use Cases:** Business logic implementations
  - `SendMessageUseCase` - Send chat message
  - `LoadHistoryUseCase` - Load chat history
  - `SwitchProviderUseCase` - Change LLM provider
  - `ManagePromptsUseCase` - Manage prompt templates
  - `ConfigureMemoryUseCase` - Configure memory settings

- **Application Services:** Business rules coordination
  - Session management
  - User validation
  - Message validation

**Rules:**
- Depends only on domain layer
- No external dependencies
- Use cases are independent
- No direct database access
- No UI code

### 3. Infrastructure Layer

**Purpose:** External system integrations and data persistence

**Components:**
- **Driving Adapters (Internal):**
  - `ChainlitAdapter` - Frontend UI integration
  - `CLIAdapter` - Command line interface

- **Driven Adapters (External):**
  - `OllamaProviderAdapter` - Local Ollama integration
  - `OpenRouterProviderAdapter` - OpenRouter API
  - `ZAIProviderAdapter` - z.AI API
  - `AgentaAIPromptAdapter` - AgentaAI integration
  - `Mem0MemoryAdapter` - Memory service integration
  - `SQLiteUserRepository` - User database
  - `SQLiteMessageRepository` - Message database
  - `SQLitePromptRepository` - Prompt storage (if used)

**Rules:**
- Depends on application and domain layers
- No business logic
- No UI code
- Framework-specific code
- External API implementations

## Dependency Flow

### High-Level Dependencies (Inside-Out)

```
Chainlit Adapter (Infrastructure)
    ↓
Use Cases (Application)
    ↓
Domain Entities & Ports (Domain)
```

### Low-Level Dependencies (Outside-In)

```
External APIs (OpenRouter, Ollama, etc.)
    ↓
Driven Adapters (Infrastructure)
    ↓
Domain Ports (Domain)
```

## Design Patterns Used

### 1. Repository Pattern
- **Purpose:** Abstract data access
- **Implementation:** `IUserRepository`, `IMessageRepository`
- **Benefits:** Decouples data access from business logic

### 2. Adapter Pattern
- **Purpose:** Convert external interfaces to internal ports
- **Implementation:** Provider adapters, database adapters
- **Benefits:** Easy to add new providers/services

### 3. Use Case Pattern
- **Purpose:** Encapsulate business logic
- **Implementation:** `SendMessageUseCase`, etc.
- **Benefits:** Clear business operations, testable

### 4. Dependency Injection
- **Purpose:** Loose coupling between components
- **Implementation:** Pass dependencies in constructors
- **Benefits:** Easy testing, flexible configuration

### 5. Strategy Pattern
- **Purpose:** Different LLM provider strategies
- **Implementation:** `IProvider` interface with multiple implementations
- **Benefits:** Easy to add new providers

## Data Flow

### Message Flow

```
1. User Input (Chainlit UI)
   ↓
2. Chainlit Adapter
   ↓
3. SendMessageUseCase
   ↓
4. Get System Prompt (Prompt Management)
   ↓
5. Generate Response (LLM Provider)
   ↓
6. Stream Response to User
   ↓
7. Save User Message (Message Repository)
   ↓
8. Save Assistant Message (Message Repository)
   ↓
9. Optional: Save to Memory (Memory Management)
```

### User Authentication Flow

```
1. User Enters Username
   ↓
2. Chainlit Adapter
   ↓
3. GetOrCreateUser (User Repository)
   ↓
4. Validate Username (Domain Service)
   ↓
5. Store in Session
   ↓
6. Allow Access
```

## Configuration Management

### Configuration Layers

1. **Environment Variables:** External configuration
2. **Config Modules:** Python configuration objects
3. **Domain Objects:** Configuration as domain entities

### Configuration Flow

```
Environment Variables (.env)
    ↓
Configuration Objects (config/)
    ↓
Domain Objects (domain/models/)
    ↓
Use Cases
```

## Error Handling Strategy

### Error Hierarchy

```
ChatAppError (Base)
    ↓
ProviderError
    ↓
StorageError
    ↓
ConfigurationError
    ↓
AuthenticationError
```

### Error Propagation

1. **Domain Layer:** Throws domain-specific exceptions
2. **Application Layer:** Catches and translates to user-facing errors
3. **Infrastructure Layer:** Catches and logs technical errors
4. **Adapters:** Handles external service errors

## Testing Strategy

### Unit Tests (Domain Layer)
- Test all entities
- Test all value objects
- Test all domain services
- Test all use cases

### Integration Tests (Infrastructure Layer)
- Test all repositories with real database
- Test all adapters with real APIs
- Test use cases with mock dependencies

### End-to-End Tests
- Test complete flows
- Test user authentication
- Test multi-provider switching
- Test error scenarios

## Performance Considerations

### Database
- Use indexes for performance
- Implement pagination
- Use connection pooling
- Consider query optimization

### API Calls
- Use async operations
- Implement request caching
- Use streaming responses
- Rate limit API calls

### Memory Management
- Use connection pooling
- Implement memory limits
- Clean up resources
- Use lazy loading

## Security Considerations

### Input Validation
- Validate all user inputs
- Sanitize outputs
- Prevent SQL injection
- Validate API keys

### Data Storage
- Encrypt sensitive data (if needed)
- Secure credential storage
- No hardcoded secrets
- Proper access control

### API Security
- Validate API endpoints
- Handle API errors
- No exposed credentials
- Rate limiting

## Scalability Considerations

### Database
- Use appropriate indexes
- Implement connection pooling
- Consider read replicas
- Implement caching

### API Calls
- Implement request caching
- Use async operations
- Implement rate limiting
- Use streaming

### Memory
- Implement memory limits
- Use efficient data structures
- Implement cleanup
- Use lazy loading

## Future Enhancements

### Short-term
- Add message search
- Add conversation export
- Add message editing
- Add conversation tagging

### Medium-term
- Add advanced memory features
- Add prompt analytics
- Add conversation grouping
- Add message notifications

### Long-term
- Add multi-language support
- Add advanced analytics
- Add collaborative features
- Add advanced security features

## Architecture Diagrams

### Class Diagram (Simplified)

```
Domain Layer
    ├── Entities: ChatMessage, User, Prompt, Memory
    ├── Value Objects: MemoryConfig
    └── Ports: IUserRepository, IMessageRepository, IPromptRepository, IMemoryRepository, IProvider

Application Layer
    ├── Use Cases: SendMessageUseCase, LoadHistoryUseCase, etc.
    └── Application Services: SessionManager, etc.

Infrastructure Layer
    ├── Driving Adapters: ChainlitAdapter, CLIAdapter
    └── Driven Adapters: SQLiteMessageRepository, OllamaProviderAdapter, etc.
```

### Sequence Diagram (Message Flow)

```
User → ChainlitAdapter → SendMessageUseCase → Provider → Stream Response → ChainlitAdapter → User
                ↓                                      ↓
        UserRepository                            MessageRepository
        (Get User)                                 (Save Message)
                ↓                                      ↓
        ChainlitAdapter ← User ← ← ← ← ← ← ← ← ← ← ← ChainlitAdapter
```

## Conclusion

This architecture demonstrates Clean/Hexagonal Architecture principles with SOLID principles throughout. The clear separation of concerns makes the codebase maintainable, testable, and extensible while providing a solid foundation for the LLM Chat Application.
