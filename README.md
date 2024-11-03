
# Flag Images API

This API enables the flagging of images by saving image prompts and metadata retrieved from `sd-png-info` endpoints in a SQLite database. It is designed for use with mobile apps to provide structured metadata storage and retrieval for image generation prompts and settings. The API uses Flask for backend functionality, Gunicorn as the WSGI server, and Docker for containerization.

## Features

- **Flag Images**: Accepts `POST` requests to store image metadata and settings.
- **Integration with `sd-png-info`**: Receives data from `sd-png-info` endpoints and saves it for analysis and record-keeping.
- **API Key Authentication**: Protects API access with an API key.
- **Health Check Endpoint**: Provides a health status of the API.
- **Database**: Stores metadata in SQLite, enabling manual review and analysis.

## Project Structure

- `app.py` – Main Flask application file.
- `init_db.py` – Initializes the SQLite database and creates tables if they do not exist.
- `Dockerfile` – Configures Docker to run the app with Gunicorn.
- `.env` – Environment variables for the API key and port.
- `requirements.txt` – Lists required Python packages.

## Integration with `sd-png-info` Endpoints

The `flag-images-api` is designed to work with data returned by `sd-png-info` endpoints, commonly used in Stable Diffusion and other image generation tools. When an image is processed via `sd-png-info`, it provides various metadata such as:

- **Image Prompt**: The prompt used to generate the image.
- **Steps**: Number of steps taken in the generation process.
- **Sampler**: The sampling algorithm used.
- **CFG Scale**: Classifier-free guidance scale.
- **Seed**: The random seed for generation.
- **Size**: Dimensions of the generated image.
- **Model Hash and Name**: Identifiers for the model used.
- **Seed Resize From**: Original size for seed-based resizing.
- **Denoising Strength**: Degree of denoising applied.

### Mobile App Use Case

Mobile apps can use this API to store and retrieve structured data from images generated by Stable Diffusion. When a mobile app retrieves metadata from an `sd-png-info` endpoint, it can submit the data to this API’s `/flag-image` endpoint for long-term storage. This setup allows apps to build features such as reviewing image generation anomalies and harmful image generation.

## Prerequisites

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Python 3.9** (for local development)

## Environment Variables

Create a `.env` file in the project root with the following variables:

```plaintext
API_KEY=your_api_key_here
PORT=5000
```

## Setup

### 1. Clone the Repository

```bash
git clone <repository_url>
cd flag-images-api
```

### 2. Install Dependencies (For Local Development)

```bash
pip install -r requirements.txt
```

### 3. Initialize the Database

Run the following script to set up the database:

```bash
python init_db.py
```

## Usage

### Run Locally

To run the app locally for development, use:

```bash
flask run --host=0.0.0.0 --port=${PORT}
```

### Run with Docker

1. **Build the Docker Image**:

   ```bash
   docker build -t flag-images-api .
   ```

2. **Run the Docker Container**:

   ```bash
   docker run -p 5002:5000 --env-file .env flag-images-api
   ```

The API will now be accessible at `http://localhost:5002`.

## API Endpoints

### Flag an Image

- **URL**: `/flag-image`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <API_KEY>`
- **Data**: JSON payload from the `sd-png-info` endpoint

Example request body:

```json
{
  "image_prompt": "A beautiful landscape",
  "steps": "50",
  "sampler": "Euler a",
  "cfg_scale": "7.5",
  "seed": "12345",
  "size": "512x512",
  "model_hash": "abcdef123456",
  "model_name": "Stable Diffusion v1.4",
  "seed_resize_from": "None",
  "denoising_strength": "0.7"
}
```

### Health Check

- **URL**: `/health`
- **Method**: `GET`
- **Description**: Returns a JSON response indicating API health status.

## Accessing the SQLite Database

If you want to copy the `flags.db` database from the container to your local machine for manual review:

1. Identify the container ID using:

   ```bash
   docker ps
   ```

2. Copy the `flags.db` file to your current directory:

   ```bash
   docker cp <container_id>:/app/flags.db ./flags.db
   ```

Replace `<container_id>` with the actual container ID.

## License

This project is licensed under the GNU GPL 3.0 License.
