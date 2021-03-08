# Follow Kenzie API DOCUMENTATION

## Django version:

3.1.6

## The application:

- This api is to compose the backend of a social network, where companies and customers can share posts, follow users, comment ... A world of connections!

## URL base:

```
https://follow-kenzie.herokuapp.com/api
```

# ENDPOINTS

## POST /accounts/

creating user, the type of user can be a customer or company :

```
// REQUEST

{
	"username": "Maria",
	"password": "1234",
	"type": "client"
}

// RESPONSE STATUS -> HTTP 201

{
  "id": 1,
  "username": "Maria",
  "type": "client"
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

## GET /members/<str:username>/

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

## POST /members/<int:user_id>/

It is possible to follow another user by passing his id as parameter

```
// REQUEST
// Header -> Authorization: Token <token>

// RESPONSE STATUS -> HTTP 200

 "OK"
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

## PUT /timeline/post/<int:post_id>/

Only the user with the permission of the author can edit and delete their own posts

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

## DELETE /timeline/post/<int:post_id>/

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

## GET /timeline/private/

Lists all public and also private posts of the users that the logged in user follows

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

## POST /timeline/post/<int:post_id>/

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

## POST timeline/comments/<int:post_id>/

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

## GET /mynotification/

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
    "text": "Você recebeu um like de Mario no Post Olá Mundo",
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
    "text": "Você recebeu um comentário de José no Post Olá Mundo",
    "read": false
  }
]

```

## Deployment

- Heroku was used for deployment

## Database:

- PostgreSQL

# OBSERVATIONS

- The use of docker, docker-compose and Gitlab runner for the CI-CD was implemented.
