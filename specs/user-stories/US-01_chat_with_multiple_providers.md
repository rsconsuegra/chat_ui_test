# User Story: Chat with Multiple LLM Providers

## Story Details
**ID**: US-01
**Priority**: P0 (Must Have)
**Status**: Not Started
**Estimated Effort**: 2-3 days

## Narrative
As a user, I want to switch between different LLM providers (OpenRouter, z.AI, Ollama) so that I can test different models and capabilities.

## Acceptance Criteria

### Functional Requirements
- [ ] User can select provider from dropdown in Chainlit UI
- [ ] Provider selection persists during session
- [ ] Each provider uses LangChain abstraction layer
- [ ] API keys for each provider configurable via environment variables
- [ ] Error handling for provider failures does not break other providers
- [ ] Provider switching does not lose chat context
- [ ] All providers use consistent response format

### Technical Requirements
- [ ] Provider abstraction interface defined in domain layer
- [ ] Primary adapter (Chainlit) uses abstraction
- [ ] Each provider implements adapter interface
- [ ] Configuration management via environment variables
- [ ] Proper error handling and logging
- [ ] No tight coupling between providers

### User Interface Requirements
- [ ] Chainlit UI has provider selection dropdown
- [ ] Dropdown shows available providers
- [ ] Default provider set (e.g., Ollama)
- [ ] Selection persists across messages
- [ ] Clear feedback when provider changes

### Non-Functional Requirements
- [ ] Response format consistent across providers
- [ ] Error messages clear and actionable
- [ ] Performance acceptable (< 10s response time)
- [ ] No race conditions with concurrent requests

## Out of Scope

### Explicitly Not Included
- [ ] Provider feature flags or availability toggles
- [ ] Custom provider loading system
- [ ] Provider health monitoring
- [ ] Provider performance metrics collection
- [ ] Provider benchmarking tools
- [ ] Provider selection based on context or query

### Future Enhancements (Not Now)
- [ ] Dynamic provider loading without restart
- [ ] Provider configuration UI
- [ ] Provider metrics dashboard
- [ ] Provider benchmarking suite
- [ ] Provider auto-selection based on query type

## Test Scenarios

### Positive Scenarios
1. **Select Provider**: User selects Ollama provider from dropdown
2. **Chat with Provider**: User sends message to Ollama provider
3. **Switch Provider**: User switches from Ollama to OpenRouter
4. **Continue Chat**: User continues chat with new provider (context preserved)
5. **Different Models**: User tests different models via provider

### Negative Scenarios
1. **Provider Failure**: OpenRouter API returns error, user can still use other providers
2. **Invalid Provider**: User selects invalid provider, system shows error
3. **Missing API Key**: Provider without valid API key shows clear error message
4. **Network Error**: Network failure handled gracefully

### Edge Cases
1. **Concurrent Requests**: Multiple messages sent rapidly
2. **Large Responses**: Large model responses handled correctly
3. **Empty Messages**: Empty message handling
4. **Special Characters**: Messages with special characters work correctly
5. **Unicode**: Unicode characters in messages

## Dependencies

### Blockers
- None (can start independently)

### Prerequisites
- LangChain framework installed and configured
- At least one provider adapter implemented
- Chainlit frontend setup

### Related User Stories
- US-02: Simple Username Authentication (needed for proper history)
- US-03: Chat History Management (history integration)

## Implementation Notes

### Architecture Pattern
- Use adapter pattern for provider abstraction
- Domain layer defines interface (port)
- Infrastructure layer implements adapters
- Application layer uses abstraction via interfaces

### File Structure
```
src/
├── domain/
│   ├── models/
│   │   ├── provider.py (abstract base class)
│   │   └── provider_config.py
│   └── interfaces/
│       └── provider.py (provider abstraction)
├── application/
│   └── use_cases/
│       └── send_message_use_case.py
├── infrastructure/
│   └── adapters/
│       ├── providers/
│       │   ├── ollama_provider.py
│       │   ├── openrouter_provider.py
│       │   └── zai_provider.py
│       └── chainlit_adapter.py
└── config/
    └── providers.py
```

### Code Examples

#### Provider Interface (domain/interfaces/provider.py)
```python
from abc import ABC, abstractmethod
from typing import AsyncGenerator, Any

class IProvider(ABC):
    @abstractmethod
    async def generate_response(
        self,
        messages: list[dict[str, str]],
        system_prompt: str | None = None
    ) -> AsyncGenerator[str, None]:
        """Generate response from LLM provider."""
        pass

    @abstractmethod
    async def get_model_info(self) -> dict[str, Any]:
        """Get information about the provider and model."""
        pass
```

#### Ollama Adapter (infrastructure/adapters/providers/ollama_provider.py)
```python
from domain.interfaces.provider import IProvider
from config.providers import get_ollama_config

class OllamaProvider(IProvider):
    def __init__(self):
        self.config = get_ollama_config()

    async def generate_response(
        self,
        messages: list[dict[str, str]],
        system_prompt: str | None = None
    ) -> AsyncGenerator[str, None]:
        # Implementation
        pass

    async def get_model_info(self) -> dict[str, Any]:
        # Implementation
        pass
```

### Testing Strategy
1. **Unit Tests**: Test adapter implementations in isolation
2. **Integration Tests**: Test provider switching with Chainlit
3. **End-to-End Tests**: Full flow with real API calls
4. **Mock Tests**: Test with mocked responses

### Performance Considerations
- Provider switching should be instant (< 1s)
- Response generation uses async operations
- No blocking calls during response generation

## Success Metrics
- [ ] All three providers functional
- [ ] Provider switching works seamlessly
- [ ] Error handling prevents cascading failures
- [ ] No context loss during provider switch
- [ ] Consistent response format

## Risk Assessment
**High Risk**: None identified
**Medium Risk**: Provider API changes could break adapters
**Mitigation**: Pin versions, create stable abstraction layer

## Notes
- Start with Ollama for local development (no API key needed)
- Add OpenRouter and z.AI once Ollama is stable
- Use environment variables for API keys
- Provide clear error messages when API key is missing
