import uuid
import requests
import json
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
from dataclasses import dataclass

class MistralAIError(Exception):
    """Base exception for all Mistral AI related errors."""
    pass

class AuthenticationError(MistralAIError):
    """Raised when authentication fails."""
    def __init__(self, message="Authentication failed. Check your cookies and chat ID."):
        self.message = message
        super().__init__(self.message)

class NetworkConnectionError(MistralAIError):
    """Raised when there are network connectivity issues."""
    def __init__(self, message="Network connection failed."):
        self.message = message
        super().__init__(self.message)

class RateLimitError(MistralAIError):
    """Raised when rate limits are exceeded."""
    def __init__(self, message="API rate limit exceeded. Please try again later."):
        self.message = message
        super().__init__(self.message)

class ModelUnavailableError(MistralAIError):
    """Raised when the selected model is not available."""
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.message = f"Model '{model_name}' is currently unavailable."
        super().__init__(self.message)

class InputValidationError(MistralAIError):
    """Raised when input does not meet required validation."""
    def __init__(self, message="Invalid input provided."):
        self.message = message
        super().__init__(self.message)

class ModelType(Enum):
    """Enumeration of available Mistral AI models."""
    LARGE_2 = "mistral-large-2407"
    CODESTRAL = "codestral"
    NEMO = "mistral-nemo"
    PIXTRAL = "pixtral-12b-2409"
    WEB_SEARCH = "pandragon"

@dataclass
class MistralAIClient:
    """
    A simplified client for interacting with Mistral AI.
    
    Attributes:
        cookies (str): Authentication cookies
        chat_id (str): Chat session identifier
        print_responses (bool, optional): Whether to print AI responses. Defaults to True.
    """
    cookies: str
    chat_id: str
    print_responses: bool = True

    def __post_init__(self):
        """Validate initialization parameters."""
        if not self.cookies or len(self.cookies.strip()) == 0:
            raise InputValidationError("Cookies cannot be empty")
        
        if not self.chat_id or len(self.chat_id.strip()) == 0:
            raise InputValidationError("Chat ID cannot be empty")

        self._headers = {"Cookie": self.cookies}

    def _validate_query(self, query: str):
        """
        Validate the input query.
        
        Args:
            query (str): Input query to validate
        
        Raises:
            InputValidationError: If query is invalid
        """
        if not query or len(query.strip()) == 0:
            raise InputValidationError("Query cannot be empty")
        
        if len(query) > 1000:  # Example max length check
            raise InputValidationError("Query is too long. Maximum 1000 characters allowed.")

    def chat(self, user_query: str, model: ModelType = ModelType.LARGE_2) -> str:
        """
        Send a message to Mistral AI and get a response.

        Args:
            user_query (str): Message to send to the AI
            model (ModelType, optional): AI model to use. Defaults to LARGE_2.

        Returns:
            str: AI's response

        Raises:
            InputValidationError: If query is invalid
            AuthenticationError: If authentication fails
            ModelUnavailableError: If selected model is not available
            NetworkConnectionError: If network issues occur
            RateLimitError: If API rate limits are exceeded
        """
        # Validate input
        self._validate_query(user_query)

        payload = {
            "chatId": self.chat_id,
            "messageId": str(uuid.uuid4()),
            "model": model.value,
            "messageInput": user_query,
            "mode": "append"
        }

        try:
            response = requests.post(
                "https://chat.mistral.ai/api/chat", 
                headers=self._headers, 
                data=json.dumps(payload), 
                stream=True,
                timeout=30  # 30 seconds timeout
            )

            # Handle specific error scenarios
            if response.status_code == 401:
                raise AuthenticationError()         
            if response.status_code == 404:
                raise AuthenticationError()
            if response.status_code == 500:
                raise AuthenticationError()
            elif response.status_code == 429:
                raise RateLimitError()
            elif response.status_code != 200:
                raise NetworkConnectionError(f"Unexpected error: {response.status_code}")

            complete_response = ''
            for line in response.iter_lines(decode_unicode=True, chunk_size=1):
                if line.startswith("0:"):
                    content = line[3:-1]
                    if self.print_responses:
                        print(content, end='', flush=True)
                    complete_response += content
            
            return complete_response.replace('\n', '')

        except requests.Timeout:
            raise NetworkConnectionError("Request timed out")
        except requests.ConnectionError:
            raise NetworkConnectionError("Could not connect to Mistral AI")
        except requests.RequestException as e:
            raise NetworkConnectionError(f"Network error: {e}")

    def web_search(self, query: str) -> str:
        """
        Perform a web search using Mistral AI.

        Args:
            query (str): Search query

        Returns:
            str: Search results

        Raises:
            Similar exceptions as chat method
        """
        # Validate input
        self._validate_query(query)

        payload = {
            'chatId': self.chat_id,
            'mode': 'append',
            'model': ModelType.WEB_SEARCH.value,
            'messageInput': query,
            'messageId': str(uuid.uuid4()),
            'features': ['beta-websearch'],
            'clientPromptData': {
                'currentDate': datetime.now().strftime('%Y-%m-%d'),
            },
        }

        try:
            response = requests.post(
                "https://chat.mistral.ai/api/chat", 
                headers=self._headers, 
                json=payload, 
                stream=True,
                timeout=30
            )

            # Handle specific error scenarios
            if response.status_code == 401:
                raise AuthenticationError()         
            if response.status_code == 404:
                raise AuthenticationError()
            if response.status_code == 500:
                raise AuthenticationError()
            elif response.status_code == 429:
                raise RateLimitError()
            elif response.status_code != 200:
                raise NetworkConnectionError(f"Unexpected error: {response.status_code}")

            complete_response = ''
            for line in response.iter_lines(decode_unicode=True, chunk_size=1):
                if line.startswith("0:"):
                    content = line[3:-1]
                    if self.print_responses:
                        print(content, end='', flush=True)
                    complete_response += content
            
            return complete_response.replace('\n', '')

        except requests.Timeout:
            raise NetworkConnectionError("Request timed out")
        except requests.ConnectionError:
            raise NetworkConnectionError("Could not connect to Mistral AI")
        except requests.RequestException as e:
            raise NetworkConnectionError(f"Network error: {e}")

# Simple example usage
if __name__ == "__main__":
    # Initialize the client
    try:
        client = MistralAIClient(
            cookies="your_authentication_cookies", 
            chat_id="your_chat_session_id",
            print_responses=True
        )

        # Chat with the AI
        response = client.chat("Hello, what can you do?")
        print("\nFull Response:", response)

        # Use a specific model
        code_response = client.chat(
            "Write a Python function to reverse a string", 
            model=ModelType.CODESTRAL
        )
        print("\nCode Response:", code_response)

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