# AI Legal Assistant (RAG)

## Overview

AI Legal Assistant is a Retrieval-Augmented Generation (RAG) application that helps users interact with legal documents using natural language questions.

The project allows users to ask questions about legal information and receive answers generated based on retrieved legal sources. Instead of manually searching through long legal documents, users can ask questions directly and the system retrieves the most relevant legal sections before generating an answer.

The main goal of this project is to make legal information easier to access while keeping answers grounded in reliable source documents.

## Problem

Legal documents are often large, complex, and difficult to search manually. Finding a specific article or regulation requires time and familiarity with legal terminology.

This project helps solve this problem by:

- Allowing users to ask legal questions in natural language.
- Retrieving relevant information from legal documents.
- Generating answers based on retrieved legal context.
- Reducing the time required to search through documents.
- Maintaining a connection between answers and their original sources.

## Knowledge Base

The current knowledge base was collected and prepared manually from legal sources.

The project currently uses:

### Jordanian Labor Law

- Extracted from an official PDF document.
- The document was processed, cleaned, and divided into smaller chunks.
- Each chunk was stored with metadata to support retrieval and source tracking.

### Social Security Corporation (SSC) FAQs

- A small collection of frequently asked questions was collected from the official Social Security Corporation website.
- These questions were processed and added as additional knowledge sources.

The purpose of manually collecting and preparing these sources is to create a reliable legal knowledge base that the RAG system can retrieve information from when answering user questions.

## How It Works

The application follows a Retrieval-Augmented Generation pipeline:

### 1. Query Processing

The user sends a legal question through the API.

The query is preprocessed to improve retrieval quality before searching the knowledge base.

### 2. Embedding

The query is converted into a vector representation using an embedding model.

Documents are also converted into embeddings during the indexing process.

### 3. Retrieval

The system searches the vector database to find the most relevant document chunks related to the user's question.

The project uses ChromaDB as the vector database.

### 4. Reranking

Retrieved chunks can be passed through a reranking model to improve the ordering and select the most relevant context.

### 5. Answer Generation

The retrieved legal context is provided to the LLM together with the user's question.

The LLM generates an answer based on the available legal sources.

## Features

- AI-powered legal question answering.
- Retrieval-Augmented Generation (RAG) pipeline.
- Semantic search using embeddings.
- ChromaDB vector database integration.
- Reranking support for improving retrieval quality.
- Modular FastAPI architecture.
- Separation between API routes, services, and utilities.
- Source-grounded answers from legal documents.

## Project Architecture

The project is built using FastAPI with a modular architecture.
