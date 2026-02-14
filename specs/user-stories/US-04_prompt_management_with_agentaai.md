# User Story: Prompt Management with AgentaAI

## Story Details
**ID**: US-04
**Priority**: P1 (Should Have)
**Status**: Not Started
**Estimated Effort**: 2 days

## Narrative
As a user, I want to manage prompts through AgentaAI so that I can version and track prompt templates.

## Acceptance Criteria

### Functional Requirements
- [ ] Integration with AgentaAI API
- [ ] Can pull prompts from AgentaAI
- [ ] System prompts configurable via AgentaAI
- [ ] Fallback to local prompts if AgentaAI unavailable
- [ ] Prompt templates loaded at application startup
- [ ] Prompt versioning available (optional)

### Technical Requirements
- [ ] AgentaAI adapter implementation
- [ ] Prompt domain model
- [ ] Prompt configuration management
- [ ] Graceful fallback to local prompts
- [ ] Error handling for AgentaAI failures
- [ ] Prompt versioning support (optional)

### User Interface Requirements
- [ ] View available prompt templates
- [ ] Select prompt template for use
- [ ] View prompt template details
- [ ] System prompt appears in chat (if configured)
- [ ] Clear feedback when using AgentaAI prompts

### Non-Functional Requirements
- [ ] Prompts loaded quickly at startup (< 5 seconds)
- [ ] Fallback mechanism reliable
- [ ] No prompt loss when AgentaAI unavailable
- [ ] Prompt changes reflect immediately
- [ ] Error messages clear when AgentaAI fails

## Out of Scope

### Explicitly Not Included
- [ ] Edit prompts directly in AgentaAI
- [ ] Create new prompt templates
- [ ] Share prompts between users
- [ ] Prompt analytics or usage tracking
- [ ] Prompt A/B testing
- [ ] Prompt version history UI
- [ ] Prompt approval workflow
- [ ] Real-time prompt updates

### Future Enhancements (Not Now)
- [ ] Edit prompts in AgentaAI
- [ ] Create custom prompt templates
- [ ] Prompt sharing between users
- [ ] Prompt usage analytics
- [ ] Prompt version history UI
- [ ] Prompt A/B testing framework
- [ ] Prompt approval workflows
- [ ] Real-time prompt updates via websockets
- [ ] Prompt performance evaluation

## Test Scenarios

### Positive Scenarios
1. **Fetch Prompts**: Application successfully fetches prompts from AgentaAI
2. **Use AgentaAI Prompt**: User can use AgentaAI prompt template
3. **Fallback to Local**: Uses local prompt when AgentaAI unavailable
4. **Prompt Updates**: AgentaAI prompt changes reflected immediately
5. **Multiple Prompts**: Can select different prompt templates
6. **Version Support**: Can use specific prompt versions

### Negative Scenarios
1. **AgentaAI Unavailable**: Falls back to local prompt gracefully
2. **API Error**: Handles AgentaAI API errors
3. **Invalid Prompt**: Validates prompt format
4. **Empty Response**: Handles empty prompt responses
5. **Network Error**: Handles network failures

### Edge Cases
1. **No Prompts**: Application works without any prompts
2. **Empty AgentaAI Response**: Fallback to empty local prompt
3. **Large Prompts**: Handles large prompt templates
4. **Special Characters**: Prompts with special characters
5. **Unicode**: Prompts with unicode characters
6. **Version Mismatch**: Handles prompt version differences

## Dependencies

### Blockers
- [ ] AgentaAI API details (to be specified)
- [ ] Database schema for prompts (if local storage)

### Prerequisites
- Chainlit application structure
- Basic error handling infrastructure
- Configuration management

### Related User Stories
- US-01: Chat with Multiple Providers (uses system prompts)
- US-03: Chat History Management (stores messages with system context)

## Implementation Notes

### Architecture Pattern
- Use repository pattern for prompt management
- Domain layer defines prompt model and repository interface
- Infrastructure layer implements AgentaAI adapter
- Application layer manages prompt lifecycle
- Fallback mechanism uses local storage

### File Structure
```
src/
├── domain/
│   ├── models/
│   │   ├── prompt.py (Prompt entity)
│   │   └── provider.py (provider abstraction)
│   └── repositories/
│       └── prompt_repository.py (abstract interface)
├── application/
│   └── use_cases/
│       ├── manage_prompts_use_case.py
│       └── get_system_prompt_use_case.py
├── infrastructure/
│   └── adapters/
│       └── agentaai/
│           └── agentaai_prompt_adapter.py
└── config/
    └── prompts.py (local prompt defaults)
```

### Code Examples

#### Prompt Entity (domain/models/prompt.py)
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Prompt:
    id: str
    name: str
    content: str
    version: str
    provider: str  # 'agentaai' or 'local'
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def create(
        cls,
        id: str,
        name: str,
        content: str,
        version: str = "1.0",
        provider: str = "local"
    ) -> "Prompt":
        """Create a new prompt."""
        return cls(
            id=id,
            name=name,
            content=content,
            version=version,
            provider=provider
        )
```

#### Prompt Repository Interface (domain/repositories/prompt_repository.py)
```python
from abc import ABC, abstractmethod
from typing import Optional
from domain.models.prompt import Prompt

class IPromptRepository(ABC):
    @abstractmethod
    async def get_prompt_by_name(
        self,
        name: str,
        provider: Optional[str] = None
    ) -> Optional[Prompt]:
        """Get prompt by name."""
        pass

    @abstractmethod
    async def get_all_prompts(self) -> list[Prompt]:
        """Get all available prompts."""
        pass

    @abstractmethod
    async def refresh_from_agentaai(self) -> list[Prompt]:
        """Refresh prompts from AgentaAI."""
        pass
```

#### AgentaAI Prompt Adapter (infrastructure/adapters/agentaai/agentaai_prompt_adapter.py)
```python
from typing import Optional, list
from domain.models.prompt import Prompt
from domain.repositories.prompt_repository import IPromptRepository
from config.prompts import get_local_prompt

class AgentaAIPromptAdapter(IPromptRepository):
    def __init__(
        self,
        api_key: str,
        base_url: str,
        message_repo: Optional[IMessageRepository] = None
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.message_repo = message_repo

    async def get_prompt_by_name(
        self,
        name: str,
        provider: Optional[str] = None
    ) -> Optional[Prompt]:
        """Get prompt by name from AgentaAI or fallback to local."""
        # Try AgentaAI first
        if provider != "local":
            agentaai_prompt = await self._fetch_from_agentaai(name)
            if agentaai_prompt:
                return agentaai_prompt

        # Fallback to local
        return get_local_prompt(name)

    async def get_all_prompts(self) -> list[Prompt]:
        """Get all prompts from AgentaAI."""
        # Fetch all prompts from AgentaAI
        pass

    async def refresh_from_agentaai(self) -> list[Prompt]:
        """Refresh prompts from AgentaAI."""
        # Implementation
        pass

    async def _fetch_from_agentaai(self, name: str) -> Optional[Prompt]:
        """Fetch specific prompt from AgentaAI."""
        # Implementation using requests or httpx
        pass
```

#### Local Prompt Configuration (config/prompts.py)
```python
from domain.models.prompt import Prompt

# Local prompt templates as fallback
LOCAL_PROMPTS = {
    "system": Prompt.create(
        id="system",
        name="system",
        content="You are a helpful AI assistant. You answer questions accurately and helpfully.",
        version="1.0",
        provider="local"
    ),
    "coding": Prompt.create(
        id="coding",
        name="coding",
        content="You are a coding assistant. Provide clear explanations and working code examples.",
        version="1.0",
        provider="local"
    ),
    "general": Prompt.create(
        id="general",
        name="general",
        content="You are a helpful assistant. Answer questions clearly and concisely.",
        version="1.0",
        provider="local"
    )
}

def get_local_prompt(name: str) -> Optional[Prompt]:
    """Get local prompt by name."""
    return LOCAL_PROMPTS.get(name)
```

### AgentaAI Integration

#### API Request Example
```python
import httpx

async def fetch_prompt_from_agentaai(name: str) -> Optional[Prompt]:
    """Fetch prompt from AgentaAI."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{self.base_url}/api/prompts/{name}",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )

        if response.status_code == 200:
            data = response.json()
            return Prompt(
                id=data.get("id", name),
                name=data.get("name", name),
                content=data.get("content", ""),
                version=data.get("version", "1.0"),
                provider="agentaai"
            )

    return None
```

### Fallback Mechanism

```python
async def get_system_prompt(self, name: str) -> str:
    """Get system prompt, using AgentaAI with local fallback."""
    prompt = await self.get_prompt_by_name(name)

    if not prompt:
        return "You are a helpful AI assistant."

    return prompt.content
```

### Use Case Examples

#### Manage Prompts Use Case (application/use_cases/manage_prompts_use_case.py)
```python
from typing import list
from domain.repositories.prompt_repository import IPromptRepository

class ManagePromptsUseCase:
    def __init__(self, prompt_repo: IPromptRepository):
        self.prompt_repo = prompt_repo

    async def execute(self) -> list[Prompt]:
        """Get all available prompts."""
        return await self.prompt_repo.get_all_prompts()
```

#### Get System Prompt Use Case
```python
from typing import Optional
from domain.repositories.prompt_repository import IPromptRepository

class GetSystemPromptUseCase:
    def __init__(self, prompt_repo: IPromptRepository):
        self.prompt_repo = prompt_repo

    async def execute(self, name: str) -> str:
        """Get system prompt for use case."""
        prompt = await self.prompt_repo.get_prompt_by_name(name)

        if not prompt:
            return "You are a helpful AI assistant."

        return prompt.content
```

### Configuration

#### Environment Variables
```bash
# AgentaAI Configuration
AGENTA_API_KEY=agenta_api_key_here
AGENTA_BASE_URL=https://api.agenta.ai
```

#### Default Prompts
```python
# Fallback prompts when AgentaAI unavailable
DEFAULT_PROMPTS = {
    "system": "You are a helpful AI assistant. You answer questions accurately and helpfully.",
    "coding": "You are a coding assistant. Provide clear explanations and working code examples.",
    "general": "You are a helpful assistant. Answer questions clearly and concisely."
}
```

### Testing Strategy
1. **Unit Tests**: Adapter implementations
2. **Integration Tests**: AgentaAI API calls
3. **Fallback Tests**: Local prompt fallback mechanism
4. **Error Handling Tests**: API error scenarios
5. **Edge Case Tests**: Empty responses, large prompts

### Error Handling

#### AgentaAI Unavailable Scenario
```python
async def get_prompt_with_fallback(self, name: str) -> Prompt:
    """Get prompt with AgentaAI fallback."""
    try:
        # Try AgentaAI
        prompt = await self._fetch_from_agentaai(name)
        if prompt:
            return prompt
    except Exception as e:
        logger.warning(f"AgentaAI unavailable: {e}")

    # Fallback to local
    logger.info(f"Using local prompt for {name}")
    return get_local_prompt(name)
```

### Performance Considerations
- Load prompts at application startup
- Cache prompts in memory
- Fetch from AgentaAI on-demand if needed
- Implement prompt refresh mechanism

### Security Considerations
- [ ] Validate API key
- [ ] Validate API endpoints
- [ ] Sanitize prompt content
- [ ] Handle malformed responses
- [ ] No code execution from prompts
- [ ] Rate limit API calls

## Success Metrics
- [ ] AgentaAI integration works correctly
- [ ] Fallback to local prompts is reliable
- [ ] Prompts loaded quickly at startup
- [ ] Error messages clear when AgentaAI fails
- [ ] Prompt changes reflected immediately
- [ ] No prompt data loss

## Risk Assessment
**Medium Risk**: AgentaAI service availability
**Mitigation**: Robust fallback mechanism, local prompts

**Low Risk**: API authentication failures
**Mitigation**: Clear error messages, validation

**Low Risk**: Prompt versioning complexity
**Mitigation**: Start with simple versioning, enhance later

## Notes
- Start with simple prompt management
- Use AgentaAI as primary source, local as fallback
- Load prompts at application startup
- Implement graceful degradation
- Keep prompt templates simple initially
- Can enhance with versioning and editing later
- Focus on demonstrating architecture patterns
