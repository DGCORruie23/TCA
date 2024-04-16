from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from django.contrib.auth.models import User
from usuarios.models import usuarioL
from usuarios.models import Usuario
from usuarios.models import Registro

# Create your views here.
@login_required
def dashboard(request):

    if request.method == 'GET':
        data = Registro.objects.all()
        print('hola')

        print(data)

        context = {
            "registro": data,
                }
        return render(request, "dashboard/dashboard.html", context)
    

