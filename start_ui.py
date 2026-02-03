import gradio as gr
import torch
import torchaudio
from tortoise.api import TextToSpeech
from tortoise.utils.audio import get_voices, load_voices

# Initialize the TextToSpeech model globally
# This ensures we only load it once.
print("Initializing Tortoise TTS model...")
# Determine device: specific logic for Mac Silicon (MPS) is handled inside TextToSpeech,
# but we can force things if needed. TextToSpeech() auto-detects.
tts = TextToSpeech()

def generate_audio(text, voice, preset, seed):
    if not text:
        raise gr.Error("Please enter some text.")

    print(f"Generating audio for: '{text}' with voice: {voice} and preset: {preset}")

    voice_samples = None
    conditioning_latents = None

    if voice != "random":
        # Load voice samples
        # load_voices takes a list of voice names
        voice_samples, conditioning_latents = load_voices([voice])

    # Handle seed
    use_deterministic_seed = int(seed) if seed is not None else None

    # Generate
    # tts_with_preset handles the complex parameter tuning for us
    gen = tts.tts_with_preset(
        text,
        voice_samples=voice_samples,
        conditioning_latents=conditioning_latents,
        preset=preset,
        use_deterministic_seed=use_deterministic_seed
    )

    # gen is a tensor. It might be (1, S) or (k, 1, S).
    # We want to extract the audio data.
    if isinstance(gen, list):
        # Should not happen with tts_with_preset usually unless modified, but handled just in case
        if len(gen) > 0:
            gen = gen[0]

    if torch.is_tensor(gen):
        gen = gen.detach().cpu()
        if gen.dim() == 3:
            gen = gen.squeeze(1) # (k, S)
        if gen.dim() == 2 and gen.shape[0] > 1:
            # If multiple candidates, take the first one
            gen = gen[0]
        elif gen.dim() == 2:
             # (1, S)
            gen = gen.squeeze(0)

        # Now gen is (S,)
        numpy_audio = gen.numpy()
    else:
        # Fallback
        numpy_audio = gen

    # Gradio expects (sample_rate, numpy array)
    # Tortoise outputs 24kHz audio
    return (24000, numpy_audio)

def get_voice_list():
    voices = get_voices()
    voice_list = sorted(list(voices.keys()))
    # Ensure 'random' is an option
    if "random" not in voice_list:
        voice_list.insert(0, "random")
    return voice_list

def main():
    # CSS for a nicer look
    css = """
    .container { max_width: 900px; margin: auto; }
    """

    theme = gr.themes.Soft()

    with gr.Blocks(css=css, theme=theme, title="Tortoise TTS") as demo:
        gr.Markdown(
            """
            # 🐢 Tortoise TTS

            Generate high-quality speech from text using the Tortoise TTS model.
            """
        )

        with gr.Row():
            with gr.Column(scale=1):
                text_input = gr.Textbox(
                    label="Text",
                    placeholder="Enter text here...",
                    lines=5,
                    value="The quick brown fox jumps over the lazy dog."
                )

                with gr.Row():
                    voice_dropdown = gr.Dropdown(
                        choices=get_voice_list(),
                        label="Voice",
                        value="random",
                        interactive=True
                    )
                    preset_dropdown = gr.Dropdown(
                        choices=["ultra_fast", "fast", "standard", "high_quality"],
                        label="Quality Preset",
                        value="fast",
                        interactive=True
                    )

                with gr.Accordion("Advanced Settings", open=False):
                    seed_input = gr.Number(
                        label="Seed (Optional)",
                        value=None,
                        precision=0,
                        info="Set for reproducible results."
                    )

                generate_btn = gr.Button("Generate Speech", variant="primary", size="lg")

            with gr.Column(scale=1):
                audio_output = gr.Audio(label="Generated Audio", type="numpy")

        # Link the button
        generate_btn.click(
            fn=generate_audio,
            inputs=[text_input, voice_dropdown, preset_dropdown, seed_input],
            outputs=[audio_output]
        )

    print("Starting Gradio server...")
    demo.launch(share=False)

if __name__ == "__main__":
    main()
