# Mistral AI Python Client

## Overview

This is a Python client library for interacting with the Mistral AI chat and web search services, designed for educational and learning purposes.

## 🚨 Important Disclaimer

**EDUCATIONAL PURPOSE ONLY**

This software is strictly for educational and research purposes. It is intended to demonstrate programming concepts, API interaction techniques, and Python development practices.

**IMPORTANT WARNINGS:**
- This library is NOT officially supported by Mistral AI
- Do NOT use this for any malicious, unauthorized, or commercial purposes
- Respect Mistral AI's Terms of Service and Usage Policies
- Unauthorized or abusive API access may result in your account being banned

## Features

- Simple and intuitive Mistral AI interaction
- Support for multiple AI models
- Web search capabilities
- Comprehensive error handling
- Type-safe implementation

## Prerequisites

- Python 3.8+
- `requests` library
- Valid Mistral AI authentication credentials

## Installation

```bash
pip install requests
```

## Quick Start

### Basic Chat Interaction

```python
# Simple example usage
if __name__ == "__main__":
    # Initialize the client
    try:
        client = MistralAIClient(
            cookies="your_authentication_cookies", 
            chat_id="your_chat_session_id"
        )

        # Chat with the AI
        response = client.chat("Hello, what can you do?")
        print("\nFull Response:", response)

        # Use a specific model
        code_response = client.chat(
            "Write a Python function to reverse a string", 
            model=ModelType.CODESTRAL
        )

        # Perform a web search
        search_results = client.web_search("Latest AI developments")
        print("\nSearch Results:", search_results)

    except AuthenticationError as e:
        print(f"Authentication failed: {e}")
    except NetworkConnectionError as e:
        print(f"Network error: {e}")
    except RateLimitError as e:
        print(f"Rate limit exceeded: {e}")
    except ModelUnavailableError as e:
        print(f"Model error: {e}")
    except InputValidationError as e:
        print(f"Input error: {e}")
    except MistralAIError as e:
        print(f"Unexpected Mistral AI error: {e}")
```

## Available Models

- `LARGE_2`: General-purpose large language model
- `CODESTRAL`: Specialized in code generation
- `NEMO`: Another variant of Mistral AI model
- `PIXTRAL`: Specialized model
- `WEB_SEARCH`: Web search model

## Error Handling

The library provides comprehensive error handling:

- `AuthenticationError`: Authentication failures
- `NetworkConnectionError`: Network issues
- `RateLimitError`: API rate limit exceeded
- `ModelUnavailableError`: Model-specific errors
- `InputValidationError`: Invalid input

### Example Error Handling

```python
try:
    response = client.chat("Hello")
except AuthenticationError as e:
    print(f"Login failed: {e}")
except NetworkConnectionError as e:
    print(f"Network error: {e}")
```

## Ethical Use Guidelines

1. Always obtain proper authorization
2. Respect API usage limits
3. Do not generate harmful content
4. Comply with Mistral AI's terms of service
5. Use responsibly and ethically

## Acknowledgments

- Mistral AI for their innovative technology
- Python community for continuous support

## Reporting Issues

If you encounter any issues or have suggestions:
- Check existing issues
- Provide detailed information
- Be respectful and constructive

---

**Note**: This is a community project and is not officially affiliated with or endorsed by Mistral AI.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contact
For questions or support, please open an issue or reach out to the maintainer.

## Contributing

Contributions are welcome! Please submit pull requests or open issues on the project repository.
