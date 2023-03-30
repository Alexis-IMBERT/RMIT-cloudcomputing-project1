- [ ]
- [x] Create a login table containing 10 entities
- [x] write a programe to automatically create a table music in dynamoDB with differente attributes
        [doc here](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html)
- [x] write a programe to automatically load the data from a1.json to your music table
- [x] login page fonctionelle
    - [x] récuperer les champs des inputs
    - [x] test dans la base de données
    - [x] connection si pertinent
- [x] register page
    - [x] récuperer les champs des inputs
    - [x] test dans la base de données
    - [x] message si non pertinent
- [x] after user login show the user_name
- [x] after user logout redirect to login page
- [ ] Query area 
    - [ ] If the queried information is contained in (one or more) entities’ corresponding attribute value(s) in the music table, the area will show
    - [ ] If the queried information is not contained in the entities’ corresponding attribute value(s) in the music table, it will show “No result is retrieved. Please query again”.
    - [ ] All the retrieved music information (title, artist, and year).
    - [ ] Each music information is followed by the corresponding artist images retrieved from S3 and a “Subscribe” button.
    - [ ] If the user clicks a “Subscribe” button, the subscribed music information and the corresponding artist image will be added into the subscription area and the subscribed music information will be stored in DynamoDB.
- [ ] Subscription area :
    - [ ] The subscription area will show all the user subscribed music information (title, artist, and year) stored in DynamoDB.
    - [ ] Each music information is followed by the corresponding artist image retrieved from S3 and a “Remove” button.
    - [ ] If the user clicks a “Remove” button, the corresponding subscribed music information and artist information will be removed from the subscription area and the corresponding table in DynamoDB.


