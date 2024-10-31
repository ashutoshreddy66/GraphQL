import graphene

# Define a Person object type with fields for name, address, and age
class Person(graphene.ObjectType):
    name = graphene.String()
    address = graphene.String()
    age = graphene.Int()

# In-memory storage for created Person instances
people = []

# Define a CreatePerson mutation class to handle creation of new Person instances
class CreatePerson(graphene.Mutation):
    # Define the expected input arguments for the mutation
    class Arguments:
        name = graphene.String(required=True)
        age = graphene.Int(required=True)
        address = graphene.String()

    # Define the return type for the mutation
    person = graphene.Field(lambda: Person)

    # Mutation logic to create and add a new Person to the in-memory storage
    def mutate(self, info, name, address, age):
        new_person = Person(name=name, address=address, age=age)
        people.append(new_person)
        return CreatePerson(person=new_person)

# Mutation root type to include all defined mutations
class Mutation(graphene.ObjectType):
    create_person = CreatePerson.Field()

# Query root type to define the available queries
class Query(graphene.ObjectType):
    # Define a query that returns a list of all Person instances
    all_people = graphene.List(Person)

    # Resolver function to return all people from the in-memory storage
    def resolve_all_people(self, info):
        return people

# Create the GraphQL schema with the query and mutation types
schema = graphene.Schema(query=Query, mutation=Mutation)

# Function to execute a GraphQL query with optional variables
def execute_graphql_query(query, variables=None):
    result = schema.execute(query, variables=variables)
    # Return query results if no errors, otherwise return errors
    return result.data if not result.errors else result.errors

# Mutation template for creating a new Person
mutation_template = '''
    mutation CreatePerson($name: String!, $age: Int!, $address:String) {
        createPerson(name: $name, age: $age, address:$address) {
            person {
                name
                age
                address
            }
        }
    }
'''

# Define list of people to be added via mutations
persons_to_add = [{"name": "Alice", "age": 25, "address": "1234"}, {"name": "Dexter", "age": 35, "address": "5678"}]
# Execute the mutation for each person in the list
for person in persons_to_add:
    mutation_result = execute_graphql_query(mutation_template, variables=person)
    print("Mutation result:", mutation_result)

# Query to fetch all people
all_people_query = '''
    query {
        allPeople {
            name
            age
            address
        }
    }
'''

# Execute the query to get all Person instances and print the result
query_result = execute_graphql_query(all_people_query)
print("All People:", query_result)
