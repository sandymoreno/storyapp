# Serverless Story Generator

This project is a serverless application that integrates with the OpenApi API to generate stories for kids. It utilizes Lambda functions, DynamoDB, and AWS API Gateway. All the necessary resources and policies are created using the SAM (Serverless Application Model) framework and SAM CLI.

## Contents

-   [Description](#description)
-   [Prerequisites](#prerequisites)
-   [Installation](#installation)
-   [Usage](#usage)
-   [API Endpoints](#api-endpoints)
-   [Resources](#resources)
-   [License](#license)

## Description

The Serverless Story Generator is a serverless application that generates stories for kids based on predefined OpenApi specifications. It consists of Lambda functions written in Python 3.9, a DynamoDB table to store the stories, and an AWS API Gateway to expose the API endpoints. The application is deployed using the SAM framework, which simplifies the deployment and management of serverless applications on AWS.

## Prerequisites

Before deploying and running the Serverless Story Generator, make sure you have the following prerequisites:

-   AWS account
-   AWS CLI installed and configured
-   SAM CLI installed
-   Python 3.9 or later installed

## Installation

Follow these steps to install and deploy the Serverless Story Generator:

1. Clone the repository: `git clone https://github.com/your-username/serverless-story-generator.git`
2. Navigate to the project directory: `cd serverless-story-generator`
3. Deploy the application using SAM CLI:
    ```
    sam build
    sam deploy --guided
    ```
    Follow the prompts to configure the deployment options.

## Usage

To generate a story using the Serverless Story Generator, you can make a POST request to the `/story` endpoint of the deployed API. The request should include the necessary input data based on the OpenApi specification.

To retrieve a list of available stories, you can make a GET request to the `/stories` endpoint.

To retrieve a specific story by its ID, you can make a GET request to the `/story/{id}` endpoint, where `{id}` is the ID of the desired story.

## API Endpoints

The Serverless Story Generator exposes the following API endpoints:

-   `POST /story`: Generates a new story based on the provided input data.
-   `GET /stories`: Retrieves a list of available stories.
-   `GET /story/{id}`: Retrieves a specific story by its ID.

## Resources

The Serverless Story Generator utilizes the following AWS resources:

-   AWS Lambda functions: The Lambda functions handle the generation and retrieval of stories.
-   AWS DynamoDB table: The DynamoDB table is used to store the generated stories.
-   AWS API Gateway: The API Gateway acts as the interface to access the application's API endpoints.

## License

This project is licensed under the [MIT License](LICENSE).
