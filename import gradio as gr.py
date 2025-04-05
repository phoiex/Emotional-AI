import gradio as gr
import numpy as np

# Configuration
AUDIO2FACE_URL = "http://192.168.31.241:8011/streaming/webrtc-client"

def process_audio(audio_input):
    """Process audio input and return analysis results"""
    sr, audio = audio_input
    if len(audio.shape) > 1:  # Convert stereo to mono if needed
        audio = np.mean(audio, axis=1)
    
    # Generate text output (replace with your actual processing)
    text_output = (
        f"Audio Analysis Results:\n\n"
        f"- Sample Rate: {sr}Hz\n"
        f"- Duration: {len(audio)/sr:.2f} seconds\n"
        f"- Max Amplitude: {np.max(np.abs(audio)):.4f}"
    )
    
    return text_output

with gr.Blocks(title="Audio2Face Controller") as demo:
    with gr.Row():
        # Left column - inputs/outputs
        with gr.Column(scale=1):
            gr.Markdown("## Audio Controls")
            audio_input = gr.Audio(sources=["microphone"], 
                                 type="numpy",
                                 label="Speak Here")
            submit_btn = gr.Button("Process Audio")
            text_output = gr.Textbox(label="Analysis Results", 
                                   interactive=False)
        
        # Right column - Audio2Face
        with gr.Column(scale=1):
            gr.Markdown("## Audio2Face Display")
            gr.HTML(f"""
            <iframe 
                src="{AUDIO2FACE_URL}" 
                width="100%" 
                height="600px"
                style="border:none;"
                allow="microphone *"
                id="a2f-iframe"
            ></iframe>
            """)
    
    submit_btn.click(
        fn=process_audio,
        inputs=audio_input,
        outputs=text_output
    )

if __name__ == "__main__":
    demo.launch(
        server_port=7860,
        server_name="0.0.0.0",
        share=True
    )