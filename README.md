# Scraping del sitemap de biobiochile.cl

Por default los datos de guardan en la carpeta /opt/scraped_data/ se puede cambiar en settings.py

El script permissions.sh es una utilidad para los permisos de escritura a la carpeta /opt/scraped_data/ si el usuario no es root

Dentro del ambiente virtual (venv - poetry), ejecutar el siguiente comando:

```bash
python scraping/biobio/biobio/run_sitemap.py
```
