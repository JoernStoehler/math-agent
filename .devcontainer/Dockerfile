FROM mcr.microsoft.com/devcontainers/universal:2

# Install additional tools as root
USER root

# Install base dependencies
RUN apt-get update && apt-get install -y \
    ripgrep \
    jq \
    tree \
    direnv \
    curl \
    wget \
    # LaTeX dependencies
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-lang-german \
    # Python dependencies
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Install GitHub CLI
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt-get update \
    && apt-get install -y gh \
    && rm -rf /var/lib/apt/lists/*

# Install cloudflared
RUN wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb \
    && dpkg -i cloudflared-linux-amd64.deb \
    && rm cloudflared-linux-amd64.deb

# Switch to codespace user for user installations
USER codespace

# Install uv (Python package manager) for the user
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Claude Code CLI globally using existing npm
RUN npm install -g @anthropic-ai/claude-code

# Install Gemini CLI globally using existing npm
RUN npm install -g @google/gemini-cli

# Configure direnv hook for bash and zsh
RUN echo 'eval "$(direnv hook bash)"' >> ~/.bashrc \
    && echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc

# Ensure uv is in PATH
ENV PATH="/home/codespace/.cargo/bin:${PATH}"

# Add src directory to PATH for math-agent scripts
ENV PATH="/workspaces/math-agent/src:${PATH}"