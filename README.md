# Random wallpaper

Downloads random wallpaper in directory.


## Usage

```text
python random_wallpaper [dir] [timeframe]
```

| Argument | Description |
| --- | --- |
| `dir` | Path-like string of destination directory. |
| `timeframe` | Reddit's timeframe, valid values: `hour`, `day`, `week`, `month`, `year`, `all`. |

*See: <https://www.jcchouinard.com/documentation-on-reddit-apis-json/>*

## Example

```sh
python random_wallpaper.py "~/wallpaper" week
```


## Detailed help

```sh
python random_wallpaper.py -h
```

