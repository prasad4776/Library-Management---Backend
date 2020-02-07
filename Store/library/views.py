from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from .models import Book, Author, BooksIssued, User
from .serializers import BookSerializer, AuthorSerializer, IssueSerializer
from rest_framework.views import APIView
from .serializers import LoginSerializer
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response


class BookViewSet(ViewSet):
    serializer_class = BookSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def list(self, request):
        if request.user.is_staff:
            queryset = Book.objects.all()
            serializer = BookSerializer(queryset, many=True)
        else:

            book_ids = BooksIssued.objects.filter(person_id=request.user).values_list('book_id', flat=True)
            queryset = Book.objects.filter(id__in=list(book_ids))
            serializer = BookSerializer(queryset,many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        print(data)
        queryset = Book.objects.create(book_name=data['book_name'], price=data['price'])
        serializer = BookSerializer(queryset)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Book.objects.get(id=pk)
        print(queryset)
        serializer = BookSerializer(queryset)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        queryset = Book.objects.get(id=pk).delete()
        return Response({'message': 'successfully deleted', 'status': 200, 'queryset': queryset})

    # def partial_update(self, request, pk=None):
    #     book = get_object_or_404(Book, pk=pk)
    #     book.b_name = request.data['b_name']
    #     book.save()
    #     serializer = BookSerializer(book)
    #     return Response(serializer.data)

    def update(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        book.book_name = request.data['book_name']
        book.price = request.data['price']
        book.save()
        serializer = BookSerializer(book)
        return Response(serializer.data)


class AuthorViewSet(ViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def list(self, request):
        queryset = Author.objects.all()
        serializer = AuthorSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        author = Author.objects.create(first_name=data['first_name'], last_name=data['last_name'])
        author.book.add(data['book'])
        author.save()
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Author.objects.get(id=pk)
        print(queryset)
        serializer = AuthorSerializer(queryset)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        queryset = Author.objects.get(id=pk).delete()
        return Response({'message': 'successfully deleted', 'status': 200, 'queryset': queryset})

    def update(self, request, pk=None):
        author = get_object_or_404(Author, pk=pk)
        author.first_name = request.data['first_name']
        author.last_name = request.data['last_name']
        author.book.add(request.data['book'])
        author.save()
        serializer = AuthorSerializer(author)
        return Response(serializer.data)


class IssueViewSet(ViewSet):
    queryset = BooksIssued.objects.all()
    serializer_class = IssueSerializer

    def list(self, request):
        queryset = BooksIssued.objects.all()
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = BooksIssued.objects.get(id=pk)
        print(queryset)
        serializer = IssueSerializer(queryset)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        queryset = BooksIssued.objects.get(id=pk).delete()
        return Response({'message': 'successfully deleted', 'status': 200, 'queryset': queryset})

    def create(self, request):
        book = Book.objects.get(id=request.data['book_id'])
        person = User.objects.get(id=request.data['person_id'])
        issue = BooksIssued.objects.create(book_id=book, person_id=person,
                                           issue_date=request.data['issue_date'],
                                           submission_date=request.data['submission_date'])
        issue.save()
        serializer = IssueSerializer(issue)
        return Response(serializer.data)

    def update(self, request, pk=None):
        issue = get_object_or_404(BooksIssued, pk=pk)
        issue.issue_date = request.data['issue_date']
        issue.submission_date = request.data['submission_date']
        issue.book_id = Book.objects.get(id=request.data['book_id'])
        issue.person_id = User.objects.get(id=request.data['person_id'])

        issue.save()
        serializer = IssueSerializer(issue)
        return Response(serializer.data)


class ObtainAuthToken(APIView):

    def post(self, request, *args, **kwargs):
        # serializer = self.serializer_class(data=request.data,
        #                                    context={'request': request})
        serializer = LoginSerializer(data=request.data,
                                     context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, "user": request.data['username']})


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        print(request.data)
        django_logout(request)
        return Response({"msg": "logout", "user": request.data['username']}, status=204)

# class LoginView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data["password"]
#         django_login(request, user)
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({"token": token.key, "username": request.data['username']}, status=200)
#
#
