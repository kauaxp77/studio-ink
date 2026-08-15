from django.shortcuts import render
from .models import Work, ArtistProfile, Certification

def portfolio_index(request):
    works = Work.objects.all()
    artist_profile = ArtistProfile.objects.first()
    certifications = Certification.objects.all()
    
    return render(request, 'portfolio/index.html', {
        'works': works,
        'artist_profile': artist_profile,
        'certifications': certifications
    })
