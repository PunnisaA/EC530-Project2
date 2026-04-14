# EC530-Project2

Upload Service:
    upload image to database
Image Service:
    takes a raw image and convert it to vertices and labels
Document DB Service:
    stores image in terms of json or output from image service
Embedding Service:
    takes the vertices and labels and give embeddings of it, which would be its location in the 
VectorIndexService:
    stores embedding vectors (another database)
CLI Service:
    is the main publisher and subscriber to send info to other modules
    2 options:
    1. upload an image
    2. query about image?





