#!/bin/bash
set -e

echo "🚀 Setting up Math Agent environment..."

# Make scripts executable
if [ -d "/workspaces/math-agent/src" ]; then
    chmod +x /workspaces/math-agent/src/*.sh 2>/dev/null || true
fi

# Install Python dependencies if requirements.txt exists
if [ -f "/workspaces/math-agent/requirements.txt" ]; then
    echo "📦 Installing Python dependencies..."
    pip install -r /workspaces/math-agent/requirements.txt
fi

# Create .env file from template if it doesn't exist
if [ ! -f "/workspaces/math-agent/.env" ] && [ -f "/workspaces/math-agent/.env.example" ]; then
    echo "📝 Creating .env file from template..."
    cp /workspaces/math-agent/.env.example /workspaces/math-agent/.env
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p /workspaces/math-agent/jobs

# Test LaTeX installation
echo "🧪 Testing LaTeX installation..."
if command -v pdflatex >/dev/null 2>&1; then
    echo "✅ LaTeX is installed"
else
    echo "❌ LaTeX installation failed"
fi

# Test cloudflared installation
echo "🧪 Testing cloudflared installation..."
if command -v cloudflared >/dev/null 2>&1; then
    echo "✅ cloudflared is installed"
    # Check authentication
    if [ -f "$HOME/.cloudflared/cert.pem" ] || cloudflared tunnel list >/dev/null 2>&1; then
        echo "✅ Cloudflared is authenticated"
    else
        echo "⚠️  Cloudflared needs authentication. Run: cloudflared tunnel login"
    fi
else
    echo "❌ cloudflared installation failed"
fi

# Test Claude CLI
echo "🧪 Testing Claude CLI..."
if command -v claude >/dev/null 2>&1; then
    echo "✅ Claude CLI is installed"
    # Check authentication
    if [ -f "$HOME/.claude/.credentials.json" ]; then
        echo "✅ Claude is authenticated"
    else
        echo "⚠️  Claude needs authentication. Run: claude (and follow the prompts)"
    fi
else
    echo "❌ Claude CLI installation failed"
fi

# Test Gemini CLI
echo "🧪 Testing Gemini CLI..."
if command -v gemini >/dev/null 2>&1; then
    echo "✅ Gemini CLI is installed"
    # Check for API key or Google auth
    if [ -n "$GEMINI_API_KEY" ]; then
        echo "✅ Gemini is configured with API key"
    elif [ -f "$HOME/.config/gcloud/application_default_credentials.json" ]; then
        echo "✅ Gemini is configured with Google Cloud credentials"
    else
        echo "⚠️  Gemini needs authentication. Either:"
        echo "    - Set GEMINI_API_KEY environment variable"
        echo "    - Or run: gemini (and login with Google account)"
        echo "    - Or run: gcloud auth application-default login"
    fi
else
    echo "❌ Gemini CLI installation failed"
fi

# Test GitHub CLI
echo "🧪 Testing GitHub CLI..."
if command -v gh >/dev/null 2>&1; then
    echo "✅ GitHub CLI is installed"
    # Check authentication
    if gh auth status >/dev/null 2>&1; then
        echo "✅ GitHub CLI is authenticated"
    else
        echo "⚠️  GitHub CLI needs authentication. Run: gh auth login"
    fi
else
    echo "❌ GitHub CLI installation failed"
fi

echo ""
echo "✨ Math Agent environment setup complete!"
echo ""
echo "Quick start:"
echo "  - Run './src/math-agent-simple.sh' to process a single exercise"
echo "  - Run 'python src/server.py' to start the web dashboard"
echo "  - Read CLAUDE.md for detailed documentation"