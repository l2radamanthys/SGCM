

keys = [
            'type_doc',
            'nro_doc',
            'gender',
            'phone',
            'address',
            'city',
            'state',
            'birth_date',
            'matricula',
]

f = open("keyform.txt", "w")
txt = "%s = dform.cleaned_data['%s']\n" 
for key in keys:
    f.write(txt %(key,key))
f.close()
