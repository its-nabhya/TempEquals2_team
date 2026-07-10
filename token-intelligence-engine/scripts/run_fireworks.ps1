docker run --rm `
    -v "${PWD}\input:/input" `
    -v "${PWD}\output:/output" `
    -e PROVIDER=fireworks `
    -e FIREWORKS_API_KEY=$env:FIREWORKS_API_KEY `
    -e FIREWORKS_BASE_URL=https://api.fireworks.ai/inference/v1 `
    -e ALLOWED_MODELS=accounts/fireworks/models/minimax-m3 `
    token-intelligence-engine:v0.1