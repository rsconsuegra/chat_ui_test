# User Story: Simple Username Authentication

## Story Details
**ID**: US-02
**Priority**: P0 (Must Have)
**Status**: Not Started
**Estimated Effort**: 1 day

## Narrative
As a user, I want to identify myself with a username so that my chat history is preserved separately from others.

## Acceptance Criteria

### Functional Requirements
- [ ] Username input appears on app load
- [ ] No password required (simple identity only)
- [ ] Username persists in session
- [ ] Chat history filtered by username
- [ ] Duplicate username handling (simple conflict resolution)
- [ ] Username case-insensitive handling

### Technical Requirements
- [ ] Username validation (format, length, uniqueness)
- [ ] Session management for username
- [ ] Database table for user storage
- [ ] Foreign key relationships with chat messages
- [ ] Username sanitization to prevent SQL injection
- [ ] Proper error handling for username conflicts

### User Interface Requirements
- [ ] Clean username input dialog on startup
- [ ] Username field with validation feedback
- [ ] Session storage for username
- [ ] Clear indication of current user
- [ ] Logout/switch user option (if needed)

### Non-Functional Requirements
- [ ] Username validation enforces rules
- [ ] No authentication bypass attempts
- [ ] Secure storage of username in session
- [ ] Database queries use parameterized statements

## Out of Scope

### Explicitly Not Included
- [ ] Password authentication (simple username only)
- [ ] OAuth authentication
- [ ] Email verification
- [ ] Password reset functionality
- [ ] User registration (auto-generated usernames)
- [ ] User profiles with additional data
- [ ] Multi-device authentication
- [ ] Session timeout
- [ ] Remember me functionality

### Future Enhancements (Not Now)
- [ ] Password-based authentication
- [ ] Email verification system
- [ ] User registration flow
- [ ] Session management with timeout
- [ ] Multi-factor authentication
- [ ] User profile customization

## Test Scenarios

### Positive Scenarios
1. **First Login**: New user enters username
2. **Valid Username**: User enters valid username format
3. **Session Persistence**: Username persists across page refreshes
4. **Chat History**: User sees only their chat history
5. **Duplicate Username**: User with existing username can still access their history

### Negative Scenarios
1. **Empty Username**: User leaves username field empty
2. **Invalid Characters**: User enters special characters in username
3. **Too Long Username**: User enters very long username
4. **Whitespace Username**: User enters username with spaces
5. **Case Sensitivity**: Username handling with different cases
6. **SQL Injection**: User tries to inject SQL commands

### Edge Cases
1. **Unicode Characters**: Username with unicode characters
2. **Very Short Username**: Minimum length username
3. **Maximum Length Username**: Maximum length username
4. **Repeated Characters**: Username with repeated characters
5. **Special Characters**: Allowed special characters

## Dependencies

### Blockers
- [ ] Database schema defined (US-03: Chat History)

### Prerequisites
- SQLite database setup
- Basic application structure
- Chainlit session management

### Related User Stories
- US-03: Chat History Management (requires user association)
- US-01: Chat with Multiple Providers (optional but recommended)

## Implementation Notes

### Architecture Pattern
- Use repository pattern for user storage
- Domain layer defines user entity and repository interface
- Infrastructure layer implements SQLite repository
- Application layer manages session state

### File Structure
```
src/
├── domain/
│   ├── models/
│   │   └── user.py (User entity)
│   └── repositories/
│       └── user_repository.py (abstract interface)
├── application/
│   └── use_cases/
│       ├── register_user_use_case.py
│       └── login_user_use_case.py
├── infrastructure/
│   └── repositories/
│       └── sqlite_user_repository.py
└── adapters/
    └── auth/
        └── username_adapter.py
```

### Code Examples

#### User Entity (domain/models/user.py)
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    id: int
    username: str
    created_at: datetime
    updated_at: datetime

    @property
    def normalized_username(self) -> str:
        """Return username in lowercase for case-insensitive comparison."""
        return self.username.lower()
```

#### User Repository Interface (domain/repositories/user_repository.py)
```python
from abc import ABC, abstractmethod
from typing import Optional
from domain.models.user import User

class IUserRepository(ABC):
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        pass

    @abstractmethod
    async def create_user(self, username: str) -> User:
        """Create new user with given username."""
        pass

    @abstractmethod
    async def get_or_create_user(self, username: str) -> User:
        """Get existing user or create new one."""
        pass
```

#### SQLite User Repository (infrastructure/repositories/sqlite_user_repository.py)
```python
from typing import Optional
from domain.models.user import User
from domain.repositories.user_repository import IUserRepository

class SQLiteUserRepository(IUserRepository):
    def __init__(self, db_path: str = "./chat_history.db"):
        self.db_path = db_path

    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username (case-insensitive)."""
        # Implementation with parameterized query
        pass

    async def create_user(self, username: str) -> User:
        """Create new user."""
        # Implementation
        pass

    async def get_or_create_user(self, username: str) -> User:
        """Get existing user or create new one."""
        # Implementation with conflict resolution
        pass
```

### Username Validation Rules
- **Minimum length**: 3 characters
- **Maximum length**: 50 characters
- **Allowed characters**: Letters, numbers, underscores, hyphens
- **No special characters**: Only alphanumerics and _ -
- **No whitespace**: No spaces or tabs
- **Case-insensitive**: "User1" and "user1" treated as same
- **Normalized**: Stored in lowercase

### SQL Query Example
```sql
-- Get user by username (case-insensitive)
SELECT * FROM users WHERE LOWER(username) = LOWER(?) LIMIT 1;

-- Create new user
INSERT INTO users (username, created_at, updated_at)
VALUES (?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Conflict resolution (upsert)
INSERT INTO users (username, created_at, updated_at)
VALUES (?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT(username) DO NOTHING;
```

### Testing Strategy
1. **Unit Tests**: Repository implementations
2. **Integration Tests**: Database operations
3. **Validation Tests**: Username format validation
4. **Security Tests**: SQL injection prevention

### Security Considerations
- [ ] Use parameterized queries (no SQL injection)
- [ ] Sanitize user input
- [ ] No authentication bypass
- [ ] Secure session storage
- [ ] Limit username length to prevent buffer overflow
- [ ] Validate input format strictly

## Success Metrics
- [ ] Username input works correctly
- [ ] Session persists across refreshes
- [ ] Chat history filtered by username
- [ ] No authentication bypass
- [ ] No SQL injection vulnerabilities
- [ ] Case-insensitive username handling works

## Risk Assessment
**Medium Risk**: User input validation issues
**Mitigation**: Implement strict validation, parameterized queries, unit tests

**Low Risk**: Database connection issues
**Mitigation**: Connection pooling, error handling

## Notes
- Keep it simple - username only, no password
- Auto-create users if they don't exist
- Use case-insensitive comparison for user identification
- Store username in lowercase for consistency
- Provide clear error messages for invalid usernames
- Username serves as simple authentication mechanism for history
