import graphene
from graphene_django import DjangoObjectType

from .models import MentorshipSession
from graphql_jwt.decorators import login_required

class MentorshipType(DjangoObjectType):
    class Meta:
        model = MentorshipSession
        fields = "__all__"
        

class CreateMentorshipSession(graphene.Mutation):
    class Arguments:
        requesting_user_id = graphene.ID(required=True)
        mentor_id = graphene.ID(required=True)
        topic = graphene.String(required=True)
        description = graphene.String(required=True)
        scheduled_time = graphene.String(required=True)

    mentorship_session = graphene.Field(MentorshipType)
    
    @login_required
    def mutate(root, info, requesting_user_id, mentor_id, topic, description, scheduled_time):       
        mentorship_session = MentorshipSession(
            requesting_user_id=requesting_user_id,
            mentor_id=mentor_id,
            topic=topic,
            description=description,
            scheduled_time=scheduled_time,
            is_accepted=None  
        )
        mentorship_session.save()
        return CreateMentorshipSession(mentorship_session=mentorship_session)
    

class AddReview(graphene.Mutation):
    class Arguments:
        mentor_id = graphene.ID(required=True)
        rating = graphene.Int(required=True)
        comment = graphene.String()

    review = graphene.Field(ReviewType)
    
    @login_required
    def mutate(root, info, mentor_id, rating, comment=None):       
        review = Review(
            mentor_id=mentor_id,
            mentee_id=info.context.user.id,  # Assuming the mentee is the logged-in user
            rating=rating,
            comment=comment
        )
        review.save()
        return AddReview(review=review)

class AcceptMentorshipSession(graphene.Mutation):
    class Arguments:
        mentorship_session_id = graphene.ID(required=True)

    mentorship_session = graphene.Field(MentorshipType)
    
    @login_required
    def mutate(root, info, mentorship_session_id):       
        mentorship_session = MentorshipSession.objects.get(pk=mentorship_session_id)
        mentorship_session.is_accepted = True
        mentorship_session.save()
        return AcceptMentorshipSession(mentorship_session=mentorship_session)

class DeclineMentorshipSession(graphene.Mutation):
    class Arguments:
        mentorship_session_id = graphene.ID(required=True)

    mentorship_session = graphene.Field(MentorshipType)
    
    @login_required
    def mutate(root, info, mentorship_session_id):       
        mentorship_session = MentorshipSession.objects.get(pk=mentorship_session_id)
        mentorship_session.delete()
        return DeclineMentorshipSession(mentorship_session=None)

class ViewPreviousSessions(graphene.ObjectType):
    mentorship_sessions = graphene.List(MentorshipType)

    @login_required
    def resolve_mentorship_sessions(self, info):        
        user = info.context.user
        return MentorshipSession.objects.filter(requesting_user=user)

class DeleteReview(graphene.Mutation):
    class Arguments:
        review_id = graphene.ID(required=True)

    review = graphene.Field(ReviewType)

    @login_required
    def mutate(root, info, review_id):
        review = Review.objects.get(pk=review_id)
        review.delete()
        return DeleteReview(review=None)

class ViewRequestedSessions(graphene.ObjectType):
    mentorship_sessions = graphene.List(MentorshipType)

    @login_required
    def resolve_mentorship_sessions(self, info):        
        user = info.context.user
        return MentorshipSession.objects.filter(mentor=user)    

class Mutation(graphene.ObjectType):
    create_mentorship_session = CreateMentorshipSession.Field()
    add_review = AddReview.Field()
    accept_mentorship_session = AcceptMentorshipSession.Field()
    decline_mentorship_session = DeclineMentorshipSession.Field()
    delete_review = DeleteReview.Field()


class Query(graphene.ObjectType):    
    view_previous_sessions = ViewPreviousSessions.Field()    
    view_requested_sessions = ViewRequestedSessions.Field()
    
schema = graphene.Schema(query=Query, mutation=Mutation)