# Edge-LLM

This project demonstrates how to use a language model with a Flask API. It allows you to send text inputs to the model and receive generated outputs via HTTP requests.

## Requirements

- Python 3.12+
- Install dependencies from `requirements.txt`:
  ```bash
  pip install -r requirements.txt
  ```

## Model Setup

1. **Download the Model**:
   Use the `huggingface-cli` to download the model and save it locally:
   ```bash
   huggingface-cli download microsoft/Phi-3-mini-4k-instruct-onnx --include directml/* --local-dir .
   ```

## Running the API

1. **Start the Flask API**:
   Run the `api.py` script in the command line:
   ```bash
   python api.py
   ```

2. The Flask API will be running at `http://127.0.0.1:5000`.

## Testing the API with Postman

1. Open **Postman** and create a POST request to the following endpoint:
   ```
   http://127.0.0.1:5000/generate
   ```

2. In the **Body** tab, set the request type to **JSON** and enter the following JSON data:
   ```json
   {
     "input": "Tell me a joke."
   }
   ```

3. You should receive a response similar to this:
   ```json
   {
     "input": "Tell me a joke.",
     "output": "Here's a joke..."
   }
   ```

## References

- [ONNX Runtime GenAI - Phi-3 Tutorial](https://github.com/microsoft/onnxruntime-genai/blob/main/examples/python/phi-3-tutorial.md)