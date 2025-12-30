# FTP Server
This FTP server is designed to safely handle file transfers for a home server.

## Overview
This server uses python sockets to handle quickly transfering data.

## Outline
The server processes connections as follows:
1. The server listens for incomming connections
2. The client connects to the server
3. The server completes a security handshake with the client
4. The server accepts and transfers the connection to a seperate thread
5. The client sends a JSON request to the server
6. The server uses the requests `type` header to determine which dispatcher to forward the request to
7. The dispatcher completes an opperation using the requests `body`, and a resolution object given by the handler
8. The dispatcher then sends a status and message to the resolution
9. The resolution transfers the dispatchers status and message to the client

## Security Handshake
I'll do it eventually 

## Thread Management
The server handles threads using the `concurrent` package. The main thread waits for client connection requests. Once a connection request is found, the server accepts the connection and sends it to a seperate thread for validation.
When the server accepts a connection it pulls a thread from the thread pool. This pool has a fixef length, defined in `config.py`, and is immutable. The pool does not auto scale to ensure server and data integrity.

## JSON Request Format
Each JSON request has two paramaters:
1. The `request_type` tells the server which dispatcher it should use to process the request. Allowed types include:
   - `GET` requests. These are requests to fetch a resource at a certain endpoint.
   - `CMP` requests. These compare the state of a local file against the remote.
   - `PUSH` requests. These push a file to a certain endpoint in the remotes root. Push requests will override any content at the endpoint.
  
### GET
Each GET request must contain a body with the following context:
```json
{
   rel_endpoint: "path/to/resource
}
```
The request returns a status code (0 for success) alongside the content of the resource at the given endpoint.
The target can be any of the following filetypes:
- `.txt`

### CMP
Each CMP request must contain a body with the following context:
```json
{
   rel_endpoint: "path/to/resource,
   hash: some_hash
   meta_data: [
       entry1,
       entry2
   ]
}
```
The request returns a status code (10 to 14 for success) representing the state of the remote compared to the local state. The request compares the hash of a local resource against the hash of the resource in the remote, and the metadata of the local resource against the metadata of the remote resource.
The target can be any of the following filetypes:
- `.txt`
