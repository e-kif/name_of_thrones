swagger_template = {
    'swagger': '2.0',
    'info': {
        'title': 'Name of Thrones',
        'description': 'It\'s like the Game of Thrones but more focused on the Names of show\'s characters.',
        'version': '1.0'},
    'basePath': '/',
    'schemes': ['http', 'https'],
    'securityDefinitions': {
        'BearerAuth': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Enter "Bearer <token>" after logging in to access secured endpoints.'
        }},

    'paths': {
        '/characters/': {
            'get': {
                'summary': 'Retrieve a list of characters',
                'tags': [
                    'Characters'
                ],
                'description': 'Fetch characters applying filters, sorting, and pagination.'
                               'If no query parameters are provided, 20 default characters'
                               'sorted by id are returned.',
                'produces': [
                    'application/json'
                ],
                'parameters': [
                    {
                        'name': 'limit',
                        'in': 'query',
                        'description': 'The number of characters to return. Must be an integer.',
                        'required': False,
                        'type': 'integer'
                    },
                    {
                        'name': 'skip',
                        'in': 'query',
                        'description': 'The number of characters to skip (for pagination). Must be an integer.',
                        'required': False,
                        'type': 'integer'
                    },
                    {
                        'name': 'sorting',
                        'in': 'query',
                        'description': 'Field to sort by, e.g., "id" or "name".',
                        'required': False,
                        'type': 'string'
                    },
                    {
                        'name': 'order',
                        'in': 'query',
                        'description': 'Sort order, e.g., "asc" for ascending or "desc" for descending.',
                        'required': False,
                        'type': 'string'
                    },
                    {
                        'name': 'name',
                        'in': 'query',
                        'description': 'Filter characters by name.',
                        'required': False,
                        'type': 'string'
                    },
                    {
                        'name': 'house',
                        'in': 'query',
                        'description': 'Filter characters by house.',
                        'required': False,
                        'type': 'string'
                    },
                    {
                        'name': 'animal',
                        'in': 'query',
                        'description': 'Filter characters by animal.',
                        'required': False,
                        'type': 'string'
                    },
                    {
                        'name': 'symbol',
                        'in': 'query',
                        'description': 'Filter characters by symbol.',
                        'required': False,
                        'type': 'string'
                    },
                    {
                        'name': 'nickname',
                        'in': 'query',
                        'description': 'Filter characters by nickname.',
                        'required': False,
                        'type': 'string'
                    },
                    {
                        'name': 'role',
                        'in': 'query',
                        'description': 'Filter characters by role.',
                        'required': False,
                        'type': 'string'
                    },
                    {
                        'name': 'strength',
                        'in': 'query',
                        'description': 'Filter characters by strength.',
                        'required': False,
                        'type': 'string'
                    },
                    {
                        'name': 'age',
                        'in': 'query',
                        'description': 'Filter characters by exact age (integer).',
                        'required': False,
                        'type': 'integer'
                    },
                    {
                        'name': 'age_more_than',
                        'in': 'query',
                        'description': 'Filter characters with an age greater than the given value.',
                        'required': False,
                        'type': 'integer'
                    },
                    {
                        'name': 'age_less_than',
                        'in': 'query',
                        'description': 'Filter characters with an age less than the given value.',
                        'required': False,
                        'type': 'integer'
                    },
                    {
                        'name': 'death',
                        'in': 'query',
                        'description': 'Filter characters by death value (integer).',
                        'required': False,
                        'type': 'integer'
                    }
                ],
                'responses': {
                    '200': {
                        'description': 'Successful response with a list of characters.'
                    },
                    '400': {
                        'description': 'Bad request due to invalid parameters.'
                    },
                    '404': {
                        'description': 'No characters found.'
                    }
                }
            },
            'post': {
                'summary': 'Add a new character',
                'tags': [
                    'Characters'
                ],
                'security': [
                    {
                        'BearerAuth': []
                    }
                ],
                'description': 'Creates a new character in the database. Requires a valid token for authorization.',
                'produces': [
                    'application/json'
                ],
                'parameters': [
                    {
                        'name': 'body',
                        'in': 'body',
                        'description': 'The new character data to be added.',
                        'required': True,
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'name': {
                                    'type': 'string',
                                    'description': 'Name of the character.',
                                    'required': True
                                },
                                'house': {
                                    'type': 'string',
                                    'description': 'House affiliation of the character.'
                                },
                                'age': {
                                    'type': 'integer',
                                    'description': 'Age of the character.'
                                },
                                'nickname': {
                                    'type': 'string',
                                    'description': 'Nickname of the character.'
                                },
                                'animal': {
                                    'type': 'string',
                                    'description': 'Animal of the character.'
                                },
                                'symbol': {
                                    'type': 'string',
                                    'description': 'Symbol of the character.'
                                },
                                'role': {
                                    'type': 'string',
                                    'description': 'Role of the character.',
                                    'required': True
                                },
                                'death': {
                                    'type': 'string',
                                    'description': 'Season of character\'s death.'
                                },
                                'strength': {
                                    'type': 'string',
                                    'description': 'Strength of the character.',
                                    'required': True
                                }

                            },
                            'example': {
                                'name': 'Tyrion Lannister',
                                'house': 'Lannister',
                                'animal': 'Lion',
                                'symbol': 'Lion',
                                'nickname': 'The Imp',
                                'role': 'Hand of the King',
                                'age': 39,
                                'death': None,
                                'strength': 'Intelligence'
                            }
                        }
                    }
                ],
                'responses': {
                    '201': {
                        'description': 'Character created successfully.'
                    },
                    '400': {
                        'description': 'Invalid data provided.'
                    },
                    '409': {
                        'description': 'Conflict due to duplicate data or other constraints.'
                    }
                }
            }
        },

        '/characters/{character_id}': {
            'get': {
                'summary': 'Retrieve a specific character by ID',
                'tags': [
                    'Characters'
                ],
                'description': 'Fetch a single character by its unique ID.'
                               'If the specified character ID is not found,'
                               'an error response is returned.',
                'produces': [
                    'application/json'
                ],
                'parameters': [
                    {
                        'name': 'character_id',
                        'in': 'path',
                        'description': 'The unique identifier of the character.',
                        'required': True,
                        'type': 'integer'
                    }
                ],
                'responses': {
                    '200': {
                        'description': 'Successful response with the character details.'
                    },
                    '404': {
                        'description': 'Character not found. Returned when the provided character_id does not exist.'
                    }
                }
            },
            'delete': {
                'summary': 'Remove a character by ID',
                'tags': [
                    'Characters'
                ],
                'security': [
                    {
                        'BearerAuth': []
                    }
                ],
                'description': 'Deletes a specific character from the database by its unique ID.'
                               'Requires a valid token for authorization.',
                'produces': [
                    'application/json'
                ],
                'parameters': [
                    {
                        'name': 'character_id',
                        'in': 'path',
                        'description': 'The unique identifier of the character to be deleted.',
                        'required': True,
                        'type': 'integer'
                    }
                ],
                'responses': {
                    '200': {
                        'description': 'Character deleted successfully.'
                    },
                    '404': {
                        'description': 'Character not found.'
                    }
                }
            },
            'put': {
                'summary': 'Update a character by ID',
                'tags': [
                    'Characters'
                ],
                'security': [
                    {
                        'BearerAuth': []
                    }
                ],
                'description': 'Updates an existing character in the database'
                               'using its unique ID. Requires a valid token for authorization.',
                'produces': [
                    'application/json'
                ],
                'parameters': [
                    {
                        'name': 'character_id',
                        'in': 'path',
                        'description': 'The unique identifier of the character to be updated.',
                        'required': True,
                        'type': 'integer'
                    },
                    {
                        'name': 'body',
                        'in': 'body',
                        'description': 'The updated character data.',
                        'required': True,
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'name': {
                                    'type': 'string',
                                    'description': 'Updated name of the character.'
                                },
                                'house': {
                                    'type': 'string',
                                    'description': 'Updated house affiliation of the character.'
                                },
                                'age': {
                                    'type': 'integer',
                                    'description': 'Updated age of the character.'
                                },
                                'nickname': {
                                    'type': 'string',
                                    'description': 'Nickname of the character.'
                                },
                                'animal': {
                                    'type': 'string',
                                    'description': 'Animal of the character.'
                                },
                                'symbol': {
                                    'type': 'string',
                                    'description': 'Symbol of the character.'
                                },
                                'role': {
                                    'type': 'string',
                                    'description': 'Role of the character.'
                                },
                                'death': {
                                    'type': 'string',
                                    'description': 'Season of character\'s death.'
                                },
                                'strength': {
                                    'type': 'string',
                                    'description': 'Strength of the character.'
                                }

                            },
                            'example': {
                                'name': 'Arya Stark',
                                'house': 'Stark',
                                'age': 19
                            }
                        }
                    }
                ],
                'responses': {
                    '200': {
                        'description': 'Character updated successfully.'
                    },
                    '400': {
                        'description': 'Invalid data provided or character ID not found.'
                    },
                    '404': {
                        'description': 'Character not found.'
                    }
                }
            }
        },

        '/login': {
            'post': {
                'summary': 'User login',
                'tags': [
                    'Authentication'
                ],
                'description': 'Allows a user to log in and receive an access token.'
                               'Username and password are required.',
                'produces': [
                    'application/json'
                ],
                'parameters': [
                    {
                        'name': 'body',
                        'in': 'body',
                        'description': 'The login credentials.',
                        'required': True,
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'username': {
                                    'type': 'string',
                                    'description': 'The username of the user.'
                                },
                                'password': {
                                    'type': 'string',
                                    'description': 'The password of the user.'
                                }
                            },
                            'example': {
                                'username': 'user123',
                                'password': 'securepassword'
                            }
                        }
                    }
                ],
                'responses': {
                    '200': {
                        'description': 'Successfully authenticated. Returns the access token.'
                    },
                    '400': {
                        'description': 'Missing username or password.'
                    },
                    '401': {
                        'description': 'Invalid username or password.'
                    }
                }
            }
        },

        '/users/': {
            'get': {
                'summary': 'Retrieve all users',
                'tags': [
                    'Users Admin'
                ],
                'description': 'Fetches a list of all users in the database.',
                'security': [{'BearerAuth': []}],
                'produces': [
                    'application/json'
                ],
                'responses': {
                    '200': {
                        'description': 'Successfully retrieved the list of users.'
                    }
                }
            },
            'post': {
                'summary': 'Create a new user',
                'tags': [
                    'Users'
                ],
                'description': 'Creates a new user with the provided username, password, and optional role.',
                'produces': [
                    'application/json'
                ],
                'parameters': [
                    {
                        'name': 'body',
                        'in': 'body',
                        'description': 'The new user data to be added.',
                        'required': True,
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'username': {
                                    'type': 'string',
                                    'description': 'The new username of the current user.'
                                },
                                'password': {
                                    'type': 'string',
                                    'description': 'The new password for the current user.'
                                },
                                'role': {
                                    'type': 'string',
                                    'description': 'New role for the current user.'
                                }
                            },
                            'example': {
                                'username': 'user123',
                                'password': 'securepassword',
                                'role': 'admin'
                            }
                        }
                    }
                ],
                'responses': {
                    '200': {
                        'description': 'User updated successfully.'
                    },
                    '400': {
                        'description': 'Missing required field or invalid input.'
                    },
                    '409': {
                        'description': 'Conflict due to duplicate data.'
                    }
                }
            }
        },

        '/users/me': {
            'get': {
                'summary': 'Fetches a current user',
                'tags': ['Users'],
                'description': 'Fetches current user\'s info.',
                'security': [{'BearerAuth': []}],
                'produces': [
                    'application/json'
                ],
                'parameters': [],
                'responses': {
                    '200': {'description': 'Current user info.'},
                    '401': {'description': 'Not authenticated.'}
                },
            },
            'put': {
                'summary': 'Updates a current user',
                'tags': ['Users'],
                'description': 'Updates current user\'s info.',
                'security': [{'BearerAuth': []}],
                'produces': ['application/json'],
                'parameters': [{
                    'name': 'body',
                    'in': 'body',
                    'description': 'User info to be updated.',
                    'required': True,
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'username': {
                                'type': 'string',
                                'description': 'The new username of the current user.'
                            },
                            'password': {
                                'type': 'string',
                                'description': 'The new password for the current user.'
                            },
                            'role': {
                                'type': 'string',
                                'description': 'The new role of the current user.'
                            }
                        },
                        'example': {
                            'username': 'user123',
                            'password': 'securepassword',
                            'role': 'Salesman'
                        }
                    }
                }],
                'responses': {
                    '200': {'description': 'Updated current user info.'},
                    '400': {'description': 'Invalid request body.'},
                    '409': {'description': 'Conflict: username already taken.'},
                    '401': {'description': 'Not authenticated.'}
                }
            },
            'delete': {
                'summary': 'Delete a current user',
                'tags': ['Users'],
                'description': 'Deletes a specific user by their unique ID.',
                'security': [{'BearerAuth': []}],
                'produces': [
                    'application/json'
                ],
                'parameters': [],
                'responses': {
                    '200': {'description': 'Current user deleted successfully.'},
                    '401': {'description': 'Not authenticated.'}
                },
            },
        },

        '/users/{user_id}': {
            'delete': {
                'summary': 'Delete a user by ID',
                'tags': [
                    'Users Admin'
                ],
                'security': [{'BearerAuth': []}],
                'description': 'Deletes a specific user by their unique ID.',
                'produces': [
                    'application/json'
                ],
                'parameters': [
                    {
                        'name': 'user_id',
                        'in': 'path',
                        'description': 'The unique identifier of the user to be deleted.',
                        'required': True,
                        'type': 'integer'
                    }
                ],
                'responses': {
                    '200': {'description': 'User deleted successfully.'},
                    '404': {'description': 'User not found.'},
                    '401': {'description': 'Not authenticated.'},
                    '403': {'description': 'User does not have permission for this endpoint.'}
                }
            },
            'get': {
                'summary': 'Retrieve a specific user by ID',
                'tags': [
                    'Users Admin'
                ],
                'security': [{'BearerAuth': []}],
                'description': 'Fetches the details of a specific user by their unique ID.',
                'produces': [
                    'application/json'
                ],
                'parameters': [
                    {
                        'name': 'user_id',
                        'in': 'path',
                        'description': 'The unique identifier of the user.',
                        'required': True,
                        'type': 'integer'
                    }
                ],
                'responses': {
                    '200': {'description': 'Successfully retrieved the user details.'},
                    '404': {'description': 'User not found.'},
                    '401': {'description': 'Not authenticated.'},
                    '403': {'description': 'User does not have permission for this endpoint.'}
                }
            },
            'put': {
                'summary': 'Update a user by ID',
                'tags': [
                    'Users Admin'
                ],
                'security': [{'BearerAuth': []}],
                'description': 'Updates the details of an existing user.'
                               'At least one of the fields (username, password, role) must be provided.',
                'produces': [
                    'application/json'
                ],
                'parameters': [
                    {
                        'name': 'user_id',
                        'in': 'path',
                        'description': 'The unique identifier of the user to be updated.',
                        'required': True,
                        'type': 'integer'
                    },
                    {
                        'name': 'body',
                        'in': 'body',
                        'description': 'The updated user data.',
                        'required': True,
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'username': {
                                    'type': 'string',
                                    'description': 'Updated username for the user.'
                                },
                                'password': {
                                    'type': 'string',
                                    'description': 'Updated password for the user.'
                                },
                                'role': {
                                    'type': 'string',
                                    'description': 'Updated role for the user.'
                                }
                            },
                            'example': {
                                'username': 'updated_user',
                                'password': 'newsecurepassword',
                                'role': 'moderator'
                            }
                        }
                    }
                ],
                'responses': {
                    '200': {'description': 'User updated successfully.'},
                    '400': {'description': 'Invalid input or no valid fields provided.'},
                    '404': {'description': 'User not found.'},
                    '401': {'description': 'Not authenticated.'},
                    '403': {'description': 'User does not have permission for this endpoint.'}
                }
            }
        },

        '/database/reset': {
            'get': {
                'summary': 'Resets application database',
                'tags': ['Database'],
                'description': 'Drops all database tables, creates them and populates with the default data.',
                'security': [{'BearerAuth': []}],
                'produces': [
                    'application/json'
                ],
                'parameters': [],
                'responses': {
                    '200': {'description': 'Database was reset successfully.'},
                    '401': {'description': 'Not authenticated.'},
                    '403': {'description': 'User does not have permission for this endpoint.'}
                },

            }
        }

    },

    'tags': [
        {
            'name': 'Characters',
            'description': 'Endpoints for character management and retrieval.'
        },
        {
            'name': 'Users',
            'description': 'Endpoints for managing currently logged in user.'
        },
        {
            'name': 'Users Admin',
            'description': 'Endpoints for user management done by administrator (Regional Manager).'
        },
        {
            'name': 'Database',
            'description': 'Endpoints for database management done by administrator (Regional Manager).'
        }
    ]

}
