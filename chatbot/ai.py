import os
import io
import warnings
import pathlib

from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

# This file is basically the stability.ai tutorial for now.
# TODO: cleanup.

def get_key():
    return pathlib.Path('./stability.key').read_text().strip()

stability_api = client.StabilityInference(
    key=get_key(),
    verbose=True,
    engine="stable-diffusion-v1-5",
    # TODO 2.0 is out in their ui too
    # Available engines: stable-diffusion-v1 stable-diffusion-v1-5 stable-diffusion-512-v2-0 stable-diffusion-768-v2-0
    # stable-diffusion-512-v2-1 stable-diffusion-768-v2-1 stable-inpainting-v1-0 stable-inpainting-512-v2-0
)

def make_prompt(text):
    return generation.Prompt(text=text, parameters=generation.PromptParameters(weight=1))

def generate(prompt, seed):
    answers = stability_api.generate(
        # Negative prompting is now possible via the API, simply assign a negative weight to a prompt.
        # In the example above we are combining a mountain landscape with the style of thomas kinkade, and we are negative prompting trees out of the resulting concept.
        # When determining prompt weights, the total possible range is [-10, 10] but we recommend staying within the range of [-2, 2].
        prompt=prompt,
        seed=seed,
        steps=15, # Amount of inference steps performed on image generation. Defaults to 30.
        cfg_scale=8.0, # Influences how strongly your generation is guided to match your prompt.
                       # Setting this value higher increases the strength in which it tries to match your prompt.
                       # Defaults to 7.0 if not specified.
        width=512, # Generation width, defaults to 512 if not included.
        height=512, # Generation height, defaults to 512 if not included.
        samples=1, # Number of images to generate, defaults to 1 if not included.
        sampler=generation.SAMPLER_K_DPMPP_2M # Choose which sampler we want to denoise our generation with.
                                                     # Defaults to k_dpmpp_2m if not specified. Clip Guidance only supports ancestral samplers.
                                                     # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m)
    )

    # Set up our warning to print to the console if the adult content classifier is tripped.
    # If adult content classifier is not tripped, save generated images.
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                img.save("images/" + str(artifact.seed)+ ".png") # Save our generated images with their seed number as the filename.
                img.save("images/latest.png") # Save
