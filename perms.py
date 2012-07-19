
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

"""
Agrega todos los permisos necesarios que por defecto no se agregan

#en shell
>>> include perms
"""

perms = [
    #['Agregar Medico', 'add_medic', 'auth', 'user'],
    #['Modificar Medico', 'change_medic', 'auth', 'user'],
    #['Borrar Medico', 'delete_medic', 'auth', 'user'],
    #['Mostrar Medico', 'show_medic', 'auth', 'user'],
    #permisos ya agregados

]


for perm in perms:
    somemodel_ct = ContentType.objects.get(app_label=perm[2], model=perm[3])
    my_perm = Permission(name=perm[0], codename=perm[1], content_type=somemodel_ct)
    print my_perm
    my_perm.save()