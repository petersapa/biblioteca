from django.shortcuts import render, redirect
from .models import Prestec, Llibre, Alumne
from django.utils import timezone

def menu_principal(request):
    return render(request, 'biblioteca/menu.html')

def prestar_llibre(request):
    if request.method == 'POST':
        id_llibre = request.POST['llibre_id']
        id_alumne = request.POST['alumne_id']
        llibre = Llibre.objects.get(id=id_llibre)
        alumne = Alumne.objects.get(id=id_alumne)

        Prestec.objects.create(llibre=llibre, alumne=alumne)
        llibre.prestat = True
        llibre.save()
        return redirect('menu_principal')

    llibres_disponibles = Llibre.objects.filter(prestat=False)
    alumnes = Alumne.objects.all()
    return render(request, 'biblioteca/prestar.html', {'llibres': llibres_disponibles, 'alumnes': alumnes})

def tornar_llibre(request):
    if request.method == 'POST':
        id_prestec = request.POST['prestec_id']
        prestec = Prestec.objects.get(id=id_prestec)
        prestec.data_devolucio = timezone.now().date()
        prestec.save()

        llibre = prestec.llibre
        llibre.prestat = False
        llibre.save()
        return redirect('menu_principal')

    prestecs_actius = Prestec.objects.filter(data_devolucio__isnull=True)
    return render(request, 'biblioteca/tornar.html', {'prestecs': prestecs_actius})

def llistat_prestats(request):
    prestecs = Prestec.objects.filter(data_devolucio__isnull=True)
    return render(request, 'biblioteca/llistat_prestats.html', {'prestecs': prestecs})
