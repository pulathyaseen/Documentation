
class DesignationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        items = Designation.objects.all()

        if self.q:
            items = items.filter(Q(name__istartswith=self.q))

        return items

    def create_object(self, text):
        text = text.title()
        if not Designation.objects.filter(name=text):
            return Designation.objects.create(
                name=text,
            )

