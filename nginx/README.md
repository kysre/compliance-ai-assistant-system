# Nginx Reverse Proxy

This directory contains the configuration for the Nginx reverse proxy service used in the Compliance AI Assistant System.

## Overview

The Nginx service acts as a reverse proxy that sits in front of the backend and frontend applications. It is responsible for routing incoming HTTP requests to the appropriate service based on the request URL. This setup provides a single entry point to the application and simplifies the overall architecture.

## Key Responsibilities

- **Request Routing**: It routes requests starting with `/api/` or `/admin/` to the Django backend service and all other requests to the Next.js frontend service.
- **Serving Static and Media Files**: It directly serves static and media files for the Django application, which is more efficient than serving them through Django in a production environment.
- **Load Balancing**: Although currently configured with single instances of the backend and frontend, this setup can be easily extended for load balancing across multiple container replicas.
- **SSL Termination**: In a production deployment, Nginx can be configured to handle SSL/TLS termination, encrypting traffic between clients and the proxy.

## File Structure

- `Dockerfile`: The Dockerfile used to build the Nginx image. It copies the custom configuration file into the official Nginx container.
- `default.conf`: The main Nginx configuration file that defines the reverse proxy rules.

## Configuration (`default.conf`)

The `default.conf` file contains two main `upstream` blocks and a `server` block:

- **`upstream backend`**: Defines the location of the Django backend service (`backend:8000`).
- **`upstream frontend`**: Defines the location of the Next.js frontend service (`frontend:3000`).

The `server` block listens on port `80` and includes the following `location` blocks:

- `location /`: The default location, which proxies requests to the `frontend` upstream.
- `location ~* ^/(api|admin)/`: Matches any request starting with `/api/` or `/admin/` and proxies it to the `backend` upstream.
- `location /static/` and `location /media/`: These locations are configured with an `alias` to serve static and media files directly from the volume shared with the backend container.

This configuration ensures that all application traffic is correctly routed and static assets are served efficiently.
