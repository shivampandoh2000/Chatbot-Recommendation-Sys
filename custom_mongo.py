import re
from chatterbot.storage import StorageAdapter


class CusMongoDatabaseAdapter(StorageAdapter):
    """
    The MongoDatabaseAdapter is an interface that allows
    ChatterBot to store statements in a MongoDB database.

    :keyword database_uri: The URI of a remote instance of MongoDB.
                           This can be any valid
                           `MongoDB connection string <https://docs.mongodb.com/manual/reference/connection-string/>`_
    :type database_uri: str

    .. code-block:: python

       database_uri='mongodb://example.com:8100/'
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from pymongo import MongoClient
        from pymongo.errors import OperationFailure

        self.database_uri = kwargs.get(
            'database_uri', 'mongodb://localhost:27017/chatterbot-database'
        )

        # Use the default host and port
        self.client = MongoClient(self.database_uri)

        # Increase the sort buffer to 42M if possible
        try:
            self.client.admin.command({'setParameter': 1, 'internalQueryExecMaxBlockingSortBytes': 44040192})
        except OperationFailure:
            pass

        # Specify the name of the database
        self.database = self.client.get_database()

        # The mongo collection of statement documents
        self.statements = self.database['statements']
        print("This is __init__")
    def get_statement_model(self):
        """
        Return the class for the statement model.
        """
        from chatterbot.conversation import Statement

        # Create a storage-aware statement
        statement = Statement
        statement.storage = self
        print("This is get_statement_model")

        return statement


    def count(self):
        print("This is count")
        return self.statements.count()


    def mongo_to_object(self, statement_data):
        """
        Return Statement object when given data
        returned from Mongo DB.
        """
        Statement = self.get_model('statement')

        statement_data['id'] = statement_data['_id']
        print("This is mongo_to_object")

        return Statement(**statement_data)
    def filter(self, **kwargs):
        """
        Returns a list of statements in the database
        that match the parameters specified.
        """
        import pymongo

        page_size = kwargs.pop('page_size', 1000)
        print('page_size :',page_size)
        print('=============================================================')
        order_by = kwargs.pop('order_by', None)
        print('order_by :',order_by)
        print('==============================================================')
        tags = kwargs.pop('tags', [])
        print('tags :',tags)
        print('=============================================================')
        exclude_text = kwargs.pop('exclude_text', None)
        print('exclude_text :',exclude_text)
        print('==============================================================')
        exclude_text_words = kwargs.pop('exclude_text_words', [])
        print('exclude_text_words :',exclude_text_words)
        print('=============================================================')
        persona_not_startswith = kwargs.pop('persona_not_startswith', None)
        print('persona_not_startswith :',persona_not_startswith)
        print('=============================================================')
        search_text_contains = kwargs.pop('search_text_contains', None)
        print('search_text_contains :',search_text_contains)
        print('=============================================================')

        if tags:
            kwargs['tags'] = {
                '$in': tags
            }

        if exclude_text:
            if 'Solution' not in kwargs:
                kwargs['Solution'] = {}
            elif 'Solution' in kwargs and isinstance(kwargs['Solution'], str):
                Solution = kwargs.pop('Solution')
                kwargs['Solution'] = {
                    '$eq': Solution
                }
            kwargs['Solution']['$nin'] = exclude_text

        if exclude_text_words:
            if 'Solution' not in kwargs:
                kwargs['Solution'] = {}
            elif 'Solution' in kwargs and isinstance(kwargs['Solution'], str):
                Solution = kwargs.pop('Solution')
                kwargs['Solution'] = {
                    '$eq': Solution
                }
            exclude_word_regex = '|'.join([
                '.*{}.*'.format(word) for word in exclude_text_words
            ])
            kwargs['Solution']['$not'] = re.compile(exclude_word_regex)

        if persona_not_startswith:
            if 'persona' not in kwargs:
                kwargs['persona'] = {}
            elif 'persona' in kwargs and isinstance(kwargs['persona'], str):
                persona = kwargs.pop('persona')
                kwargs['persona'] = {
                    '$eq': persona
                }
            kwargs['persona']['$not'] = re.compile('^bot:*')

        if search_text_contains:
            or_regex = '|'.join([
                '{}'.format(word) for word in search_text_contains.split(' ')
            ])
            kwargs['search_text'] = re.compile(or_regex)

        mongo_ordering = []

        if order_by:

            # Sort so that newer datetimes appear first
            if 'created_at' in order_by:
                order_by.remove('created_at')
                mongo_ordering.append(('created_at', pymongo.DESCENDING, ))

            for order in order_by:
                mongo_ordering.append((order, pymongo.ASCENDING))

        total_statements = self.statements.find(kwargs).count()

        for start_index in range(0, total_statements, page_size):
            if mongo_ordering:
                for match in self.statements.find(kwargs).sort(mongo_ordering).skip(start_index).limit(page_size):
                    print("match if",match)
                    yield self.mongo_to_object(match)
            else:
                for match in self.statements.find(kwargs).skip(start_index).limit(page_size):
                    print('match else',match)
                    yield self.mongo_to_object(match)
        print("This is filter")
    def create(self, **kwargs):
        """
        Creates a new statement matching the keyword arguments specified.
        Returns the created statement.
        """
        Statement = self.get_model('statement')

        if 'tags' in kwargs:
            kwargs['tags'] = list(set(kwargs['tags']))

        if 'search_text' not in kwargs:
            kwargs['search_text'] = self.tagger.get_bigram_pair_string(kwargs['Solution'])

        if 'search_in_response_to' not in kwargs:
            if kwargs.get('question'):
                kwargs['search_in_response_to'] = self.tagger.get_bigram_pair_string(kwargs['question'])

        inserted = self.statements.insert_one(kwargs)

        kwargs['id'] = inserted.inserted_id
        print("This is create")

        return Statement(**kwargs)


    def create_many(self, statements):
        """
        Creates multiple statement entries.
        """
        create_statements = []

        for statement in statements:
            statement_data = {
                'Solution': statement.Solution,
                'search_text': statement.search_text,
                'conversation': statement.conversation,
                'persona': statement.persona,
                'question': statement.question,
                'search_in_response_to': statement.search_in_response_to,
                'created_at': statement.created_at,
                'tags': list(set(statement.tags))
            }
            if not statement.search_text:
                statement_data['search_text'] = self.tagger.get_bigram_pair_string(statement.Solution)

            if not statement.search_in_response_to and statement.question:
                statement_data['search_in_response_to'] = self.tagger.get_bigram_pair_string(statement.question)

            create_statements.append(statement_data)

        self.statements.insert_many(create_statements)
        print("This is create_many")
    def update(self, statement):
        data = statement.serialize()
        data.pop('id', None)
        data.pop('tags', None)

        data['search_text'] = self.tagger.get_bigram_pair_string(data['Solution'])

        if data.get('question'):
            data['search_in_response_to'] = self.tagger.get_bigram_pair_string(data['question'])

        update_data = {
            '$set': data
        }

        if statement.tags:
            update_data['$addToSet'] = {
                'tags': {
                    '$each': statement.tags
                }
            }

        search_parameters = {}

        if statement.id is not None:
            search_parameters['_id'] = statement.id
        else:
            search_parameters['Solution'] = statement.Solution
            search_parameters['conversation'] = statement.conversation

        update_operation = self.statements.update_one(
            search_parameters,
            update_data,
            upsert=True
        )

        if update_operation.acknowledged:
            statement.id = update_operation.upserted_id
        print("This is update")

        return statement
    def get_random(self):
        """
        Returns a random statement from the database
        """
        from random import randint

        count = self.count()

        if count < 1:
            raise self.EmptyDatabaseException()

        random_integer = randint(0, count - 1)

        statements = self.statements.find().limit(1).skip(random_integer)
        print("This is get_random")

        return self.mongo_to_object(list(statements)[0])


    def remove(self, statement_text):
        """
        Removes the statement that matches the input Solution.
        """
        self.statements.delete_one({'Solution': statement_text})
        print("This is remove")


    def drop(self):
        """
        Remove the database.
        """
        self.client.drop_database(self.database.name)
        print("This is drop")
