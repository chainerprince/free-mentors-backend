import graphene
from graphql_auth.schema import MeQuery, UserQuery
from graphql_auth import mutations
import mentoring.schema


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()    
    token_auth =  mutations.ObtainJSONWebToken.Field() 
    update_account = mutations.UpdateAccount.Field()

class Query(UserQuery,MeQuery,mentoring.schema.Query, graphene.ObjectType):
    pass

class Mutation(AuthMutation, mentoring.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
