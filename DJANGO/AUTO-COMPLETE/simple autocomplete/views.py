class DoctorsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Doctor.objects.none()

        items = Doctor.objects.filter(is_deleted=False)

        if self.q:
            query = self.q
            items = items.filter(Q(name__istartswith=query))

        return items
