# Product Requirements Document: LLM Chat Application

## 1. Executive Summary

### Problem Statement
There is a need for an educational project to deeply understand and practice Clean/Hexagonal Architecture and SOLID principles through hands-on implementation of a multi-provider LLM chat application.

### Proposed Solution
Build a multi-provider LLM chat application with Chainlit frontend and LangChain backend, structured using Clean/Hexagonal architecture patterns with simple username authentication, AgentaAI prompt management, and chat history persistence. The project will serve as a reference implementation for learning Clean Architecture principles.

### Success Criteria
- Successfully implement multi-provider support (OpenRouter, z.AI, Ollama) with unified interface
- Codebase follows Clean/Hexagonal architecture patterns with clear separation of concerns
- Chainlit frontend integrated cleanly with hexagonal backend
- Simple username-based authentication functional
- AgentaAI prompt management integrated
- Chat history persisted per username
- All code follows Python 3.12 standards with full typing
- Clean codebase demonstrating SOLID principles throughout

---

## 2. User Experience & Functionality

### User Personas
- **Primary Persona**: Developer/Student learning Clean/Hexagonal Architecture and SOLID principles
- **Secondary Persona**: User testing chat functionality with different LLM providers

### User Stories

#### US1: Chat with Multiple LLM Providers

**As a user, I want to switch between different LLM providers (OpenRouter, z.AI, Ollama) so that I can test different models and capabilities.**

**Acceptance Criteria**:
- [ ] Users can select provider from dropdown in Chainlit UI
- [ ] Provider selection persists during session
- [ ] Each provider uses LangChain abstraction layer
- [ ] API keys for each provider configurable via environment variables
- [ ] Error handling for provider failures does not break other providers
- [ ] Provider switching does not lose chat context
- [ ] All providers use consistent response format

#### US2: Simple Username Authentication

**As a user, I want to identify myself with a username so that my chat history is preserved separately from others.**

**Acceptance Criteria**:
- [ ] Username input appears on app load
- [ ] No password required (simple identity only)
- [ ] Username persists in session
- [ ] Chat history filtered by username
- [ ] Duplicate username handling (simple conflict resolution)
- [ ] Username case-insensitive handling

#### US3: Chat History Management

**As a user, I want to see my previous conversations so that I can reference past discussions.**

**Acceptance Criteria**:
- [ ] Chat history stored per username
- [ ] History viewable in Chainlit UI
- [ ] Can continue previous conversations
- [ ] History persists across sessions
- [ ] Simple SQLite storage for learning purposes
- [ ] Chat history can be cleared (optional feature)

#### US4: Prompt Management with AgentaAI

**As a user, I want to manage prompts through AgentaAI so that I can version and track prompt templates.**

**Acceptance Criteria**:
- [ ] Integration with AgentaAI API
- [ ] Can pull prompts from AgentaAI
- [ ] System prompts configurable via AgentaAI
- [ ] Fallback to local prompts if AgentaAI unavailable
- [ ] Prompt templates loaded at application startup
- [ ] Prompt versioning available (optional)

#### US5: Optional Memory Integration (Nice to Have)

**As a user, I want the AI to remember context from our conversation so that I don't have to repeat information.**

**Acceptance Criteria**:
- [ ] Integration with self-hosted Mem0
- [ ] Memory tied to username
- [ ] Configurable memory limits
- [ ] Context window management
- [ ] Memory retrieval integrated into chat flow

### Non-Goals

**Explicitly OUT of scope for this project**:
- Production deployment or scaling
- Advanced authentication (OAuth, JWT, SSO)
- Complex UI customization beyond Chainlit defaults
- Multi-tenancy beyond username separation
- Admin dashboards or analytics
- Payment processing or subscription management
- Real-time collaboration features
- Message encryption or security auditing
- API for external application integration
- Database migration tooling
- CI/CD pipeline automation
- Docker containerization (unless requested)

---

## 3. AI System Requirements

### Tool Requirements

#### Core Dependencies (pyproject.toml)
- `langchain>=1.2.8` - LLM orchestration framework
- `chainlit>=2.9.6` - Frontend UI framework
- `agenta` - Prompt management service (to be specified)

#### LLM Provider APIs
- **OpenRouter**: `https://openrouter.ai/api/v1`
  - Required for: GPT-4, Claude, and other models via OpenRouter
  - Configuration: `OPENROUTER_API_KEY`

- **z.AI**: API endpoint (to be specified)
  - Required for: z.AI specific models
  - Configuration: `ZAI_API_KEY`

- **Ollama**: `http://localhost:11434` (default, self-hosted)
  - Required for: Local LLM execution (llama3, mistral, etc.)
  - Configuration: `OLLAMA_BASE_URL`

#### Optional Services
- **AgentaAI**: Prompt management service (to be specified)
  - Required for: Prompt versioning and management
  - Configuration: `AGENTA_API_KEY`, `AGENTA_BASE_URL`

- **Mem0**: Self-hosted memory service
  - Required for: Persistent conversation memory
  - Configuration: `MEM0_BASE_URL`

#### Storage
- `sqlite3` - Chat history persistence
- Environment variables for API keys and configuration
- `typing` for complete type coverage

### Evaluation Strategy

#### Manual Testing Criteria
- [ ] All three providers respond correctly with same query
- [ ] Provider switching maintains chat context
- [ ] Username authentication filters chat history correctly
- [ ] AgentaAI integration works (with fallback)
- [ ] Mem0 integration works (if enabled)
- [ ] Chat history persists across sessions
- [ ] Error handling doesn't break other providers

#### Code Quality Metrics
- [ ] 100% type coverage on all functions
- [ ] `uv run ruff check` passes with no errors
- [ ] `uv run black` formatting consistent
- [ ] Clear separation between domain, application, and infrastructure layers
- [ ] No dependencies violate domain layer (dependencies on outer layers only)
- [ ] All functions have Google-style docstrings
- [ ] Classes follow SOLID principles

---

## 4. Technical Specifications

### Architecture Overview

#### Layered Architecture Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Primary Adap-│  │ Secondary    │  │ Database     │     │
│  │ ters (Drive- │  │ Adapters     │  │ Adapters     │     │
│  │  ing)        │  │ (Driven)     │  │              │     │
│  │              │  │              │  │              │     │
│  │ • Chainlit   │  │ • OpenRouter │  │ • SQLite     │     │
│  │   Adapter    │  │ • z.AI       │  │ • ChatHistory│     │
│  │ • CLI Adapter│  │ • Ollama     │  │   Adapter    │     │
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

### Integration Points

#### External API Integrations

**OpenRouter API**:
```
Endpoint: https://openrouter.ai/api/v1/chat/completions
Method: POST
Headers: Authorization: Bearer {OPENROUTER_API_KEY}
Body: {
  "model": "openai/gpt-4",
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."}
  ],
  "stream": true
}
```

**z.AI API**:
```
Endpoint: {ZAI_BASE_URL}/v1/chat/completions
Method: POST
Headers: Authorization: Bearer {ZAI_API_KEY}
Body: Similar structure to OpenRouter
```

**Ollama API**:
```
Endpoint: http://localhost:11434/api/chat
Method: POST
Body: {
  "model": "llama3",
  "messages": [{"role": "user", "content": "..."}],
  "stream": true
}
```

**AgentaAI API**:
```
Endpoint: {AGENTA_BASE_URL}/api/prompts
Method: GET
Headers: Authorization: Bearer {AGENTA_API_KEY}
Response: {
  "prompts": [
    {
      "id": "prompt-1",
      "name": "system_prompt",
      "content": "You are a helpful assistant...",
      "version": "1.0"
    }
  ]
}
```

**Mem0 API**:
```
Endpoint: http://localhost:8080/memory/add
Method: POST
Headers: Authorization: Bearer {MEM0_API_KEY}
Body: {
  "user_id": "username",
  "memory": "User likes Python 3.12"
}
```

#### Environment Variables

```bash
# Provider API Keys
OPENROUTER_API_KEY=sk-or-v1-...
ZAI_API_KEY=zai_api_key_here
OLLAMA_BASE_URL=http://localhost:11434

# Prompt Management
AGENTA_API_KEY=agenta_api_key_here
AGENTA_BASE_URL=https://api.agenta.ai

# Optional Memory
MEM0_BASE_URL=http://localhost:8080
MEM0_API_KEY=mem0_key_here

# Storage
DATABASE_PATH=./chat_history.db
```

### Database Schema (SQLite)

```sql
-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chat messages table
CREATE TABLE chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    provider TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id, timestamp, role, content)
);

-- Indexes for performance
CREATE INDEX idx_chat_messages_user_id ON chat_messages(user_id);
CREATE INDEX idx_chat_messages_timestamp ON chat_messages(timestamp);
```

### Security & Privacy

#### Data Handling
- [ ] API keys stored in environment variables only
- [ ] No secrets committed to repository
- [ ] No hardcoded API keys in source code
- [ ] Chat history stored locally (SQLite)
- [ ] No telemetry or analytics sent externally

#### Authentication
- [ ] Username-only identification (no password)
- [ ] Username sanitized to prevent SQL injection
- [ ] No PII collection beyond username
- [ ] Session tokens used for state management

#### Compliance
- [ ] User data stays local
- [ ] No data shared with third parties beyond LLM providers
- [ ] Clear data deletion option (delete SQLite file)
- [ ] No external data collection
- [ ] Opt-in memory feature (disabled by default)

#### Code Security
- [ ] All external API calls use proper error handling
- [ ] Input validation on all user inputs
- [ ] No code execution from untrusted sources
- [ ] No unsafe deserialization
- [ ] No file inclusion vulnerabilities
- [ ] Secure credential storage practices

---

## 5. Risks & Roadmap

### Phase 0: Foundation (Current State)
**Status**: In Progress
**Completed**:
- [x] Initial project setup
- [x] Dependencies added to pyproject.toml
- [x] Basic Chainlit echo handler created

**Next Actions**:
- [ ] Define project structure
- [ ] Set up environment configuration

### Phase 1: MVP - Core Chat Functionality
**Timeline**: 2-3 days
**Success Criteria**: Can chat with one provider through Clean Architecture

**Tasks**:
- [ ] Create domain layer (entities, value objects, interfaces)
- [ ] Implement Ollama provider adapter
- [ ] Create `SendMessageUseCase`
- [ ] Implement `ChainlitAdapter`
- [ ] Set up SQLite for basic chat history
- [ ] Add simple username authentication
- [ ] Test complete flow with Ollama

**Acceptance Criteria**:
- User can input username and chat with Ollama
- Chat messages stored in SQLite
- Architecture layers are clearly separated
- All code is fully typed

### Phase 2: Multi-Provider Support
**Timeline**: 2-3 days
**Success Criteria**: Can switch between all three providers

**Tasks**:
- [ ] Implement OpenRouter adapter
- [ ] Implement z.AI adapter
- [ ] Create provider abstraction interface
- [ ] Implement `SwitchProviderUseCase`
- [ ] Add provider selection UI to Chainlit
- [ ] Test all three providers with same queries
- [ ] Verify context persistence across switches

**Acceptance Criteria**:
- Can switch between all three providers
- Provider selection persists during session
- Chat history works with all providers
- Error handling for API failures

### Phase 3: Prompt Management
**Timeline**: 2 days
**Success Criteria**: AgentaAI integration working

**Tasks**:
- [ ] Create prompt domain model
- [ ] Implement AgentaAI adapter
- [ ] Create `ManagePromptsUseCase`
- [ ] Load system prompts at startup
- [ ] Integrate prompts into message flow
- [ ] Implement fallback to local prompts
- [ ] Test prompt management UI

**Acceptance Criteria**:
- Can fetch prompts from AgentaAI
- Prompts override default behavior
- Fallback to local prompts when AgentaAI unavailable
- Prompt configuration works

### Phase 4: Chat History (Enhanced)
**Timeline**: 1-2 days
**Success Criteria**: Rich chat history with filtering

**Tasks**:
- [ ] Implement `LoadHistoryUseCase`
- [ ] Create chat history view in Chainlit
- [ ] Add conversation continuation feature
- [ ] Implement history search/filter
- [ ] Add chat history clearing option
- [ ] Test persistence across sessions

**Acceptance Criteria**:
- Can view previous conversations
- Can continue previous conversations
- History persists correctly
- Clean history management

### Phase 5: Optional Memory Integration
**Timeline**: 1-2 days (optional)
**Success Criteria**: AI remembers context across conversations

**Tasks**:
- [ ] Install and configure Mem0
- [ ] Create `MemoryAdapter` interface
- [ ] Implement Mem0 integration
- [ ] Create `ConfigureMemoryUseCase`
- [ ] Integrate memory into chat flow
- [ ] Add memory limits configuration

**Acceptance Criteria**:
- Memory is stored per user
- AI references memory in conversations
- Memory can be disabled/configured
- Memory doesn't break normal flow

### Phase 6: Polish & Documentation
**Timeline**: 1-2 days
**Success Criteria**: Production-ready documentation

**Tasks**:
- [ ] Comprehensive docstrings for all functions
- [ ] Create architecture diagrams
- [ ] Write detailed README
- [ ] Add setup and configuration guide
- [ ] Create example configuration files
- [ ] Write testing guide
- [ ] Add type hints for all functions
- [ ] Code review and cleanup

**Acceptance Criteria**:
- Complete documentation
- All code follows Python 3.12 standards
- 100% type coverage
- Clean code with no linting errors

### Technical Risks & Mitigation

#### Risk 1: Architecture Over-Engineering
**Description**: Creating overly complex architecture for a learning project
**Impact**: Slows development, reduces maintainability
**Mitigation**:
- Keep architecture minimal and clear
- Focus on demonstrating principles, not complexity
- Use simple adapters first

#### Risk 2: API Rate Limits
**Description**: OpenRouter/z.AI rate limits during testing
**Impact**: Development slowed, testing incomplete
**Mitigation**:
- Prioritize Ollama for extensive testing
- Monitor API usage carefully
- Implement rate limit handling

#### Risk 3: AgentaAI Service Availability
**Description**: AgentaAI downtime or API changes
**Impact**: Prompt management breaks, no fallback
**Mitigation**:
- Implement robust fallback to local prompts
- Create mock adapters for testing
- Monitor AgentaAI status

#### Risk 4: Mem0 Integration Complexity
**Description**: Self-hosted Mem0 adds complexity
**Impact**: Delays project completion
**Mitigation**:
- Mark as optional from start
- Create simple adapter implementation
- Defer if time-constrained

#### Risk 5: Dependency Drift
**Description**: LangChain/Chainlit updates breaking code
**Impact**: Code breaks, requires extensive fixes
**Mitigation**:
- Pin versions in pyproject.toml
- Update dependencies incrementally
- Use concrete types instead of abstract generics initially

#### Risk 6: SQLite Performance
**Description**: SQLite doesn't scale well with large datasets
**Impact**: Performance degrades with many messages
**Mitigation**:
- Implement message archiving/purging
- Use indexes effectively
- Add query optimization

---

## 6. Non-Functional Requirements

### Performance
- **Response Time**: Chat response within 10 seconds for typical queries
- **Startup Time**: Application starts within 5 seconds
- **Memory Usage**: < 1GB RAM for typical operation
- **Concurrency**: Support for single user session (learning project)

### Maintainability
- **Code Coverage**: > 80% test coverage (if tests added)
- **Documentation**: All public APIs documented
- **Type Safety**: 100% type coverage
- **Code Style**: Follows AGENTS.md guidelines

### Reliability
- **Error Handling**: All external calls wrapped in error handling
- **Fail-Safe**: Graceful degradation when services unavailable
- **Logging**: Application events logged for debugging
- **Data Integrity**: SQLite constraints enforced

### Usability
- **Interface**: Clean Chainlit UI with clear labels
- **Configuration**: Environment variables for all settings
- **Error Messages**: Clear, actionable error messages
- **Onboarding**: Simple username input flow

### Security
- **Credential Storage**: Environment variables only
- **Data Privacy**: Local storage, no external data collection
- **Input Validation**: All user inputs validated
- **Authentication**: Username-based only (as specified)

---

## 7. Dependencies & Constraints

### External Dependencies
- **Python**: 3.12+ (as per AGENTS.md)
- **Chainlit**: 2.9.6+
- **LangChain**: 1.2.8+
- **AgentaAI**: To be specified in Phase 1
- **Mem0**: Self-hosted, optional

### Internal Constraints
- **Architecture**: Clean/Hexagonal architecture mandatory
- **Coding Standards**: Full typing, Google docstrings (as per AGENTS.md)
- **Development**: Must use `uv run` for all commands
- **Commit Policy**: No commits without explicit approval

### Business Constraints
- **Scope**: Learning project only, no production features
- **Time**: Phased approach, no strict deadline
- **Resources**: Individual developer, no team dependencies

---

## 8. Acceptance Criteria Summary

### Must-Have (MVP)
- [ ] Multi-provider support (OpenRouter, z.AI, Ollama)
- [ ] Clean/Hexagonal architecture implementation
- [ ] Simple username authentication
- [ ] Chat history persistence
- [ ] Chainlit frontend integration
- [ ] Full typing coverage
- [ ] No linting errors

### Should-Have (Phase 3)
- [ ] AgentaAI prompt management integration
- [ ] Prompt fallback mechanism
- [ ] Prompt versioning (optional)

### Nice-to-Have (Phase 5)
- [ ] Mem0 memory integration
- [ ] Advanced chat history features

---

## 9. Open Questions & Considerations

### Questions to Address
1. **AgentaAI Specifics**: Exact API endpoints and requirements
2. **z.AI API Details**: Official documentation and authentication
3. **Chat History Retention**: How long to keep messages
4. **Message Size Limits**: Maximum message length per message
5. **API Key Management**: Should we use a secrets manager?

### Technical Decisions to Consider
1. **Dependency Injection**: Should we use DI framework or manual wiring?
2. **Caching**: Should we cache LLM responses?
3. **Streaming**: Use Server-Sent Events (SSE) for streaming responses?
4. **Testing**: Unit vs integration tests, what level is appropriate?
5. **Configuration**: Environment variables vs config files vs CLI args?

---

**Document Version**: 1.0
**Last Updated**: 2026-02-06
**Status**: Approved for Implementation
