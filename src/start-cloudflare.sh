#!/bin/bash

# Start Cloudflare tunnel for math-agent.joernstoehler.com
# Make sure you've already run: cloudflared tunnel login

echo "Starting Cloudflare tunnel for math-agent.joernstoehler.com..."
echo "Make sure server.py is running on port 5001 first!"
echo ""

# Check if tunnel exists, create if not
if ! cloudflared tunnel list | grep -q "math-agent"; then
    echo "Creating tunnel 'math-agent'..."
    cloudflared tunnel create math-agent
    echo ""
fi

# Check if DNS route exists, create if not
if ! cloudflared tunnel route dns list | grep -q "math-agent.joernstoehler.com"; then
    echo "Creating DNS route for math-agent.joernstoehler.com..."
    cloudflared tunnel route dns math-agent math-agent.joernstoehler.com
    echo ""
fi

echo "Starting tunnel..."
echo "Your app will be available at: https://math-agent.joernstoehler.com"
echo ""
echo "Press Ctrl+C to stop the tunnel"
echo ""

# Run the tunnel
cloudflared tunnel run --url http://localhost:5001 --protocol http2 math-agent