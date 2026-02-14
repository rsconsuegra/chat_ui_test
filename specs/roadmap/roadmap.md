# Roadmap

## Project Overview

This document outlines the phased rollout plan for the Clean/Hexagonal Architecture LLM Chat Application. The project is organized into clear phases with defined success criteria, tasks, and deliverables.

## Project Phases

### Phase 0: Foundation (Current State)

**Status**: In Progress
**Timeline**: 1 day
**Owner**: Developer

**Completed Tasks**:
- [x] Initial project setup
- [x] Dependencies added to pyproject.toml (chainlit>=2.9.6, langchain>=1.2.8)
- [x] Basic Chainlit echo handler created (main.py, src/app.py)
- [x] AGENTS.md guidelines defined
- [x] Repository initialized with git

**Next Actions**:
- [ ] Create folder structure for Clean/Hexagonal architecture
- [ ] Set up environment configuration (.env.example)
- [ ] Create basic domain models (User, ChatMessage)
- [ ] Initialize SQLite database

**Success Criteria**:
- [ ] Project structure created
- [ ] Environment configuration working
- [ ] Database initialized

**Acceptance Criteria**:
- [ ] Folder structure matches architecture plan
- [ ] .env.example has all required variables
- [ ] Database initialization script created
- [ ] Basic application can run

**Estimated Effort**: 1 day

---

### Phase 1: MVP - Core Chat Functionality

**Status**: Not Started
**Timeline**: 2-3 days
**Owner**: Developer

**Goal**: Build a working chat application with Ollama provider using Clean Architecture principles

**Tasks**:
- [ ] **Domain Layer Implementation**
  - [ ] Create `domain/models/user.py` - User entity
  - [ ] Create `domain/models/chat_message.py` - ChatMessage entity
  - [ ] Create `domain/models/message_role.py` - MessageRole enum
  - [ ] Create `domain/models/timestamp.py` - Timestamp data class
  - [ ] Create `domain/repositories/user_repository.py` - User repository interface
  - [ ] Create `domain/repositories/message_repository.py` - Message repository interface

- [ ] **Infrastructure Layer - Database**
  - [ ] Create `infrastructure/repositories/sqlite_user_repository.py` - User repository implementation
  - [ ] Create `infrastructure/repositories/sqlite_message_repository.py` - Message repository implementation
  - [ ] Implement database initialization script
  - [ ] Create database schema
  - [ ] Add indexes for performance

- [ ] **Infrastructure Layer - Providers**
  - [ ] Create `infrastructure/adapters/providers/base_provider.py` - Base provider interface
  - [ ] Create `infrastructure/adapters/providers/ollama_provider.py` - Ollama provider adapter
  - [ ] Implement streaming response handling
  - [ ] Add error handling for Ollama

- [ ] **Application Layer**
  - [ ] Create `application/use_cases/send_message_use_case.py` - Send message use case
  - [ ] Create `application/use_cases/load_history_use_case.py` - Load history use case
  - [ ] Create `application/use_cases/get_system_prompt_use_case.py` - Get system prompt
  - [ ] Implement user validation

- [ ] **Infrastructure Layer - Chainlit Adapter**
  - [ ] Create `infrastructure/adapters/chainlit/chainlit_adapter.py` - Chainlit integration
  - [ ] Implement username input dialog
  - [ ] Implement message streaming to UI
  - [ ] Integrate with use cases

- [ ] **Configuration**
  - [ ] Create `config/providers.py` - Provider configuration
  - [ ] Create `config/prompts.py` - Prompt configuration
  - [ ] Create `config/database.py` - Database configuration
  - [ ] Update `.env.example` with configuration variables

**Success Criteria**:
- [ ] Can input username and start chat
- [ ] Can send messages to Ollama
- [ ] Messages are saved to database
- [ ] Chat history persists
- [ ] Architecture layers are clearly separated
- [ ] No code is in wrong layer

**Acceptance Criteria**:
- [ ] User can create account (username)
- [ ] User can send message to Ollama
- [ ] Message appears in chat UI
- [ ] Message is saved to database
- [ ] Message persists after app restart
- [ ] All functions have type hints
- [ ] All code follows AGENTS.md guidelines

**Technical Requirements**:
- [ ] 100% type coverage
- [ ] All functions have Google docstrings
- [ ] No linting errors (uv run ruff check)
- [ ] Clean code structure

**Risk Mitigation**:
- [ ] Test Ollama connection first
- [ ] Implement database rollback on failure
- [ ] Use async operations for performance

**Estimated Effort**: 2-3 days

---

### Phase 2: Multi-Provider Support

**Status**: Not Started
**Timeline**: 2-3 days
**Owner**: Developer

**Goal**: Add OpenRouter and z.AI providers with provider switching

**Tasks**:
- [ ] **Provider Implementation**
  - [ ] Create `infrastructure/adapters/providers/openrouter_provider.py` - OpenRouter adapter
  - [ ] Create `infrastructure/adapters/providers/zai_provider.py` - z.AI adapter
  - [ ] Implement provider abstraction interface
  - [ ] Add provider health checking

- [ ] **Provider Management**
  - [ ] Create `domain/models/provider.py` - Provider model
  - [ ] Create `application/use_cases/switch_provider_use_case.py` - Switch provider
  - [ ] Implement provider selection UI
  - [ ] Add provider persistence in session

- [ ] **Enhanced Chat History**
  - [ ] Improve message storage with provider information
  - [ ] Add conversation continuation
  - [ ] Implement message filtering

- [ ] **Error Handling**
  - [ ] Implement fallback mechanism
  - [ ] Add provider error messages
  - [ ] Handle API failures gracefully

**Success Criteria**:
- [ ] Can switch between Ollama, OpenRouter, z.AI
- [ ] Provider selection persists
- [ ] Chat context maintained during switch
- [ ] All three providers work correctly
- [ ] Error handling prevents crashes

**Acceptance Criteria**:
- [ ] Provider dropdown in UI
- [ ] Switching provider doesn't lose messages
- [ ] Can chat with all three providers
- [ ] Provider error handled gracefully
- [ ] Error messages are clear and actionable

**Technical Requirements**:
- [ ] Provider abstraction implemented
- [ ] Each provider implements same interface
- [ ] Consistent error handling across providers
- [ ] Proper type hints and documentation

**Risk Mitigation**:
- [ ] Test with Ollama first (no API key needed)
- [ ] Use mock responses for API testing
- [ ] Implement graceful degradation

**Estimated Effort**: 2-3 days

---

### Phase 3: Prompt Management with AgentaAI

**Status**: Not Started
**Timeline**: 2 days
**Owner**: Developer

**Goal**: Integrate AgentaAI for prompt management with fallback

**Tasks**:
- [ ] **Prompt Domain Layer**
  - [ ] Create `domain/models/prompt.py` - Prompt entity
  - [ ] Create `domain/repositories/prompt_repository.py` - Prompt repository interface
  - [ ] Create `domain/models/memory_config.py` - MemoryConfig value object

- [ ] **AgentaAI Integration**
  - [ ] Create `infrastructure/adapters/agentaai/agentaai_prompt_adapter.py` - AgentaAI adapter
  - [ ] Implement API authentication
  - [ ] Implement prompt fetching
  - [ ] Implement prompt versioning (basic)

- [ ] **Fallback Mechanism**
  - [ ] Create local prompt templates (config/prompts.py)
  - [ ] Implement fallback logic
  - [ ] Add prompt configuration UI

- [ ] **Application Layer**
  - [ ] Create `application/use_cases/manage_prompts_use_case.py` - Manage prompts
  - [ ] Create `application/use_cases/get_system_prompt_use_case.py` - Get system prompt
  - [ ] Integrate prompts into message flow

**Success Criteria**:
- [ ] Can fetch prompts from AgentaAI
- [ ] System prompts work in chat
- [ ] Fallback to local prompts when AgentaAI unavailable
- [ ] Prompt configuration works

**Acceptance Criteria**:
- [ ] Can view available prompts
- [ ] Can select prompt template
- [ ] System prompt appears in chat
- [ ] Falls back to local prompts correctly
- [ ] Error messages clear when AgentaAI fails

**Technical Requirements**:
- [ ] Prompt repository interface
- [ ] AgentaAI adapter implementation
- [ ] Fallback mechanism robust
- [ ] Prompt validation

**Risk Mitigation**:
- [ ] Test with AgentaAI API first
- [ ] Implement comprehensive fallback
- [ ] Add mock adapter for testing

**Estimated Effort**: 2 days

---

### Phase 4: Chat History (Enhanced)

**Status**: Not Started
**Timeline**: 1-2 days
**Owner**: Developer

**Goal**: Enhance chat history with better user experience

**Tasks**:
- [ ] **Chat History UI**
  - [ ] Create conversation view component
  - [ ] Implement message filtering
  - [ ] Add message deletion option
  - [ ] Implement chat history export

- [ ] **Conversation Management**
  - [ ] Create conversation grouping logic
  - [ ] Implement conversation switching
  - [ ] Add conversation summary (optional)

- [ ] **Enhanced Features**
  - [ ] Add message search (optional)
  - [ ] Implement conversation tagging (optional)
  - [ ] Add message notifications (optional)

**Success Criteria**:
- [ ] Can view all conversations
- [ ] Can continue specific conversation
- [ ] Can clear chat history
- [ ] History persists correctly

**Acceptance Criteria**:
- [ ] List of conversations viewable
- [ ] Can select and continue conversation
- [ ] Can delete messages/conversations
- [ ] History persists across restarts

**Technical Requirements**:
- [ ] Enhanced repository methods
- [ ] Improved UI components
- [ ] Better database queries
- [ ] Performance optimization

**Estimated Effort**: 1-2 days

---

### Phase 5: Optional Memory Integration

**Status**: Not Started
**Timeline**: 1-2 days (Optional)
**Owner**: Developer

**Goal**: Integrate Mem0 for memory management

**Tasks**:
- [ ] **Memory Domain Layer**
  - [ ] Create `domain/models/memory.py` - Memory entity
  - [ ] Create `domain/repositories/memory_repository.py` - Memory repository interface
  - [ ] Create `domain/models/memory_config.py` - MemoryConfig value object

- [ ] **Mem0 Integration**
  - [ ] Create `infrastructure/adapters/mem0/mem0_memory_adapter.py` - Mem0 adapter
  - [ ] Implement memory storage
  - [ ] Implement memory retrieval
  - [ ] Implement memory deletion

- [ ] **Memory Configuration**
  - [ ] Add memory settings to UI
  - [ ] Implement memory limits
  - [ ] Add memory cleanup logic

- [ ] **Integration with Message Flow**
  - [ ] Modify SendMessageUseCase to include memory
  - [ ] Implement memory context in prompts
  - [ ] Add memory persistence to conversation

**Success Criteria**:
- [ ] Memory can be enabled/disabled
- [ ] Memories are stored correctly
- [ ] Memories retrieved based on context
- [ ] Memory limits enforced

**Acceptance Criteria**:
- [ ] Memory configuration UI
- [ ] Memories saved to Mem0
- [ ] Memories retrieved during chat
- [ ] Memory operations don't break flow

**Technical Requirements**:
- [ ] Memory repository interface
- [ ] Mem0 adapter implementation
- [ ] Memory context integration
- [ ] Proper error handling

**Risk Mitigation**:
- [ ] Start with memory disabled
- [ ] Implement comprehensive error handling
- [ ] Test with mock Mem0 if needed

**Estimated Effort**: 1-2 days

---

### Phase 6: Polish & Documentation

**Status**: Not Started
**Timeline**: 1-2 days
**Owner**: Developer

**Goal**: Create production-ready documentation and final polish

**Tasks**:
- [ ] **Documentation**
  - [ ] Update README.md with complete setup instructions
  - [ ] Add architecture diagrams
  - [ ] Create API documentation
  - [ ] Add troubleshooting guide
  - [ ] Document environment variables

- [ ] **Code Quality**
  - [ ] Add docstrings to all functions
  - [ ] Add type hints to all functions
  - [ ] Run linting and fix issues
  - [ ] Run formatting with black
  - [ ] Remove any commented code

- [ ] **Testing**
  - [ ] Add unit tests for critical components
  - [ ] Add integration tests for key flows
  - [ ] Test all user stories
  - [ ] Create test documentation

- [ ] **Final Polish**
  - [ ] Clean up code structure
  - [ ] Remove debug code
  - [ ] Optimize performance
  - [ ] Add comments where helpful

**Success Criteria**:
- [ ] Complete documentation
- [ ] All code follows standards
- [ ] Tests pass
- [ ] Clean, maintainable code

**Acceptance Criteria**:
- [ ] README has setup instructions
- [ ] All public functions documented
- [ ] 100% type coverage
- [ ] No linting errors
- [ ] No commented code

**Technical Requirements**:
- [ ] Complete documentation
- [ ] All functions have docstrings
- [ ] All functions typed
- [ ] Clean code structure

**Estimated Effort**: 1-2 days

---

## Critical Path

```
Phase 0 (Foundation)
    ↓
Phase 1 (MVP)
    ↓
Phase 2 (Multi-Provider)
    ↓
Phase 3 (Prompt Management)
    ↓
Phase 4 (Chat History)
    ↓
Phase 6 (Polish & Documentation)
```

**Optional Path**:
```
Phase 5 (Memory Integration) - Can be done anytime after Phase 1
```

---

## Milestones

### Milestone 1: MVP Complete
**Completion**: End of Phase 1
**Checklist**:
- [ ] Basic chat functionality works
- [ ] Ollama provider functional
- [ ] Clean Architecture demonstrated
- [ ] Username authentication working
- [ ] Chat history persistent

### Milestone 2: Multi-Provider Ready
**Completion**: End of Phase 2
**Checklist**:
- [ ] All three providers working
- [ ] Provider switching functional
- [ ] Context maintained during switch
- [ ] Error handling robust

### Milestone 3: Prompt Management
**Completion**: End of Phase 3
**Checklist**:
- [ ] AgentaAI integration working
- [ ] Local prompt fallback functional
- [ ] Prompt management UI working
- [ ] System prompts integrated

### Milestone 4: Feature Complete
**Completion**: End of Phase 4
**Checklist**:
- [ ] Enhanced chat history
- [ ] Conversation management
- [ ] Message deletion working
- [ ] All core features functional

### Milestone 5: Documentation Complete
**Completion**: End of Phase 6
**Checklist**:
- [ ] Complete documentation
- [ ] Clean code structure
- [ ] Tests passing
- [ ] Ready for review

---

## Risk Management

### Phase 1 Risks

**Risk 1**: Ollama Service Unavailable
- **Probability**: Low
- **Impact**: Medium
- **Mitigation**: Use mock responses for testing, implement fallback

**Risk 2**: Database Performance Issues
- **Probability**: Low
- **Impact**: Medium
- **Mitigation**: Use indexes, implement pagination, test performance

**Risk 3**: Architecture Complexity
- **Probability**: Medium
- **Impact**: High
- **Mitigation**: Keep architecture simple, focus on learning, don't over-engineer

### Phase 2 Risks

**Risk 1**: Provider API Changes
- **Probability**: Medium
- **Impact**: High
- **Mitigation**: Pin versions, implement stable abstractions, handle errors

**Risk 2**: API Rate Limits
- **Probability**: Medium
- **Impact**: Medium
- **Mitigation**: Use Ollama for testing, monitor usage, implement rate limiting

### Phase 3 Risks

**Risk 1**: AgentaAI Service Unavailability
- **Probability**: Medium
- **Impact**: Medium
- **Mitigation**: Robust fallback to local prompts, mock adapter for testing

**Risk 2**: Prompt Format Issues
- **Probability**: Low
- **Impact**: Medium
- **Mitigation**: Validate prompt format, implement strict parsing

### Phase 4 Risks

**Risk 1**: Performance with Large History
- **Probability**: Medium
- **Impact**: Medium
- **Mitigation**: Implement pagination, add indexing, optimize queries

### Phase 5 Risks

**Risk 1**: Mem0 Integration Complexity
- **Probability**: Medium
- **Impact**: Medium
- **Mitigation**: Start with simple integration, mark as optional, implement fallback

### Phase 6 Risks

**Risk 1**: Documentation Overhead
- **Probability**: Medium
- **Impact**: Medium
- **Mitigation**: Document incrementally, focus on critical documentation

**Risk 2**: Time Constraints
- **Probability**: High
- **Impact**: High
- **Mitigation**: Prioritize features, skip optional items if needed

---

## Dependency Management

### External Dependencies
- **LangChain**: Version 1.2.8+ (for LLM orchestration)
- **Chainlit**: Version 2.9.6+ (for frontend UI)
- **Ollama**: Local service (no version constraints)
- **AgentaAI**: TBD (API will be specified during Phase 3)
- **Mem0**: TBD (self-hosted service, will configure during Phase 5)

### Internal Dependencies
- **Phase 1**: No external dependencies
- **Phase 2**: Depends on Phase 1 completion
- **Phase 3**: Depends on Phase 1 completion
- **Phase 4**: Depends on Phase 1 completion
- **Phase 5**: Depends on Phase 1 completion (can be done in parallel)
- **Phase 6**: Depends on all phases completion

---

## Quality Gates

### Pre-Phase 1
- [ ] Environment configured
- [ ] Dependencies installed
- [ ] Basic project structure created

### Pre-Phase 2
- [ ] Phase 1 completed
- [ ] Ollama provider working
- [ ] Database functional
- [ ] Clean Architecture demonstrated

### Pre-Phase 3
- [ ] Phase 2 completed
- [ ] Multi-provider working
- [ ] Context maintained
- [ ] Error handling robust

### Pre-Phase 4
- [ ] Phase 3 completed
- [ ] Prompt management working
- [ ] AgentaAI integration stable

### Pre-Phase 5
- [ ] Phase 1 completed
- [ ] Optional memory integration

### Pre-Phase 6
- [ ] All phases completed
- [ ] All features working
- [ ] Code quality standards met

---

## Metrics & Success Criteria

### Code Quality Metrics
- [ ] 100% type coverage
- [ ] No linting errors (ruff)
- [ ] Consistent formatting (black)
- [ ] Complete documentation
- [ ] No commented code

### Functional Metrics
- [ ] All three providers working
- [ ] Chat history persistent
- [ ] Username authentication working
- [ ] Prompt management functional
- [ ] Optional memory working

### Architecture Metrics
- [ ] Clear layer separation
- [ ] No circular dependencies
- [ ] Proper dependency flow
- [ ] SOLID principles followed
- [ ] Clean/Hexagonal architecture demonstrated

### User Experience Metrics
- [ ] Response time < 10 seconds
- [ ] Application starts < 5 seconds
- [ ] Error messages clear
- [ ] Intuitive UI
- [ ] Easy to use

---

## Contingency Plan

### Time Extensions
- If Phase 1 extends beyond 3 days:
  - [ ] Prioritize core features only
  - [ ] Skip optional features
  - [ ] Focus on learning goals

- If Phase 2 extends beyond 3 days:
  - [ ] Start with one new provider
  - [ ] Defer advanced features
  - [ ] Focus on stability

- If Phase 3 extends beyond 2 days:
  - [ ] Use mock AgentaAI responses
  - [ ] Focus on fallback mechanism
  - [ ] Simplify prompt features

### Feature Reduction
If project time is constrained:
- [ ] Defer Phase 4 (Chat History enhancements)
- [ ] Defer Phase 5 (Memory integration)
- [ ] Focus on Phases 1-3

### Scope Reduction
If further constraints:
- [ ] Use only Ollama (single provider)
- [ ] Use local prompts only (no AgentaAI)
- [ ] Simple chat history only

---

## Notes

- **Project Purpose**: Educational learning project
- **Success Definition**: Clean/Hexagonal Architecture demonstrated
- **Priorities**: Learning over perfection
- **Flexibility**: Adapt timeline as needed
- **Focus**: Architecture principles, not features

---

**Document Version**: 1.0
**Last Updated**: 2026-02-06
**Status**: Approved
