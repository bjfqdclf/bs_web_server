public_url = [
    '/login/',
    '/logout/',
    '/not_find/',
    '/edit_passwd_ajax/'
]

err_url = [
    '/404/',
    '/401/'
]

role_url_dict = {
    1: [  # admin_url
        '/admin/home/',
        '/admin/add/user/',
        '/admin/edit_passwd/',
        '/admin/class_manage/',
        '/admin/add_class_ajax/',

    ],
    2: [  # teacher_url
        '/teacher/home/',
        '/teacher/edit_passwd/',
    ],
    3: [  # student_url
        '/student/home/',
        '/student/edit_passwd/',
    ]
}
