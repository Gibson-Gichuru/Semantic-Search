# Semantic Search-Based Recommendation System with OpenAI and Redis

## Overview

This project is a web application that leverages OpenAI models for semantic search, enabling a recommendation system for products. Users can search for products using natural language, and the application returns products that are semantically close to the user's query. Redis is used as the vector database to ensure scalability and efficiency.

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Project Structure](#project-structure)
6. [Configuration](#configuration)
7. [Contributing](#contributing)
8. [License](#license)

## Features

- **Semantic Search**: Leverages OpenAI models to generate vector embeddings for product descriptions and reviews.
- **Scalable Vector Database**: Uses Redis for storing and querying vector embeddings.
- **Natural Language Search**: Users can search for products using natural language.
- **Efficient Recommendations**: Returns products that are semantically similar to the user's query.

## Requirements

- Python 3.7+
- Redis
- Flask
- OpenAI API key

## Installation

1. **Clone the repository**

   ```sh
   git clone https://github.com/yourusername/semantic-search-recommendation-system.git
   cd semantic-search-recommendation-system

s