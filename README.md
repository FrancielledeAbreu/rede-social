# Follow Kenzie API DOCUMENTATION

## Django version:

3.1.6

## The application:

- This api is to compose the backend of a social network, where companies and customers can share posts, follow users, comment ... A world of connections!

## URL base:

```
localhost:8000/api
```

# ENDPOINTS

## POST /accounts/

creating user, the type of user can be a customer or company :

```
// REQUEST

{
	"username": "Maria",
	"password": "1234",
	"type": "  "type": "User"
"
}

// RESPONSE STATUS -> HTTP 201

{
  "id": 1,
  "username": "Maria",
  "type": "User"
}
```

## POST /login/

getting a token for the user:

```
// REQUEST

{
	"username": "Maria",
	"password": "1234"
}
}

// RESPONSE STATUS -> HTTP 200
{
  "token": "0f500a8c2f2f8d5edasdasdasdafcfvads812"
}
```

## GET /members/

listing the users

```
// REQUEST
// Header -> Authorization: Token <token>
[
  {
    "id": 1,
    "username": "Fernanda",
    "type": "client"
  },
  {
    "id": 2,
    "username": "Roberta",
    "type": "client"
  },
  {
    "id": 3,
    "username": "Mario",
    "type": "client"
  },
  {
    "id": 4,
    "username": "José",
    "type": "client"
  },
  {
    "id": 5,
    "username": "TechBrasil",
    "type": "company"
  }
]
```

## GET /members/<int:user_id>/

filters users by id

```
// REQUEST
// Header -> Authorization: Token <token>

base_url/members/2/

// RESPONSE

 {
  "id": 2,
  "username": "Maria",
  "type": "client"
}
```

## GET /members/search/<str:username>

filters users by username

```
// REQUEST
// Header -> Authorization: Token <token>

base_url/members/Maria/

// RESPONSE

 {
  "id": 2,
  "username": "Maria",
  "type": "client"
}
```

## PATCH /api/members/<int:user_id>/

-The token `owner` must be the one corresponding to the user id

update user data

```
// REQUEST
// Header -> Authorization: Token <token>

{
	"username": "Negócios Atuais"
}

// RESPONSE STATUS -> HTTP 200

 {
  "id": 81,
  "username": "Negócios Atuais",
  "type": "Company"
}
```

## DELETE /api/members/<int:user_id>/

-The token `owner` must be the one corresponding to the user id

```
// REQUEST
// Header -> Authorization: Token <token>


// RESPONSE STATUS -> HTTP 204

```

## POST /members/<int:user_id>/follow/

It is possible to follow another user by passing his id as parameter

```
// REQUEST
// Header -> Authorization: Token <token>

// RESPONSE STATUS -> HTTP 200

 ""João começou a seguir Renato""
```

## POST /members/<int:user_id>/unfollow/

It is possible to unfollow another user by passing his id as parameter

```
// REQUEST
// Header -> Authorization: Token <token>

// RESPONSE STATUS -> HTTP 200

 "João começou a seguir Renato"

 If the current user does not follow the user passed by parameter:

 "Renata você não segue Fer"

```

## POST /timeline/

Endpoint that allows the creation of a new post, it is possible to set privacy to true, but as default the post is public, private = false.

```
// REQUEST
// Header -> Authorization: Token <token>

{
	"title": "Meu post atual",
	"description": "post atual",
	"image": "url image",
	"private":true
}

// RESPONSE STATUS -> HTTP 201

 {
  "id": 7,
  "author": {
    "id": 2,
    "username": "Maria",
    "type": "client"
  },
  "title": "Meu post atual",
  "description": "post atual",
  "image": "url image",
  "posted_on": "2021-03-08T14:20:12.830708Z",
  "private": true,
  "comment": [],
  "like": []
}

```

## PATCH /timeline/<int:post_id>/

`Only the user with the permission` of the author can `edit and delete` their own posts

```
// REQUEST
// Header -> Authorization: Token <token-author>

{
	"description": "Um novo post hoje",
	"image": "nova imagem",
}

// RESPONSE STATUS -> HTTP 200

 {
  "id": 7,
  "author": {
    "id": 2,
    "username": "Maria",
    "type": "client"
  },
  "title": "Meu post atual",
	"description": "Um novo post hoje",
  "image": "nova imagem",
  "posted_on": "2021-03-08T14:20:12.830708Z",
  "private": true,
  "comment": [],
  "like": []
}

```

## DELETE /timeline/<int:post_id>/

```
// REQUEST
// Header -> Authorization: Token <token-author>


// RESPONSE STATUS -> HTTP 204

```

## GET /timeline/

lists all public posts of registered users

```
// REQUEST
// Header -> Authorization: Token <token>


// RESPONSE STATUS -> HTTP 200

[
  {
    "id": 2,
    "author": {
      "id": 2,
      "username": "Francielle",
      "type": "client"
    },
    "title": "Olá Mundo",
    "description": "projeto",
    "image": "image url",
    "posted_on": "2021-03-04T13:33:28.475749Z",
    "private": false,
    "comment": [
      {
        "id": 1,
        "author": {
          "id": 4,
          "username": "Mario",
          "type": "client"
        },
        "comment": "Show",
        "image": "gif",
        "commented_on": "2021-03-04T13:49:23.167612Z"
      },
      {
        "id": 2,
        "author": {
          "id": 5,
          "username": "José",
          "type": "client"
        },
        "comment": "Show",
        "image": "gif",
        "commented_on": "2021-03-08T13:18:41.820187Z"
      }
    ],
    "like": [
      {
        "id": 1,
        "author": {
          "id": 4,
          "username": "Mario",
          "type": "client"
        }
      },
      {
        "id": 2,
        "author": {
          "id": 5,
          "username": "José",
          "type": "client"
        }
      }
    ]
  },
  {
    "id": 4,
    "author": {
      "id": 2,
      "username": "Francielle",
      "type": "client"
    },
    "title": "Meu post atual",
    "description": "post atual",
    "image": "url image",
    "posted_on": "2021-03-04T13:33:28.475749Z".
  },
  {
    "id": 5,
    "author": {
      "id": 5,
      "username": "José",
      "type": "client"
    },
    "title": "Meu post atual",
    "description": "post atual",
    "image": "url image",
    "posted_on": "2021-03-08T13:20:18.602513Z",
    "private": false,
    "comment": [],
    "like": []
  }
]

```

## GET /timeline/private

Lists all public and also private posts of the users that the `logged in user follows`

```
// REQUEST
// Header -> Authorization: Token <token>

// RESPONSE STATUS -> HTTP 200

[
  {
    "id": 5,
    "author": {
      "id": 5,
      "username": "José",
      "type": "client"
    },
    "title": "Meu post atual",
    "description": "post atual",
    "image": "url image",
    "posted_on": "2021-03-08T13:20:18.602513Z",
    "private": false,
    "comment": [],
    "like": []
  },
  {
    "id": 4,
    "author": {
      "id": 2,
      "username": "Francielle",
      "type": "client"
    },
    "title": "Meu post atual",
    "description": "post atual",
    "image": "url image",
    "posted_on": "2021-03-08T13:09:45.843396Z",
    "private": false,
    "comment": [],
    "like": []
  },
  {
    "id": 3,
    "author": {
      "id": 2,
      "username": "Francielle",
      "type": "client"
    },
    "title": "Meu post",
    "description": "post",
    "image": "url image",
    "posted_on": "2021-03-08T13:09:24.170226Z",
    "private": true,
    "comment": [],
    "like": []
  }
]

```

## GET /feed/

lists the authored posts of the logged in user

```
// REQUEST
// Header -> Authorization: Token <token>

// RESPONSE STATUS -> HTTP 200
[
  {
    "id": 5,
    "author": {
      "id": 2,
      "username": "Maria",
      "type": "client"
    },
    "title": "Meu post atual",
    "description": "post atual",
    "image": "url image",
    "posted_on": "2021-03-08T13:20:18.602513Z",
    "private": false,
    "comment": [],
    "like": []
  }
]

```

## POST /timeline/post/<int:post_id>/like/

The logged in user can like the post owner of the id, the answer will be the user data

```
// REQUEST
// Header -> Authorization: Token <token>

// RESPONSE STATUS -> HTTP 201

{
  "id": 2,
  "author": {
    "id": 5,
    "username": "José",
    "type": "client"
  }
}

```

## POST /comments/<int:post_id>/new/

It is possible to add a new comment, it is also possible to add an image

```
// REQUEST
// Header -> Authorization: Token <token>

{
	"comment": "Show",
	"image": "gif"
}

// RESPONSE STATUS -> HTTP 201

{
  "id": 2,
  "author": {
    "id": 5,
    "username": "José",
    "type": "client"
  },
  "comment": "Show",
  "image": "gif",
  "commented_on": "2021-03-08T13:18:41.820187Z"
}
```

## DELETE /comments/<int:post_id>/

only the `author` of the comment

```
// REQUEST
// Header -> Authorization: Token <token>

// RESPONSE STATUS -> HTTP 204


```

## GET /comments/

All comments

```
// REQUEST
// Header -> Authorization: Token <token>

// RESPONSE STATUS -> HTTP 200
```

## GET /mynotifications/

the logged in user will be able to know when his followers commented or liked his published posts.

```
// REQUEST
// Header -> Authorization: Token <token>

// RESPONSE STATUS -> HTTP 200

[
  {
    "id": 1,
    "user": {
      "id": 2,
      "username": "Francielle",
      "type": "client"
    },
    "author_id": 4,
    "message_type": "Comentario",
    "created_at": "2021-03-04T13:49:23.188151Z",
    "text": "Você recebeu um comentário de Mario no Post Olá Mundo",
    "read": false
  },
  {
    "id": 2,
    "user": {
      "id": 2,
      "username": "Francielle",
      "type": "client"
    },
    "author_id": 4,
    "message_type": "Like",
    "created_at": "2021-03-04T14:20:40.330895Z",
    "text": "Você recebeu um like de Mario no Post Férias",
    "read": false
  },
  {
    "id": 3,
    "user": {
      "id": 2,
      "username": "Francielle",
      "type": "client"
    },
    "author_id": 5,
    "message_type": "Comentario",
    "created_at": "2021-03-08T13:18:41.838298Z",
    "text": "Você recebeu um comentário de José no Post Cidade Linda",
    "read": false
  }
]

```

## PATCH /mynotification/<int:notification_id>/

```
// REQUEST
// Header -> Authorization: Token <token>

{ "read": true}

// RESPONSE STATUS -> HTTP 200

{
  "id": 1,
  "user": {
    "id": 70,
    "username": "João",
    "type": "client"
  },
  "author_id": 70,
  "message_type": "Like",
  "created_at": "2021-04-13T01:14:40.226614Z",
  "text": "Você recebeu um like de João no Post Olá Mundo",
  "read": true
}
```

## GET /reports/following/<int:user_id>/

## GET /reports/followers/<int:user_id>/

## GET /reports/notification/<int:user_id>/

-It is possible to extract the followers report, following and my notifications through CSV files.

## Deployment

- The deployment was `partially` carried out on heroku. Testing is recommended locally.

## Database:

- PostgreSQL

# OBSERVATIONS

- The use of docker, docker-compose and Gitlab runner for the CI-CD was implemented.
