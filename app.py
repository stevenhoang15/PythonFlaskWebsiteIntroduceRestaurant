# from schema import schema  # Import GraphQL schema
# from flask_graphql import GraphQLView # type: ignore
from routes import create_app

app = create_app()

#GraphQL
# app.add_url_rule(
#     '/graphql',
#     view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
# )

app.run(debug=True, port=5000)

