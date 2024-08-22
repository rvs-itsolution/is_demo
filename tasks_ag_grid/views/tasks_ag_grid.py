from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from integration_utils.bitrix24.models import BitrixUserToken
from datetime import datetime
import json
from django.core.serializers.json import DjangoJSONEncoder
from tasks_ag_grid.utils.utils import get_status
from django.conf import settings


@main_auth(on_start=True, set_cookie=True)
def tasks_grid(request):
    """
    View-функция для создания списка json файлов с информацией об отрытых задачах.
    Каждый json файл имеет ключи: 'ID','TITLE', 'STATUS', 'CREATED_NAME', 'CREATED_LINK',
    'RESPONSIBLE_NAME', RESPONSIBLE_LINK', 'CREATED_DATE', 'DEADLINE'.
    """
    if request.method == 'POST':
        but = BitrixUserToken.objects.first()
        select_fields = ['ID', 'TITLE', 'STATUS', 'CREATED_BY', 'RESPONSIBLE_ID', 'CREATED_DATE', 'DEADLINE']
        my_filter = {'<REAL_STATUS': 5}
        tasks = but.call_list_method('tasks.task.list',
                                     {
                                         'select': select_fields,
                                         'filter': my_filter,
                                     })['tasks']
        task_list = []

        for task in tasks:
            task_info = {}
            for f in select_fields[:2]:
                task_info[f] = task[f.lower()]

            task_info['STATUS'] = get_status(task['status'])
            task_info['CREATED_NAME'] = task['creator']['name']
            task_info['CREATED_LINK'] = f"https://{settings.APP_SETTINGS.portal_domain}{task['creator']['link']}"

            task_info['TASK_LINK'] = f"{task_info['CREATED_LINK']}tasks/task/view/{task['id']}/"

            task_info['RESPONSIBLE_NAME'] = task['responsible']['name']
            task_info['RESPONSIBLE_LINK'] = f"https://{settings.APP_SETTINGS.portal_domain}{task['responsible']['link']}"

            task_info['CREATED_DATE'] = datetime.fromisoformat(task['createdDate']).strftime('%Y.%m.%d %H:%M:%S')
            task_info['DEADLINE'] = datetime.fromisoformat(task['deadline']).strftime('%Y.%m.%d %H:%M:%S')
            task_list.append(task_info)

        json_tasks = json.dumps(task_list, cls=DjangoJSONEncoder)
        return render(request, 'home.html', context={'json_tasks': json_tasks})
