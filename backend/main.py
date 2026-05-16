import os
import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from dotenv import load_dotenv
from backend.story_agent.agent import story_agent
from backend.story_image_agent.agent import custom_image_agent
from google.adk.types import InvocationContext, Content, Part

load_dotenv()

app = FastAPI(title="StoryGen AI API")

@app.websocket("/ws/generate")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive keywords from frontend
            data = await websocket.receive_text()
            keywords = data.strip()
            
            if not keywords:
                continue

            await websocket.send_text(json.dumps({"status": "starting", "message": "Generating story..."}))

            # 1. Generate Story
            story_context = InvocationContext(
                user_content=Content(parts=[Part(text=keywords)]),
                session_id="story-session"
            )
            
            full_story_json = ""
            async for event in story_agent.run_async(story_context):
                if hasattr(event, 'text'):
                    full_story_json += event.text
            
            try:
                story_data = json.loads(full_story_json)
                await websocket.send_text(json.dumps({"status": "story_done", "data": story_data}))
            except Exception as e:
                await websocket.send_text(json.dumps({"status": "error", "message": f"Failed to parse story: {str(e)}"}))
                continue

            # 2. Generate Images for each scene
            scenes = story_data.get("scenes", [])
            characters = {c["name"]: c["description"] for c in story_data.get("main_characters", [])}
            
            for scene in scenes:
                scene_index = scene.get("index")
                await websocket.send_text(json.dumps({"status": "generating_image", "scene": scene_index}))
                
                image_input = {
                    "scene_description": scene.get("description"),
                    "character_descriptions": characters
                }
                
                image_context = InvocationContext(
                    user_content=Content(parts=[Part(text=json.dumps(image_input))]),
                    session_id=f"image-session-{scene_index}"
                )
                
                async for event in custom_image_agent.run_async(image_context):
                    pass # CustomImageAgent yields status events
                
                # Retrieve result from session state
                image_result = image_context.session.state.get("image_result", {})
                await websocket.send_text(json.dumps({
                    "status": "image_done", 
                    "scene": scene_index, 
                    "image_url": image_result.get("image_url"),
                    "error": image_result.get("message") if image_result.get("status") == "error" else None
                }))

            await websocket.send_text(json.dumps({"status": "complete", "message": "All scenes generated!"}))

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
        try:
            await websocket.send_text(json.dumps({"status": "error", "message": str(e)}))
        except:
            pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
