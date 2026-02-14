# User Story: Optional Memory Integration

## Story Details
**ID**: US-05
**Priority**: P2 (Nice to Have)
**Status**: Not Started
**Estimated Effort**: 1-2 days

## Narrative
As a user, I want the AI to remember context from our conversation so that I don't have to repeat information.

## Acceptance Criteria

### Functional Requirements
- [ ] Integration with self-hosted Mem0
- [ ] Memory tied to username
- [ ] Configurable memory limits
- [ ] Context window management
- [ ] Memory retrieval integrated into chat flow
- [ ] Memory can be disabled/configured

### Technical Requirements
- [ ] Mem0 adapter implementation
- [ ] Memory domain model
- [ ] Memory storage abstraction
- [ ] Context window management
- [ ] Memory limits enforcement
- [ ] Memory cleanup (optional)

### User Interface Requirements
- [ ] Memory configuration options
- [ ] Clear indication when memory is enabled
- [ ] Memory settings persist
- [ ] Option to view stored memories (optional)
- [ ] Option to clear memory (optional)

### Non-Functional Requirements
- [ ] Memory retrieval integrated into message flow
- [ ] Memory operations do not slow down response
- [ ] Configurable memory limits respected
- [ ] Memory data persists correctly
- [ ] Memory operations are atomic

## Out of Scope

### Explicitly Not Included
- [ ] Advanced memory management UI
- [ ] Memory search functionality
- [ ] Memory sharing between users
- [ ] Memory export/import
- [ ] Memory analytics
- [ ] Memory versioning
- [ ] Multi-language memory
- [ ] Memory backup/restore
- [ ] Memory encryption
- [ ] Collaborative memory features

### Future Enhancements (Not Now)
- [ ] Memory search and retrieval
- [ ] Memory sharing between users
- [ ] Memory export/import
- [ ] Memory analytics dashboard
- [ ] Memory version history
- [ ] Multi-language support
- [ ] Memory backup/restore
- [ ] Memory encryption
- [ ] Collaborative memory
- [ ] Memory recommendation engine
- [ ] Memory re-ranking

## Test Scenarios

### Positive Scenarios
1. **Enable Memory**: User enables memory for their account
2. **Save Memory**: User's preferences are stored in memory
3. **Retrieve Memory**: AI retrieves relevant memories during conversation
4. **Context Integration**: Memories are integrated into conversation context
5. **Disabled Memory**: Memory can be disabled and not used
6. **Memory Limits**: Memory limits are enforced
7. **Memory Persistence**: Memory persists across sessions
8. **Memory Cleanup**: Old memories are cleaned up (if configured)

### Negative Scenarios
1. **Memory Disabled**: Memory operations skipped when disabled
2. **Empty Memory**: No memory stored initially
3. **Memory Failure**: Memory operations handled gracefully
4. **Exceed Limits**: Memory operations fail when limit exceeded
5. **Memory Update**: Existing memory can be updated

### Edge Cases
1. **No Memory**: Empty memory storage
2. **Large Memory**: Many memories stored
3. **Memory Deletion**: Memory can be deleted
4. **Special Characters**: Memory with special characters
5. **Unicode**: Memory with unicode characters
6. **Memory Updates**: Updating existing memories

## Dependencies

### Blockers
- [ ] Mem0 service configuration (to be specified)
- [ ] Chat message flow integration (US-01, US-03)

### Prerequisites
- Basic application structure
- Chainlit session management
- Configuration management

### Related User Stories
- US-01: Chat with Multiple Providers (message flow integration)
- US-03: Chat History Management (memory complements history)
- US-04: Prompt Management with AgentaAI (uses memory context)

## Implementation Notes

### Architecture Pattern
- Use adapter pattern for memory abstraction
- Domain layer defines memory model and repository interface
- Infrastructure layer implements Mem0 adapter
- Application layer manages memory lifecycle
- Memory integrated into message flow

### File Structure
```
src/
├── domain/
│   ├── models/
│   │   ├── memory.py (Memory entity)
│   │   └── memory_config.py (MemoryConfig value object)
│   └── repositories/
│       └── memory_repository.py (abstract interface)
├── application/
│   └── use_cases/
│       ├── save_memory_use_case.py
│       ├── get_relevant_memories_use_case.py
│       └── configure_memory_use_case.py
├── infrastructure/
│   └── adapters/
│       └── mem0/
│           └── mem0_memory_adapter.py
└── config/
    └── memory.py (memory configuration)
```

### Code Examples

#### Memory Entity (domain/models/memory.py)
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Memory:
    id: str
    user_id: str
    content: str
    tags: list[str]
    created_at: datetime
    updated_at: Optional[datetime] = None

    @classmethod
    def create(
        cls,
        user_id: str,
        content: str,
        tags: list[str] = None
    ) -> "Memory":
        """Create a new memory."""
        return cls(
            id=f"memory-{datetime.now().timestamp()}",
            user_id=user_id,
            content=content,
            tags=tags or [],
            created_at=datetime.now()
        )
```

#### Memory Config Value Object (domain/models/memory_config.py)
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class MemoryConfig:
    enabled: bool
    max_memories: int = 10
    memory_ttl_days: int = 30
    tag_strategy: str = "auto"  # 'auto', 'none', 'custom'

    def should_save_memory(self) -> bool:
        """Check if memory should be saved based on configuration."""
        return self.enabled
```

#### Memory Repository Interface (domain/repositories/memory_repository.py)
```python
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.memory import Memory
from domain.models.memory_config import MemoryConfig

class IMemoryRepository(ABC):
    @abstractmethod
    async def save_memory(self, memory: Memory) -> Memory:
        """Save a memory for user."""
        pass

    @abstractmethod
    async def get_relevant_memories(
        self,
        user_id: str,
        context: str,
        limit: int = 5
    ) -> List[Memory]:
        """Get relevant memories based on context."""
        pass

    @abstractmethod
    async def get_user_memories(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[Memory]:
        """Get all memories for user."""
        pass

    @abstractmethod
    async def clear_user_memories(self, user_id: str) -> int:
        """Clear all memories for user."""
        pass

    @abstractmethod
    async def delete_memory(self, memory_id: str) -> bool:
        """Delete a specific memory."""
        pass
```

#### Mem0 Memory Adapter (infrastructure/adapters/mem0/mem0_memory_adapter.py)
```python
from typing import List
from domain.models.memory import Memory
from domain.repositories.memory_repository import IMemoryRepository

class Mem0MemoryAdapter(IMemoryRepository):
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    async def save_memory(self, memory: Memory) -> Memory:
        """Save memory using Mem0 API."""
        # Implementation using requests or httpx
        pass

    async def get_relevant_memories(
        self,
        user_id: str,
        context: str,
        limit: int = 5
    ) -> List[Memory]:
        """Get relevant memories based on context."""
        # Implementation using Mem0 similarity search
        pass

    async def get_user_memories(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[Memory]:
        """Get all memories for user."""
        # Implementation using Mem0 retrieval
        pass

    async def clear_user_memories(self, user_id: str) -> int:
        """Clear all memories for user."""
        # Implementation using Mem0 deletion
        pass

    async def delete_memory(self, memory_id: str) -> bool:
        """Delete a specific memory."""
        # Implementation using Mem0 deletion
        pass
```

### Configuration

#### Environment Variables
```bash
# Memory Configuration
MEM0_ENABLED=false
MEM0_BASE_URL=http://localhost:8080
MEM0_API_KEY=mem0_key_here
```

#### Memory Config (config/memory.py)
```python
from domain.models.memory_config import MemoryConfig

# Default memory configuration
DEFAULT_MEMORY_CONFIG = MemoryConfig(
    enabled=False,
    max_memories=10,
    memory_ttl_days=30,
    tag_strategy="auto"
)

def get_memory_config() -> MemoryConfig:
    """Get memory configuration from environment variables."""
    import os

    enabled = os.getenv("MEM0_ENABLED", "false").lower() == "true"

    return MemoryConfig(
        enabled=enabled,
        max_memories=int(os.getenv("MEM0_MAX_MEMORIES", "10")),
        memory_ttl_days=int(os.getenv("MEM0_TTL_DAYS", "30"))
    )
```

### Memory Usage Pattern

#### Message Flow Integration
```python
async def send_message_with_memory(
    user_id: str,
    message: str,
    memory_repo: IMemoryRepository,
    memory_config: MemoryConfig
) -> str:
    """Send message with memory integration."""

    # 1. Get relevant memories
    relevant_memories = await memory_repo.get_relevant_memories(
        user_id=user_id,
        context=message,
        limit=memory_config.max_memories
    )

    # 2. Format memory context
    memory_context = "\n".join([
        f"- {mem.content}" for mem in relevant_memories
    ])

    # 3. Add memory context to system prompt
    system_prompt = f"""{DEFAULT_SYSTEM_PROMPT}

Current Context and Memories:
{memory_context if memory_context else "No relevant memories found."}"""

    # 4. Generate response with memory context
    response = await generate_response(
        messages=[{"role": "user", "content": message}],
        system_prompt=system_prompt
    )

    # 5. Save new memory (optional)
    if memory_config.should_save_memory():
        new_memory = Memory.create(
            user_id=user_id,
            content=f"User asked about: {message}\nAI responded: {response[:200]}..."
        )
        await memory_repo.save_memory(new_memory)

    return response
```

#### Save Memory Use Case
```python
from domain.models.memory import Memory
from domain.repositories.memory_repository import IMemoryRepository

class SaveMemoryUseCase:
    def __init__(self, memory_repo: IMemoryRepository):
        self.memory_repo = memory_repo

    async def execute(self, user_id: str, content: str) -> Memory:
        """Save a memory for user."""
        memory = Memory.create(user_id=user_id, content=content)
        return await self.memory_repo.save_memory(memory)
```

#### Get Relevant Memories Use Case
```python
from typing import List
from domain.repositories.memory_repository import IMemoryRepository

class GetRelevantMemoriesUseCase:
    def __init__(self, memory_repo: IMemoryRepository):
        self.memory_repo = memory_repo

    async def execute(
        self,
        user_id: str,
        context: str,
        limit: int = 5
    ) -> List[Memory]:
        """Get relevant memories based on context."""
        return await self.memory_repo.get_relevant_memories(
            user_id=user_id,
            context=context,
            limit=limit
        )
```

### Memory Tagging Strategy

#### Auto Tagging
```python
async def generate_tags_from_message(content: str) -> list[str]:
    """Generate tags from message content."""
    # Simple keyword-based tagging
    tags = []

    if "code" in content.lower():
        tags.append("code")

    if "python" in content.lower():
        tags.append("python")

    if "api" in content.lower():
        tags.append("api")

    return tags
```

### Error Handling

#### Memory Operations
```python
async def save_memory_safe(
    memory_repo: IMemoryRepository,
    memory: Memory
) -> bool:
    """Save memory with error handling."""
    try:
        await memory_repo.save_memory(memory)
        return True
    except Exception as e:
        logger.error(f"Failed to save memory: {e}")
        return False
```

### Testing Strategy
1. **Unit Tests**: Memory operations
2. **Integration Tests**: Mem0 API integration
3. **Memory Flow Tests**: Memory integration in message flow
4. **Config Tests**: Memory configuration options
5. **Edge Case Tests**: Empty memory, large memory, etc.

### Performance Considerations
- Use async operations for memory retrieval
- Cache memory results if needed
- Implement memory limits to prevent unbounded growth
- Use efficient similarity search for memory retrieval
- Consider memory TTL for cleanup

### Security Considerations
- [ ] Validate memory content
- [ ] No code execution from memory
- [ ] Sanitize memory output
- [ ] Handle memory injection attacks
- [ ] Secure memory storage
- [ ] Validate user_id in memory operations

## Success Metrics
- [ ] Memory can be enabled/disabled
- [ ] Memories are stored correctly
- [ ] Memories retrieved correctly based on context
- [ ] Memory limits enforced
- [ ] Memory integrated into message flow
- [ ] Memory operations don't slow response significantly

## Risk Assessment
**Low Risk**: Mem0 service complexity
**Mitigation**: Start with simple integration, add features gradually

**Low Risk**: Memory performance impact
**Mitigation**: Use async operations, caching, limits

**Low Risk**: Memory data size
**Mitigation**: Implement memory limits, cleanup

## Notes
- Start with memory disabled by default
- Integrate memory into message flow after basic chat works
- Keep memory implementation simple initially
- Focus on demonstrating clean architecture
- Can enhance with advanced features later
- Memory complements chat history, not replaces it
