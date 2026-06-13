# ollama-flux-bridge-openwebui
Ollama &amp; Flux Bridge - A reliable Open WebUI function connecting your chat interface with local Ollama Flux image models. By disabling streaming, it eliminates Docker network timeouts and cleanly parses the JSON payload. Optimized for fast, uninterrupted local image generation and seamless creative workflows.

Tested Environment & Performance

    Hardware: Apple Mac (Apple Silicon / M5-Series)

    Model Version: x/flux2-klein:4b (Ollama experimental)

    Performance: Extremely fast local inference taking only 6–10 seconds per image generation.


How to Install & Use

    Enable the Function in Open WebUI:

        Go to Admin Panel > Functions.

        Click the + (plus) icon or Create / Import Function.

        Delete any default code, paste the entire pipe.py code into the editor, and click Save.

        Make sure the toggle switch next to Ollama & Flux Bridge is turned ON (Green).

    Select the Model in Chat:

        Refresh your browser page (CMD + R or F5).

        Click your current model dropdown at the top left of the chat window.

        Search for or scroll down to select Ollama & Flux Bridge.

    Generate Images:

        Simply type your image description/prompt (e.g., “a simple retro game controller texture”) into the chat, press enter, and wait 5–6 seconds for your asset to render directly in the chat!

    💡 Tip: You can customize the Ollama URL, model name, and timeout duration anytime by clicking the Gear/Settings icon next to the function inside the Admin panel.
