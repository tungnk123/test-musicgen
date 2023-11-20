from gradio_client import Client

client = Client("https://haoheliu-audioldm2-text2audio-text2music--6bf6f75654dd7m.hf.space/")
result = client.predict(
				"I am so sad",	# str  in 'Input your prompt here' Textbox component
				6,	# int | float (numeric value between 0 and 6) in 'Guidance scale (Large => better quality and relavancy to text; Small => better diversity)' Slider component
				5,	# int | float  in 'Change this value (any integer number) will lead to a different generation result.' Number component
				1,	# int | float (numeric value between 1 and 3) in 'Automatic quality control. This number control the number of candidates (e.g., generate three audios and choose the best to show you). A Larger value usually lead to better quality with heavier computation' Slider component
				fn_index=0
)
print(result)