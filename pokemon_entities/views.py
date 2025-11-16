import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from django.utils.timezone import localtime


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    today_time = localtime()
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lt=today_time, disappeared_at__gt=today_time)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemons_on_page = []
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = Pokemon.objects.get(id=pokemon_id)
    today_time = localtime()
    pokemon_entities = PokemonEntity.objects.filter(pokemon=requested_pokemon, appeared_at__lt=today_time, disappeared_at__gt=today_time)

    pokemon = {
        'img_url': request.build_absolute_uri(requested_pokemon.image.url),
        'title_ru': requested_pokemon.title,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'description': requested_pokemon.description
    }

    previous_evolution = requested_pokemon.previous_evolution
    if previous_evolution:
        pokemon['previous_evolution'] = {
            "title_ru": previous_evolution.title,
            "pokemon_id": previous_evolution.id,
            "img_url": request.build_absolute_uri(previous_evolution.image.url),
        }

    next_evolutions = requested_pokemon.next_evolution.first()
    if next_evolutions:
        pokemon['next_evolution'] = {
            "title_ru": next_evolutions.title,
            "pokemon_id": next_evolutions.id,
            "img_url": request.build_absolute_uri(next_evolutions.image.url),
        }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(requested_pokemon.image.url)
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
