Sources: 
1. fights.csv: turf war outcomes that have been observed in the games.
- https://monsterhunter.fandom.com/wiki
- https://www.youtube.com/watch?v=KX0GsR6atAw

2. monster: contains information about monsters.

| name | type | elements | weakness | size |  
|------|------|----------|----------|------|
| cat  | cat  | binary   | num      | num  |

It's highly recommended to normalize weakness feature twice (once for row normalization
of `[fire_weak, water_weak, thunder_weak, ice_weak, dragon_weak]`, and another
for column normalization. This is because the values represent the sum of elemental weaknesses 
of the monsters, and each monster varies in the number of parts it has.)

- https://github.com/TanukiSharp/mh-monster-info/tree/master/src/assets/data
- https://mhrise.mhrice.info/
- https://github.com/CrimsonNynja/monster-hunter-DB
- https://monsterhunterwiki.org/wiki
- https://github.com/Kolyn090/mhfu-db

3. subspecies.csv: record of monsters' subspecies
- https://github.com/CrimsonNynja/monster-hunter-DB

4. size: contains information about size of monsters.

Missing information are approximated via a missing-data imputation method. For some monsters that
have a fixed in the game, the algorithm also approximated other expected sizes for them. For details,
check out size_combined_pred.csv file.

- https://github.com/Kolyn090/mhfu-db
- https://monsterhunter.fandom.com/wiki
- https://monsterhunterrise.wiki.fextralife.com/
- https://mhworld.kiranico.com/
