# Changelog

## 0.2.0 - 2020-01-15

**Added**
 * Added use default colors
 * Added form improvements (no character limit, display character count)
 * Added improved error handling

**Breaking**
 * Default data file location was moved from `~/.config/duro/data.db` to `~/.local/share/duro/data.db`.
   If you are coming from a previous version, you will need to move the file manually.

**Fixed**
 * Fixed crashes when card length exceeds window width by 1 character.
 * Fixed crashes when action preformed but no board is selected.

## 0.1.1 - 2020-01-13

**Fixed**
 * Running `duro` after `pip3 install duro` now works
