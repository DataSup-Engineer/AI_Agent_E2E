import json
import asyncio
from typing import AsyncGenerator
from google.adk.agents import BaseAgent
from google.adk.types import InvocationContext, Event
from google.adk.tools.google import ImagenTool

class CustomImageAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(name="custom_image_agent", **kwargs)
        self.imagen_tool = ImagenTool()

    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        # Extract user message
        user_msg = ctx.user_content.parts[0].text if ctx.user_content.parts else ""
        
        try:
            # Parse JSON input
            data = json.loads(user_msg)
            scene_description = data.get("scene_description", "")
            character_descriptions = data.get("character_descriptions", {})
        except Exception:
            # Fallback to plain text if not JSON
            scene_description = user_msg
            character_descriptions = {}

        # Build image prompt
        style_prefix = "Children's book cartoon illustration with bright vibrant colors, simple shapes, friendly characters."
        
        # Combine scene and character descriptions for consistency
        char_info = " ".join([f"{name}: {desc}" for name, desc in character_descriptions.items()])
        full_prompt = f"{style_prefix} {scene_description} {char_info}".strip()

        # Call ImagenTool directly
        try:
            # Note: The tool might require specific parameters like bucket name, which should be in env
            image_result = await self.imagen_tool.run(prompt=full_prompt)
            
            # Store results in session state
            ctx.session.state["image_result"] = {
                "status": "success",
                "image_url": image_result.url if hasattr(image_result, 'url') else str(image_result),
                "prompt": full_prompt
            }
            
            # Yield Event with results
            yield Event(text=f"Image generated successfully for: {scene_description}")
            
        except Exception as e:
            error_msg = f"Error generating image: {str(e)}"
            ctx.session.state["image_result"] = {
                "status": "error",
                "message": error_msg
            }
            yield Event(text=error_msg)

custom_image_agent = CustomImageAgent()
