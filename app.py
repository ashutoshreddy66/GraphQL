from flask import Flask
from flask_graphql import GraphQLView
from collections.abc import MutableMapping
import graphene

# Step 1: Define the Book type
class Book(graphene.ObjectType):
    id = graphene.ID()
    title = graphene.String()
    author = graphene.String()

# In-memory storage for books
books = []

# Step 2: Define Mutations to create and delete books
class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author = graphene.String(required=True)

    book = graphene.Field(lambda: Book)

    def mutate(self, info, title, author):
        new_book = Book(id=len(books) + 1, title=title, author=author)
        books.append(new_book)
        return CreateBook(book=new_book)

class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        global books
        books = [book for book in books if str(book.id) != id]
        return DeleteBook(ok=True)

# Step 3: Define Query to get the list of all books
class Query(graphene.ObjectType):
    all_books = graphene.List(Book)

    def resolve_all_books(self, info):
        return books

# Step 4: Define the Mutation class to handle all mutations
class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    delete_book = DeleteBook.Field()

# Step 5: Create the schema
schema = graphene.Schema(query=Query, mutation=Mutation)

# Step 6: Create the Flask app
app = Flask(__name__)

# Step 7: Add a GraphQL view to the Flask app
app.add_url_rule(
'/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True
))

# Step 8: Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
