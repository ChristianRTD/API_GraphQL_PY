from flask import Flask, request, jsonify
import graphene

# Define the GraphQL scheme
class Book(graphene.ObjectType):
    title = graphene.String()
    author = graphene.String()

# We simulate a database
books_data = [
    {"title": "1984", "author": "George Orwell"},
    {"title": "Brave New World", "author": "Aldous Huxley"},
    {"title": "Fahrenheit 451", "author": "Ray Bradbury"},
]

# We define the query
class Query(graphene.ObjectType):
    books = graphene.List(Book)

    def resolve_books(self, info):
        return books_data

# Crear el esquema GraphQL
schema = graphene.Schema(query=Query)

# Start the Flask application
app = Flask(__name__)

# Endpoint de GraphQL (permite GET y POST)
@app.route("/graphql", methods=["GET", "POST"])
def graphql_server():
    if request.method == "GET":
        # Simple response to GET method in the browser
        return """
        <h1>GraphQL Server</h1>
        <p>Usa una herramienta como Postman o cURL para realizar consultas POST al servidor.</p>
        <p>Prueba con una consulta GET usando la URL: <br>
        <code>/graphql?query={books{title author}}</code></p>
        """

    elif request.method == "POST":
        # Process POST requests with GraphQL queries
        data = request.get_json()
        query = data.get("query")
        result = schema.execute(query)
        return jsonify(result.data)

# Process GET queries directly from the URL
@app.route("/graphql", methods=["GET"])
def graphql_get():
    query = request.args.get("query")  # Get the query string from the URL
    if query:
        result = schema.execute(query)
        return jsonify(result.data)
    return "No query provided. Use /graphql?query={books{title author}}", 400

if __name__ == "__main__":
    app.run(debug=True)
