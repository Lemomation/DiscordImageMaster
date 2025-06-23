# Discord AI Image Bot

## Overview

This is a Discord bot that integrates with Google's Gemini 2.0 Flash Preview model to generate images from text prompts. The bot provides a simple interface for Discord users to request AI-generated images using natural language descriptions.

## System Architecture

The application follows a modular client-server architecture:

- **Bot Layer**: Discord.py bot framework handling user interactions and command processing
- **AI Integration Layer**: Custom Gemini client wrapper for image generation
- **Rate Limiting Layer**: Built-in user request throttling to prevent API abuse
- **Configuration Layer**: Environment-based configuration management

## Key Components

### 1. Discord Bot (`bot.py`)
- **Purpose**: Main bot application handling Discord events and commands
- **Framework**: Discord.py library for Discord API integration
- **Features**: 
  - Asynchronous command processing
  - User rate limiting (5 requests per 5-minute window)
  - Error handling and logging
  - Message response management

### 2. Gemini Client (`gemini_client.py`)
- **Purpose**: Wrapper for Google Gemini API image generation
- **Model**: Uses `gemini-2.0-flash-preview-image-generation`
- **Features**:
  - Async/sync hybrid approach for API calls
  - Thread pool execution for blocking operations
  - Comprehensive error handling and logging
  - Returns image data as bytes for Discord attachment

### 3. Rate Limiter
- **Purpose**: Prevents API abuse and manages user request quotas
- **Implementation**: Time-window based deque system
- **Configuration**: 5 requests per 5-minute sliding window per user
- **Storage**: In-memory user request tracking

## Data Flow

1. **User Input**: Discord user sends message with image generation request
2. **Rate Check**: Bot validates user hasn't exceeded rate limits
3. **API Call**: Request forwarded to Gemini client for image generation
4. **Processing**: Gemini generates image based on text prompt
5. **Response**: Bot receives image bytes and sends as Discord attachment
6. **Cleanup**: Request logged for rate limiting purposes

## External Dependencies

### Core Dependencies
- **discord.py**: Discord API client library for bot functionality
- **google-genai**: Official Google Gemini API client
- **python-dotenv**: Environment variable management
- **sift-stack-py**: Additional utilities (specific usage unclear from codebase)

### API Services
- **Discord API**: Bot hosting and user interaction platform
- **Google Gemini API**: AI image generation service

### Environment Variables
- `DISCORD_TOKEN`: Bot authentication token from Discord Developer Portal
- `GEMINI_API_KEY`: API key for Google Gemini services

## Deployment Strategy

### Replit Configuration
- **Runtime**: Python 3.11 with Nix package management
- **Startup**: Automated dependency installation via uv package manager
- **Execution**: Direct Python script execution (`python bot.py`)
- **Workflow**: Parallel execution support with runButton integration

### Production Considerations
- Bot runs continuously to maintain Discord connection
- No persistent data storage required (stateless design)
- Rate limiting handled in memory (resets on restart)
- Environment variables required for authentication

### Scalability Limitations
- Single-instance deployment (no horizontal scaling)
- In-memory rate limiting (doesn't persist across restarts)
- No database backing for user data or request history

## Changelog
- June 23, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.