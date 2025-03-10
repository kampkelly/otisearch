# Project README

This document provides an overview of the project, its features, and how to use it.

## Table of Contents

* [Introduction](#introduction)
* [Features](#features)
* [API Endpoints](#api-endpoints)
* [Database Synchronization](#database-synchronization)
* [Semantic Search](#semantic-search)
* [Retrieval Augmented Generation (RAG)](#retrieval-augmented-generation-rag)
* [Configuration](#configuration)
* [Dependencies](#dependencies)
* [Usage](#usage)
* [Database Relationships](#database-relationships)
* [Data Synchronization Status](#data-synchronization-status)
* [Elasticsearch Integration](#elasticsearch-integration)
* [Error Handling](#error-handling)

## Introduction

This project provides APIs for managing data synchronization, performing semantic searches, and retrieving insights on data using Retrieval Augmented Generation (RAG). It integrates with PostgreSQL and Elasticsearch to provide a comprehensive data management and search solution.

## Features

* **API to get user databases:** Retrieve a list of databases associated with a user.
* **API to add database and table:** Add a new database connection and specify tables for synchronization.
* **API to update add database logic:** Include and manage relationships between tables.
* **API to trigger sync:** Initiate data synchronization between PostgreSQL and Elasticsearch.
* **API to view sync status:** Monitor the progress of data synchronization.
* **API to perform semantic search:** Perform natural language searches using OpenAI and Elasticsearch.
* **API to retrieve insights on data:** Generate insights using Retrieval Augmented Generation (RAG).
* **API to get all user datasyncs:** Retrieve all data synchronization configurations for a user.
* **API to get a single database:** Retrieve detailed information about a single database.

## API Endpoints

* **`GET /databases`:** Retrieves a list of databases associated with the authenticated user.
* **`POST /sync/add-database`:** Adds a new database connection and specifies tables for synchronization. Requires relationship information.
* **`POST /sync/trigger-sync`:** Triggers data synchronization for a specified datasync configuration.
* **`POST /sync/status`:** Retrieves the synchronization status between PostgreSQL and Elasticsearch.
* **`POST /semantic`:** Performs a semantic search using natural language queries.
* **`POST /insights`:** Retrieves data insights using Retrieval Augmented Generation (RAG).
* **`GET /datasyncs`:** Retrieves all data synchronization configurations for a user.
    * Accepts an optional query parameter `is_active` to filter datasyncs based on their active status.
* **`GET /database/{database_id}`:** Retrieves a single database by its ID for a given user.

## Database Synchronization

The project utilizes `pgsync` to synchronize data between PostgreSQL and Elasticsearch. Synchronization configurations are managed through the `DataSync` model, and tables are linked to specific datasync configurations.

* **Triggering Sync:** Use the `/sync/trigger-sync` API endpoint with the `datasync_id` to initiate synchronization.
* **Sync Status:** Monitor synchronization progress using the `/sync/status` API endpoint.
* **Configuration:** `pgsync` is configured using dynamically generated JSON schema files. Environment variables are used for database and Elasticsearch credentials.
* **Index Naming:** Elasticsearch index names include the database name, table name, UUID, and timestamp for uniqueness.

## Semantic Search

The semantic search feature allows users to perform natural language searches using OpenAI's GPT-4o and Elasticsearch.

* **API Endpoint:** `/semantic`
* **Query Generation:** OpenAI is used to translate natural language queries into Elasticsearch queries.
* **Elasticsearch Integration:** Elasticsearch is used to perform the actual search.
* **Database Schema:** The `table` table includes an `es_columns` field to store Elasticsearch column information.

## Retrieval Augmented Generation (RAG)

The project implements Retrieval Augmented Generation (RAG) to provide insights on data.

* **API Endpoint:** `/insights`
* **Embedding Model:** `langchain_voyageai` is used for generating embeddings.
* **Search Service:** Elasticsearch is used to retrieve relevant documents.
* **Language Model:** Langchain is used to generate responses based on retrieved documents.

## Configuration

* **Environment Variables:**
    * `POSTGRES_URL`: PostgreSQL connection string.
    * `ELASTICSEARCH_HOST`: Elasticsearch host.
    * `ELASTICSEARCH_PORT`: Elasticsearch port.
    * `VOYAGE_API_KEY`: API key for VoyageAI embeddings.
    * `OPENAI_API_KEY`: API key for OpenAI.
    * Redis connection information.
    * Python virtual environment paths.
* **Redis:** Redis is used to store and track `pgsync` process information.

## Dependencies

* `pgsync`
* Redis
* Python virtual environment
* `langchain`
* `langchain-openai`
* `langchain-elasticsearch`
* `langchain_voyageai`
* `llama-index`
* `llama-index-embeddings-voyageai`

## Usage

1.  Set up a Python virtual environment.
2.  Install dependencies from `requirements.txt`.
3.  Configure environment variables.
4.  Configure Redis.
5.  Add a database and table using the `/sync/add-database` API.
6.  Trigger synchronization using the `/sync/trigger-sync` API.
7.  Monitor synchronization status using the `/sync/status` API.
8.  Perform semantic searches using the `/semantic` API.
9.  Retrieve data insights using the `/insights` API.
10. Retrieve all user datasyncs using `/datasyncs` API.
11. Retrieve a single database using `/database/{database_id}` API.

## Database Relationships

The project supports defining relationships between tables during the database addition process.

* **Relationship Data:** The `Relationship` object includes the foreign table name, columns involved in the relationship, and relationship type.
* **Validation:** Relationships are validated against the actual database schema.
* **Database Schema:** The `table` table includes a `relationships` column to store relationship data.

## Data Synchronization Status

The `/sync/status` API endpoint provides information about the synchronization status between PostgreSQL and Elasticsearch.

* **Response:** Includes `table_row_count`, `es_index_count`, `is_success`, and `percent`.
* **Index Count:** The Elasticsearch index document count is retrieved using `ESearchQuery`.
* **Table Count:** The PostgreSQL table row count is retrieved using `SyncDatabaseConnection`.

## Elasticsearch Integration

* **Configuration:** Elasticsearch connection is configured using `ELASTICSEARCH_HOST` and `ELASTICSEARCH_PORT` environment variables.
* **Custom Retriever:** `CustomElasticsearchRetriever` is used for retrieving relevant documents.
* **Query Generation:** Custom query generation functions are used to create Elasticsearch queries.
* **Rank:** `rank={"rrf": {"rank_window_size": 50}}` is added to the root of Elasticsearch queries.
* **Vector Plugin:** `VectorPlugin` is used to generate vector embeddings for search.

## Error Handling

* **Authentication:** Authentication failures result in a 401 Unauthorized error.
* **API Endpoints:** API endpoints include `try...except` blocks to catch exceptions and return error responses.
* **Database and Elasticsearch:** Errors related to database or Elasticsearch connections are handled and returned in API responses.
* **Relationship Validation:** Invalid relationship definitions result in errors during the `add_database` process.