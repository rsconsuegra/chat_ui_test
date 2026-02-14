# User Story: Chat History Management

## Story Details
**ID**: US-03
**Priority**: P0 (Must Have)
**Status**: Not Started
**Estimated Effort**: 2 days

## Narrative
As a user, I want to see my previous conversations so that I can reference past discussions.

## Acceptance Criteria

### Functional Requirements
- [ ] Chat history stored per username
- [ ] History viewable in Chainlit UI
- [ ] Can continue previous conversations
- [ ] History persists across sessions
- [ ] Simple SQLite storage for learning purposes
- [ ] Chat history can be cleared (optional feature)

### Technical Requirements
- [ ] Database schema for chat messages
- [ ] Repository pattern for message storage
- [ ] Foreign key relationship with users table
- [ ] Message indexing for performance
- [ ] Efficient query for message retrieval
- [ ] Proper cleanup of old messages (optional)

### User Interface Requirements
- [ ] Chat history view in Chainlit
- [ ] List of past conversations
- [ ] Option to view conversation details
- [ ] Option to continue conversation
- [ ] Option to clear history
- [ ] Clear feedback when history is cleared

### Non-Functional Requirements
- [ ] Messages retrieved in correct order (chronological)
- [ ] History loads within 3 seconds
- [ ] Message content preserved exactly
- [ ] No data corruption
- [ ] Proper transaction handling for writes

## Out of Scope

### Explicitly Not Included
- [ ] Message search functionality
- [ ] Message filtering by date
- [ ] Message export to file
- [ ] Message sharing
- [ ] Conversation tagging/categorization
- [ ] Message editing or deletion
- [ ] Message notifications
- [ ] Real-time chat history updates
- [ ] Collaborative chat history
- [ ] Chat history encryption

### Future Enhancements (Not Now)
- [ ] Advanced search and filtering
- [ ] Message export formats (JSON, CSV, etc.)
- [ ] Conversation categorization
- [ ] Message editing and deletion
- [ ] Conversation tagging
- [ ] Message notifications
- [ ] Export to PDF
- [ ] Advanced analytics on chat history

## Test Scenarios

### Positive Scenarios
1. **New Conversation**: User starts new conversation
2. **View History**: User can view list of past conversations
3. **Continue Conversation**: User can continue a past conversation
4. **Persistence**: User sees previous messages after restart
5. **Clear History**: User can clear their chat history
6. **Multiple Users**: Different users see different histories

### Negative Scenarios
1. **No History**: User with no chat history shows empty state
2. **Clear History**: Clearing history removes all messages
3. **Empty Message**: No message stored when message is empty
4. **Large History**: Many messages loaded correctly
5. **Restart Session**: Chat history available after app restart

### Edge Cases
1. **Special Characters**: Messages with special characters
2. **Unicode**: Messages with unicode characters
3. **Empty User**: User without any messages
4. **Very Long Message**: Messages longer than database field
5. **Concurrent Messages**: Multiple messages sent rapidly
6. **Date Formatting**: Messages from different times

## Dependencies

### Blockers
- [ ] User authentication (US-02) - for user association
- [ ] Database schema design

### Prerequisites
- SQLite database setup
- User entity defined
- Basic application structure

### Related User Stories
- US-02: Simple Username Authentication (requires user association)
- US-01: Chat with Multiple Providers (uses chat messages)
- US-05: Optional Memory Integration (optional, can reference context)

## Implementation Notes

### Architecture Pattern
- Use repository pattern for message storage
- Domain layer defines message entity and repository interface
- Infrastructure layer implements SQLite repository
- Application layer provides use cases for history operations

### File Structure
```
src/
├── domain/
│   ├── models/
│   │   ├── chat_message.py (ChatMessage entity)
│   │   └── user.py (User entity)
│   └── repositories/
│       ├── message_repository.py (abstract interface)
│       └── user_repository.py (abstract interface)
├── application/
│   └── use_cases/
│       ├── load_history_use_case.py
│       ├── get_messages_by_conversation.py
│       └── clear_history_use_case.py
├── infrastructure/
│   └── repositories/
│       └── sqlite_message_repository.py
└── adapters/
    └── chainlit/
        ├── chat_history_adapter.py
        └── conversation_view.py
```

### Code Examples

#### ChatMessage Entity (domain/models/chat_message.py)
```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

class MessageRole(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

@dataclass
class ChatMessage:
    id: int
    user_id: int
    provider: str
    role: MessageRole
    content: str
    timestamp: datetime

    @classmethod
    def create(
        cls,
        user_id: int,
        provider: str,
        role: MessageRole,
        content: str
    ) -> "ChatMessage":
        """Create a new chat message."""
        return cls(
            id=0,  # Will be set by repository
            user_id=user_id,
            provider=provider,
            role=role,
            content=content,
            timestamp=datetime.now()
        )
```

#### Message Repository Interface (domain/repositories/message_repository.py)
```python
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.chat_message import ChatMessage
from domain.models.user import User

class IMessageRepository(ABC):
    @abstractmethod
    async def save_message(self, message: ChatMessage) -> ChatMessage:
        """Save a new chat message."""
        pass

    @abstractmethod
    async def get_messages_by_user(
        self,
        user_id: int,
        limit: int = 100
    ) -> List[ChatMessage]:
        """Get all messages for a user."""
        pass

    @abstractmethod
    async def get_messages_by_conversation(
        self,
        user_id: int,
        start_timestamp: Optional[datetime] = None,
        limit: int = 100
    ) -> List[ChatMessage]:
        """Get messages for a specific conversation."""
        pass

    @abstractmethod
    async def clear_user_history(self, user_id: int) -> int:
        """Clear all messages for a user."""
        pass

    @abstractmethod
    async def get_message_count(self, user_id: int) -> int:
        """Get message count for a user."""
        pass
```

#### SQLite Message Repository (infrastructure/repositories/sqlite_message_repository.py)
```python
from typing import List, Optional
from domain.models.chat_message import ChatMessage, MessageRole
from domain.repositories.message_repository import IMessageRepository
from domain.models.user import User

class SQLiteMessageRepository(IMessageRepository):
    def __init__(self, db_path: str = "./chat_history.db"):
        self.db_path = db_path

    async def save_message(self, message: ChatMessage) -> ChatMessage:
        """Save a new chat message."""
        # Implementation with INSERT ... ON CONFLICT
        pass

    async def get_messages_by_user(
        self,
        user_id: int,
        limit: int = 100
    ) -> List[ChatMessage]:
        """Get all messages for a user."""
        # Implementation with ORDER BY timestamp DESC LIMIT
        pass

    async def get_messages_by_conversation(
        self,
        user_id: int,
        start_timestamp: Optional[datetime] = None,
        limit: int = 100
    ) -> List[ChatMessage]:
        """Get messages for a specific conversation."""
        # Implementation with filtered query
        pass

    async def clear_user_history(self, user_id: int) -> int:
        """Clear all messages for a user."""
        # Implementation with DELETE WHERE
        pass

    async def get_message_count(self, user_id: int) -> int:
        """Get message count for a user."""
        # Implementation with COUNT query
        pass
```

### Database Schema
```sql
-- Chat messages table
CREATE TABLE chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    provider TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX idx_chat_messages_user_id ON chat_messages(user_id);
CREATE INDEX idx_chat_messages_timestamp ON chat_messages(timestamp);

-- Trigger to update updated_at (optional, if needed)
-- CREATE TRIGGER update_timestamp
-- BEFORE UPDATE ON chat_messages
-- BEGIN
--     UPDATE chat_messages SET updated_at = CURRENT_TIMESTAMP;
-- END;
```

### Message Storage Strategy
- **Table**: `chat_messages`
- **Fields**: id, user_id, provider, role, content, timestamp
- **Relationship**: Many-to-one with users (CASCADE delete)
- **Indexing**: user_id and timestamp for efficient queries
- **Ordering**: Messages sorted by timestamp (newest first)

### Use Case Examples

#### Load History Use Case (application/use_cases/load_history_use_case.py)
```python
from typing import List
from domain.repositories.message_repository import IMessageRepository
from domain.models.user import User
from domain.models.chat_message import ChatMessage

class LoadHistoryUseCase:
    def __init__(self, message_repo: IMessageRepository):
        self.message_repo = message_repo

    async def execute(self, user: User, limit: int = 100) -> List[ChatMessage]:
        """Load chat history for user."""
        return await self.message_repo.get_messages_by_user(
            user.id,
            limit=limit
        )
```

#### Get Messages by Conversation Use Case
```python
class GetMessagesByConversationUseCase:
    def __init__(self, message_repo: IMessageRepository):
        self.message_repo = message_repo

    async def execute(
        self,
        user: User,
        start_timestamp: Optional[datetime] = None
    ) -> List[ChatMessage]:
        """Get messages for a specific conversation."""
        return await self.message_repo.get_messages_by_conversation(
            user.id,
            start_timestamp=start_timestamp
        )
```

### Testing Strategy
1. **Unit Tests**: Repository implementations
2. **Integration Tests**: Database operations
3. **Persistence Tests**: Message retention after restart
4. **Performance Tests**: Large history loading
5. **Edge Case Tests**: Empty history, special characters, etc.

### Performance Considerations
- Use indexes on user_id and timestamp
- Implement pagination (limit/offset)
- Consider using "last message timestamp" for conversations
- Use async operations for database queries
- Implement query caching if needed

### Security Considerations
- [ ] Use parameterized queries (no SQL injection)
- [ ] Only allow access to own messages
- [ ] Validate message content length
- [ ] Sanitize output for UI
- [ ] Handle potential database errors gracefully

## Success Metrics
- [ ] History loads within 3 seconds
- [ ] Messages persist across sessions
- [ ] Multiple users see different histories
- [ ] History can be cleared
- [ ] No data corruption
- [ ] No SQL injection vulnerabilities
- [ ] Performance acceptable with large histories

## Risk Assessment
**Medium Risk**: Database performance with large datasets
**Mitigation**: Indexes, pagination, query optimization

**Low Risk**: Database corruption
**Mitigation**: Proper transaction handling, WAL mode

**Low Risk**: Memory usage with large history
**Mitigation**: Load with limit, lazy loading

## Notes
- Start with simple list of conversations (just timestamps)
- Load full message history on demand
- Implement conversation view (list of messages in conversation)
- Consider adding message search in future
- Clear history should ask for confirmation
- Provide option to export conversation
