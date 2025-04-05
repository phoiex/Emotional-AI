import gradio as gr
import subprocess
import os
import requests
import soundfile as sf
import tempfile
from PIL import Image

def process_inputs(audio_path, image_path):
    # 1. ASR
    text = asr(audio_path)
    print(text)
    # 2. Facial AU
    #au_data = run_au_detection(image_path)
    
    # 3. LLM
    response_text = llm(text)
    print(response_text)
    # 4-5. TTS + Voice Clone
    cloned_audio = tts(response_text)
    
    # 6. Audio2Face
    stream_to_audio2face(cloned_audio)
    
    return {
        "text": response_text,
        "audio": cloned_audio
    }

# --------------------------
# Gradio Interface
# --------------------------
with gr.Blocks(title="Metahuman Interaction") as demo:
    gr.Markdown("## 🎤 Speak to the Metahuman")
    
    with gr.Row():
        # Inputs
        audio_input = gr.Audio(
            sources=["microphone", "upload"],
            type="filepath",
            label="Speak Here"
        )
        image_input = gr.Image(
            sources=["webcam", "upload"],
            label="Face Image (Webcam/Upload)"
        )
    
    # Outputs
    with gr.Row():
        text_output = gr.Textbox(label="LLM Response")
        audio_output = gr.Audio(label="Cloned Voice", autoplay=True)
        au_output = gr.JSON(label="Facial Action Units")
    
    # Process
    audio_input.change(
        fn=process_inputs,
        inputs=[audio_input, image_input],
        outputs=[text_output, audio_output, au_output]
    )
    audio2face_html = gr.HTML(
        f"""
        <iframe 
            src="http://192.168.31.241:8011/streaming/webrtc-demo/?server=192.168.31.241" 
            width="100%" 
            height="500px"
            frameborder="0"
        ></iframe>
        """
    )

demo.launch(
    server_port=7869,
    share=True  # Set to False for local-only
)