"""LLM interface for communicating with language models."""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from enum import Enum

logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    """Supported LLM providers."""
    CLAUDE = "claude"
    GPT4 = "gpt4"
    LOCAL = "local"


class LLMInterface:
    """
    Interface for communicating with Large Language Models.

    Supports multiple providers (Claude, GPT-4) and handles the conversion
    of natural language commands to FreeCAD API calls.
    """

    # System prompt template for command translation
    SYSTEM_PROMPT = """You are an expert FreeCAD Python API translator. Your task is to convert natural language commands into valid FreeCAD Python API calls.

**FreeCAD API Guidelines:**

1. **Basic Shapes** (use Part module):
   - Box: Part.makeBox(length, width, height, [base_point], [direction])
   - Cylinder: Part.makeCylinder(radius, height, [base_point], [direction])
   - Sphere: Part.makeSphere(radius, [center], [direction], [angle1], [angle2], [angle3])
   - Cone: Part.makeCone(radius1, radius2, height, [base_point], [direction])

2. **BIM Elements** (use Arch module):
   - Wall: Arch.makeWall(baseobj=None, length=None, width=None, height=None, align="Center")
   - Structure: Arch.makeStructure(baseobj=None, length=None, width=None, height=None)
   - Window: Arch.makeWindow(baseobj=None, width=None, height=None)
   - Door: Arch.makeDoor(baseobj=None, width=None, height=None)
   - Floor: Arch.makeFloor(objectslist=[])
   - Building: Arch.makeBuilding(objectslist=[])
   - Site: Arch.makeSite(objectslist=[])

3. **Object Manipulation**:
   - Move: obj.Placement.Base = FreeCAD.Vector(x, y, z)
   - Rotate: obj.Placement.Rotation = FreeCAD.Rotation(axis, angle)
   - Scale: Draft.scale(obj, FreeCAD.Vector(scale_x, scale_y, scale_z))

4. **Properties**:
   - Color: obj.ViewObject.ShapeColor = (r, g, b)
   - Transparency: obj.ViewObject.Transparency = value  # 0-100
   - Visibility: obj.ViewObject.Visibility = True/False

**Important Notes:**
- All dimensions in FreeCAD are in millimeters by default
- Convert meters to millimeters (multiply by 1000)
- Always include necessary imports (FreeCAD, Part, Arch, Draft)
- Return ONLY valid Python code, no explanations
- Each operation should be a separate statement
- Use descriptive object names

**Output Format:**
Return a JSON object with this structure:
{
    "operations": [
        {
            "code": "# Python code here",
            "description": "Human-readable description",
            "type": "create|modify|delete|query",
            "affected_objects": ["object_names"]
        }
    ],
    "imports": ["FreeCAD", "Part", "Arch"],
    "requires_confirmation": false,
    "estimated_complexity": 1-10
}

**Examples:**

Input: "Create a wall 4 meters long, 3 meters high, 0.2 meters thick"
Output:
{
    "operations": [{
        "code": "wall = Arch.makeWall(length=4000, height=3000, width=200)",
        "description": "Create wall: 4m x 3m x 0.2m",
        "type": "create",
        "affected_objects": ["wall"]
    }],
    "imports": ["FreeCAD", "Arch"],
    "requires_confirmation": false,
    "estimated_complexity": 2
}

Input: "Delete all walls"
Output:
{
    "operations": [{
        "code": "walls = [obj for obj in FreeCAD.ActiveDocument.Objects if obj.TypeId == 'Arch::Wall']\\nfor wall in walls:\\n    FreeCAD.ActiveDocument.removeObject(wall.Name)",
        "description": "Delete all walls in document",
        "type": "delete",
        "affected_objects": ["all_walls"]
    }],
    "imports": ["FreeCAD"],
    "requires_confirmation": true,
    "estimated_complexity": 5
}

Now translate the following command:"""

    def __init__(self, provider: LLMProvider = LLMProvider.CLAUDE, api_key: Optional[str] = None):
        """
        Initialize LLM interface.

        Args:
            provider: LLM provider to use
            api_key: API key for the provider (or set via environment variables)
        """
        self.provider = provider
        self.api_key = api_key or self._get_api_key()
        logger.info(f"LLM interface initialized with provider: {provider.value}")

    def _get_api_key(self) -> Optional[str]:
        """Get API key from environment variables."""
        if self.provider == LLMProvider.CLAUDE:
            return os.getenv('ANTHROPIC_API_KEY')
        elif self.provider == LLMProvider.GPT4:
            return os.getenv('OPENAI_API_KEY')
        return None

    def translate_command(self, natural_language_command: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Translate natural language command to FreeCAD API calls.

        Args:
            natural_language_command: User's natural language command
            context: Optional context about the current document state

        Returns:
            Dictionary containing operations, imports, and metadata
        """
        logger.info(f"Translating command: {natural_language_command}")

        # Build the full prompt
        user_prompt = natural_language_command
        if context:
            user_prompt = f"Context: {json.dumps(context, indent=2)}\n\nCommand: {natural_language_command}"

        try:
            if self.provider == LLMProvider.CLAUDE:
                response = self._call_claude(user_prompt)
            elif self.provider == LLMProvider.GPT4:
                response = self._call_gpt4(user_prompt)
            else:
                response = self._mock_response(natural_language_command)

            return response

        except Exception as e:
            logger.error(f"Error translating command: {e}")
            return {
                'error': str(e),
                'operations': [],
                'imports': [],
                'requires_confirmation': False,
                'estimated_complexity': 0
            }

    def _call_claude(self, user_prompt: str) -> Dict[str, Any]:
        """
        Call Claude API for command translation.

        Args:
            user_prompt: User's prompt

        Returns:
            Parsed response
        """
        try:
            import requests

            if not self.api_key:
                raise ValueError("ANTHROPIC_API_KEY not set")

            headers = {
                'x-api-key': self.api_key,
                'anthropic-version': '2023-06-01',
                'content-type': 'application/json'
            }

            data = {
                'model': 'claude-3-5-sonnet-20241022',
                'max_tokens': 2048,
                'temperature': 0.2,
                'system': self.SYSTEM_PROMPT,
                'messages': [
                    {'role': 'user', 'content': user_prompt}
                ]
            }

            response = requests.post(
                'https://api.anthropic.com/v1/messages',
                headers=headers,
                json=data,
                timeout=30
            )

            response.raise_for_status()
            result = response.json()

            # Extract the response content
            content = result['content'][0]['text']

            # Parse JSON response
            return self._parse_llm_response(content)

        except ImportError:
            logger.warning("requests library not installed. Install with: pip install requests")
            return self._mock_response(user_prompt)
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise

    def _call_gpt4(self, user_prompt: str) -> Dict[str, Any]:
        """
        Call GPT-4 API for command translation.

        Args:
            user_prompt: User's prompt

        Returns:
            Parsed response
        """
        try:
            import requests

            if not self.api_key:
                raise ValueError("OPENAI_API_KEY not set")

            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }

            data = {
                'model': 'gpt-4-turbo-preview',
                'messages': [
                    {'role': 'system', 'content': self.SYSTEM_PROMPT},
                    {'role': 'user', 'content': user_prompt}
                ],
                'temperature': 0.2,
                'response_format': {'type': 'json_object'}
            }

            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=30
            )

            response.raise_for_status()
            result = response.json()

            # Extract the response content
            content = result['choices'][0]['message']['content']

            # Parse JSON response
            return self._parse_llm_response(content)

        except ImportError:
            logger.warning("requests library not installed. Install with: pip install requests")
            return self._mock_response(user_prompt)
        except Exception as e:
            logger.error(f"GPT-4 API error: {e}")
            raise

    def _parse_llm_response(self, content: str) -> Dict[str, Any]:
        """
        Parse LLM response into structured format.

        Args:
            content: LLM response content

        Returns:
            Parsed dictionary
        """
        try:
            # Try to extract JSON from the response
            # Sometimes LLMs wrap JSON in markdown code blocks
            if '```json' in content:
                start = content.find('```json') + 7
                end = content.find('```', start)
                content = content[start:end].strip()
            elif '```' in content:
                start = content.find('```') + 3
                end = content.find('```', start)
                content = content[start:end].strip()

            return json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            logger.debug(f"Response content: {content}")

            # Return a default error structure
            return {
                'error': 'Failed to parse LLM response',
                'raw_response': content,
                'operations': [],
                'imports': [],
                'requires_confirmation': False,
                'estimated_complexity': 0
            }

    def _mock_response(self, command: str) -> Dict[str, Any]:
        """
        Generate a mock response for testing without API access.

        Args:
            command: User command

        Returns:
            Mock response
        """
        logger.warning("Using mock LLM response")

        # Simple pattern matching for common commands
        command_lower = command.lower()

        if 'wall' in command_lower and 'create' in command_lower:
            return {
                'operations': [{
                    'code': 'wall = Arch.makeWall(length=4000, height=3000, width=200)',
                    'description': 'Create a wall (mock response)',
                    'type': 'create',
                    'affected_objects': ['wall']
                }],
                'imports': ['FreeCAD', 'Arch'],
                'requires_confirmation': False,
                'estimated_complexity': 2
            }
        elif 'delete' in command_lower:
            return {
                'operations': [{
                    'code': '# Mock delete operation',
                    'description': 'Delete operation (mock response)',
                    'type': 'delete',
                    'affected_objects': []
                }],
                'imports': ['FreeCAD'],
                'requires_confirmation': True,
                'estimated_complexity': 5
            }
        else:
            return {
                'operations': [],
                'imports': [],
                'requires_confirmation': False,
                'estimated_complexity': 0,
                'note': 'Mock response - API not available'
            }

    def validate_response(self, response: Dict[str, Any]) -> bool:
        """
        Validate that the LLM response has the expected structure.

        Args:
            response: LLM response

        Returns:
            True if valid
        """
        required_fields = ['operations', 'imports', 'requires_confirmation', 'estimated_complexity']

        if not all(field in response for field in required_fields):
            logger.error("LLM response missing required fields")
            return False

        if not isinstance(response['operations'], list):
            logger.error("Operations must be a list")
            return False

        for op in response['operations']:
            if not all(key in op for key in ['code', 'description', 'type', 'affected_objects']):
                logger.error("Operation missing required fields")
                return False

        return True
