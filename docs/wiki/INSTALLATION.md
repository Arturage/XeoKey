# Installation Guide

This guide will walk you through installing and setting up XeoKey on your system.

## Prerequisites

- **[Bun](https://bun.sh)** - JavaScript runtime (v1.3.4 or later)
- **[MongoDB](https://www.mongodb.com/)** - Database server (optional, but recommended)

## Step-by-Step Installation

### 1. Clone or Download the Repository

```bash
cd XeoKey
```

### 2. Install Dependencies

```bash
bun install
```

Dependencies will be automatically installed by Bun.

### 3. Set Up Environment Variables

Create a `.env` file in the root directory (optional, but recommended for production):

```env
# Server Configuration
PORT=3000
NODE_ENV=production

# Database Configuration
MONGODB_URI=mongodb://localhost:27017

# Security (REQUIRED for production)
SESSION_SECRET=your-super-secret-session-key-at-least-32-characters-long
ENCRYPTION_KEY=your-super-secret-encryption-key-for-password-storage
```

**Important Security Notes:**
- `SESSION_SECRET`: Must be at least 32 characters long. Used for session cookie signing.
- `ENCRYPTION_KEY`: Used to encrypt passwords. Must be set in production.
- Generate strong random keys for production use.

For detailed information about all environment variables, see the [Configuration Guide](./CONFIGURATION.md).

### 4. Start MongoDB (if using local database)

**On Windows:**
- If installed as a service, MongoDB should start automatically
- Or use MongoDB Compass
- Or start manually from the command line

**On Linux/Mac:**
```bash
mongod
```

## Running the Server

### Development Mode (with auto-reload):
```bash
bun run dev
```

### Production Mode:
```bash
bun run start
```

**On Windows:**
```bash
Start.bat
```

The server will start on `http://localhost:3000` by default (or the port specified in `PORT` environment variable).

## First-Time Setup

1. **Start the server** (see above)

2. **Navigate to** `http://localhost:3000`

3. **Register a new account:**
   - Click "Register" or navigate to `/register`
   - Create your first user account
   - Username requirements:
     - 3-20 characters
     - Letters, numbers, underscores, and hyphens only
   - Password requirements:
     - Minimum 8 characters
     - At least one letter and one number

4. **Login** with your new account

5. **Add your first password:**
   - Click "+ Add Password" or navigate to `/passwords/add`
   - Fill in the website, username, email (optional), password, and notes (optional)
   - Click "Save Password"

## Next Steps

- Read the [Configuration Guide](./CONFIGURATION.md) for detailed environment variable setup
- Check the [Security Guide](./SECURITY.md) for security best practices
- Review the [API Documentation](./API.md) for integration details
- See [Troubleshooting](./TROUBLESHOOTING.md) if you encounter any issues

