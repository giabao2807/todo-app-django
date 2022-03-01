from datetime import datetime

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api_todo.models import Note
from api_todo.serializers.Note import NoteSerializer


class NoteViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    @action(detail=False, methods=['post'])
    def list_for_user(self, request, *args, **kwargs):
        user = request.user

        notes = Note.objects.filter(user__username=user.username)
        if notes.exists():
            return Response(NoteSerializer(notes, many=True).data, status=status.HTTP_200_OK)
        else:
            return Response({"error_message": "error in find list notes by user"}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        user = request.user

        note = request.data.get('note')
        deadline = request.data.get('deadline')
        something = request.data.get('something')

        new_note = Note(note=note, deadline=deadline, something=something, user=user)
        new_note.save()

        return Response(NoteSerializer(new_note).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def change_to_done(self, request, pk):
        user = request.user
        note = self.get_object()

        if note.user == user:
            note.is_done = True
            note.save()
            return Response({"message": "completed changing to done"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "invalid user"}, status=status.HTTP_400_BAD_REQUEST)
