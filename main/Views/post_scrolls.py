from django.utils import timezone

from rest_framework.response import Response
from rest_framework import status, exceptions

from main.models import Scrolls, User
from main.serializer import *
import tasks


def upload_video(request):
    """
    Uploads the video requested and starts conversion.
    If successfully launched, the method returns the
    convertion task id. This does not garauntees the
    success of the video conversion.
    """
    try:
        if request.method == 'POST':

            assert(request.data['video_to_upload'] and request.data['title'])

            unprocessed_video = request.data['video_to_upload']
            title = request.data['title']
            # only in production!
            user_id = 2
            # in production,
            # user_id = user_id from token

            video = VideoMedia.objects.create(video=unprocessed_video, title=title, user_id=user_id)

            if not video:
                return Response({'message': 'error occured during video uploading'},
                                status=status.HTTP_400_BAD_REQUEST)

            if conversion_task_id := VideoMedia.objects.convert(video.id):
                return Response({'task_id': f'{conversion_task_id}'}, 
                    status=status.HTTP_200_OK)
            
            VideoMedia.objects.delete(video.id)

        return Response({'message': 'wrong method call'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED)

    except:
        return Response({'message': 'argument missing'}, 
            status=status.HTTP_400_BAD_REQUEST)

    
def scrollify_video(request):
    """
    If called in the right order, this method should have been called
    after the upload_video method.
    """

    try:
        task_id = request.data['task_id']
        title = request.data['title']
        height = request.data['height']
        fps = request.data['fps']
        quality = request.data['quality']
        media_id = tasks.get_result_from_task_id(task_id)

        if tasks.task_status(task_id) in [3,4]:
            return Response({'message': 'task is being run or waiting inside the queue'},
                status=status.HTTP_102_PROCESSING)

        if not media_id:
            VideoMedia.objects.delete(media_id)
            return Response({'message': 'error occured in conversion process, try uploading again'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        scrolls_object = Scrolls.objects.create(media_id=media_id, title=title, height=height)
        
        if not scrolls_object:
            return Response({'message': 'media object does not exist, possibly deleted'},
                status=status.HTTP_404_NOT_FOUND)
        
        if scrollify_task_id := VideoMedia.objects.mp4_to_scrolls(media_id=media_id, scrolls_id=scrolls_object.id, fps=fps, quality=quality):
            return scrollify_task_id

        # This deletes not only the scrolls but also related VideoMedia too.
        # Users have to re-upload from the begining when they reach here.
        Scrolls.objects.delete(scrolls_object.id)
        
        return Response({'message': 'scrollify process not launched, try uploading again'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    except:
        return Response({'message': 'argument missing'}, 
            status=status.HTTP_400_BAD_REQUEST)



def upload_scrolls(request):
    """
    """
    try:
        task_id = request.data['task_id']
        scrolls_id = request.data['scrolls_id']

        if tasks.task_status(task_id) in [3,4]:
            return Response({'message': 'task is being run or waiting inside the queue'},
                status=status.HTTP_102_PROCESSING)
        
        scrolls_dirname = tasks.get_result_from_task_id(task_id)
        
        if not scrolls_dirname:
            return Response({'message': 'scrollify process was not successful, try uploading again'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if (upload_task_id := Scrolls.objects.upload(scrolls_id=scrolls_id, scrolls_dirname=scrolls_dirname, wait=False)):
            return upload_task_id
        
        return Response({'message': f'scrolls with id {scrolls_id} not found, try uploading again'},    
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except:
        return Response({'message': 'argument missing'}, 
            status=status.HTTP_400_BAD_REQUEST)

