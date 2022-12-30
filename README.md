# Movie progress timer

* Create a text file somewhere within the script directory
* Set OBS to use it as a source for a text label.
/.config/obs-studio/<...>.json will look something like this
```
{
            "id": "text_ft2_source",
            "name": "counter",
            "settings": {
                "font": {
                    ...
                },
                "from_file": true,
                "text": "1:00:14/1:32:10",
                "text_file": "~/streams/movie-progress.txt",
                "undo_sname": "counter"
            },
},
```
* Change `file_path` and `movie_length` within the script to the appropriate values
* `python3 update_progress.py`
