import onnxruntime_genai as og
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the model and tokenizer
model = og.Model('directml/directml-int4-awq-block-128')
tokenizer = og.Tokenizer(model)
tokenizer_stream = tokenizer.create_stream()

search_options = {
    'do_sample': False,
    'max_length': 2048,
    'min_length': 1,
    'top_p': 1.0,
    'top_k': 50,
    'temperature': 1.0,
    'repetition_penalty': 1.0
}

chat_template = '<|user|>\n{input} <|end|>\n<|assistant|>'

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()

    if not data or 'input' not in data:
        return jsonify({'error': 'Invalid input, "input" key is required in JSON data'}), 400

    text = data['input']

    if not text:
        return jsonify({'error': 'Input text cannot be empty'}), 400

    # Generate the prompt with the chat template
    prompt = f'{chat_template.format(input=text)}'

    input_tokens = tokenizer.encode(prompt)

    params = og.GeneratorParams(model)
    params.set_search_options(**search_options)
    params.input_ids = input_tokens
    generator = og.Generator(model, params)

    new_tokens = []

    try:
        while not generator.is_done():
            generator.compute_logits()
            generator.generate_next_token()

            new_token = generator.get_next_tokens()[0]
            decoded_token = tokenizer_stream.decode(new_token)
            new_tokens.append(decoded_token)

    except KeyboardInterrupt:
        return jsonify({'error': 'Generation interrupted'}), 500

    response = {
        'input': text,
        'output': ''.join(new_tokens)
    }

    return jsonify(response)

if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True)
