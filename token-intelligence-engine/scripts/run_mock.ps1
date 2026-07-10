docker run --rm `
    -v "${PWD}\input:/input" `
    -v "${PWD}\output:/output" `
    -e PROVIDER=mock `
    -e ALLOWED_MODELS=mock-model `
    token-intelligence-engine:v0.1