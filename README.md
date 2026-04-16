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

Publishers and Subscribers:
    STATUS:
    - CLI service publishes to everyone to make sure that every service is on
    - Every other service subscribes to CLI service, similar to ACK

CLI interface UPLOAD:
    connects to upload service, which connects to image service, and then takes the output of that into document db

    TOPICS:
    1. 
    2. 
    3.


Message Structure Options:
1. what is currently there (no DB)
pros:
- simple responsibility
cons:
- no back up
2. have no data related to the image, only id's, call to get me (local database)
pros:
cons:
- 
3. store in db and call from there
pros:
- responses or results are persistent
- split responsibility
cons: 
- if other listeners use the databases at the same time, this is a problem when requesting or uploading the database
- multiple people being able to access is security issue

Events:
1. img_upload_requests
2. img_upload
3. img_proc_request
4. img_annotated
5. img_embedded
6. img_proc


#finish messaging system and define message





