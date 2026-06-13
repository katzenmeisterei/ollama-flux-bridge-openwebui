"""
title: Ollama & Flux Bridge
author: LocalDev
author_url: https://github.com/yourusername
version: 1.0.0
description: Bridges Open WebUI with Ollama's experimental Flux image models (like x/flux2-klein:4b). Disables streaming to guarantee rock-solid stability against Docker network timeouts and automatically parses the correct image payloads.
"""

import json
import requests
from pydantic import BaseModel, Field
from typing import List, Union, Generator, Iterator

class Pipe:
    # This class creates a clean configuration menu in the Open WebUI admin panel
    class Valves(BaseModel):
        OLLAMA_URL: str = Field(
            default="http://host.docker.internal:11434/api/generate",
            description="The primary API URL of your local Ollama server."
        )
        ALT_OLLAMA_URL: str = Field(
            default="http://172.17.0.1:11434/api/generate",
            description="Automatic fallback IP for the Docker bridge if the hostname does not resolve."
        )
        MODEL_NAME: str = Field(
            default="x/flux2-klein:4b",
            description="The exact name of the installed Flux model in Ollama."
        )
        TIMEOUT: int = Field(
            default=60,
            description="Timeout in seconds. Gives your hardware enough time to calculate the image in one go."
        )

    def __init__(self):
        self.type = "manifold"
        self.name = "Ollama & Flux Bridge"
        self.valves = self.Valves()

    def pipe(self, body: dict) -> str:
        # Extract chat history from the Open WebUI request
        messages = body.get("messages", [])
        if not messages:
            return "Error: No message found in the chat history."
            
        # Use the latest user input as the image prompt
        user_message = messages[-1].get("content", "")
        
        # Prepare payload. CRITICAL: stream=False prevents connection drops within Docker!
        payload = {
            "model": self.valves.MODEL_NAME,
            "prompt": user_message,
            "stream": False
        }
        
        try:
            # Connection attempt 1 (Standard Mac/Windows Docker Host)
            try:
                response = requests.post(self.valves.OLLAMA_URL, json=payload, timeout=self.valves.TIMEOUT)
                response.raise_for_status()
            except requests.exceptions.ConnectionError:
                # Connection attempt 2 (Direct Docker-Bridge IP as failover)
                response = requests.post(self.valves.ALT_OLLAMA_URL, json=payload, timeout=self.valves.TIMEOUT)
                response.raise_for_status()

            data = response.json()
            raw_base64 = ""

            # Search through all known JSON structures where Ollama might hide the image data
            if "images" in data and isinstance(data["images"], list) and len(data["images"]) > 0:
                raw_base64 = data["images"][0].strip()
            elif "response" in data and data["response"].strip():
                raw_base64 = data["response"].strip()
            elif "image" in data and data["image"].strip():
                raw_base64 = data["image"].strip()

            if not raw_base64:
                keys_found = list(data.keys())
                return f"Error: No image data found. Ollama responded unexpectedly with the following JSON fields: {keys_found}"

            # Clean the Base64 string from disruptive newlines
            raw_base64 = raw_base64.replace("\n", "").replace("\r", "").strip()

            # Add the correct MIME header for proper image rendering in the browser
            if not raw_base64.startswith("data:image"):
                base64_image = f"data:image/png;base64,{raw_base64}"
            else:
                base64_image = raw_base64
                
            # Return the finished image as native Markdown back to the chat
            return f"\n\n![Generated Image]({base64_image})\n\n*Asset generated via **Ollama & Flux Bridge** ({self.valves.MODEL_NAME})*"
            
        except Exception as e:
            return f"**Ollama & Flux Bridge - Error:** {str(e)}"
