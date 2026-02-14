-- Migration ID: 002
-- Description: Add indexes for performance optimization
-- Created: 2025-01-01

CREATE INDEX IF NOT EXISTS idx_users_username
ON users (username);

CREATE INDEX IF NOT EXISTS idx_messages_user_id
ON chat_messages (user_id);

CREATE INDEX IF NOT EXISTS idx_messages_timestamp
ON chat_messages (timestamp DESC);
