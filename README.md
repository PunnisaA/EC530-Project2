# EC530-Project2

Upload Service:
    upload image to database
Image Service:
    takes a raw image and convert it to vertices and labels
Document DB Service:
    stores image in terms of json or output from image service
Embedding Service:
    takes the vertices and labels and give embeddings of it
VectorIndexService:
    stores embedding vectors (another database)
CLI Service:
    is the main publisher and subscriber to send info to other modules
    2 options:
    1. upload an image
    2. query about image


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

chose 2 for the purposes of not having to move all the data around

Video Link in GDrive: https://drive.google.com/file/d/1oZBiFdSN1uU71vrZBQef5nTs2sC-Pyxp/view?usp=sharing