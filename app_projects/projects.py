from django.utils.translation import gettext_lazy as _


PROJECT_CATEGORIES = {
    'web': _('Веб-программирование'),
    'python': _('Python'),
    'php': _('PHP'),
}

PROJECT_TYPES = {
    'web': {
        'simple_web': _('Простой веб-приложение (HTML/CSS/JS)'),
        'reactjs_web': _('ReactJS веб-приложение'),
        'nodejs_web': _('NodeJS веб-сервер'),
    },
    'python': {
        'simple_python': _('Python с стандартной библиотекой'),
        'django_python': _('Django веб-сервер'),
        'pygame_python': _('Создание графической игры (pygame)'),
    },
    'php': {
        'simple_php': _('Веб-сервер с PHP и MySQL'),
        'wordpress_php': _('CMS WordPress'),
        'laravel_php': _('Фреймворк Laravel'),
    }
}