This plugin for QGIS 3.x regroup all points linked one to another because they are within a given distance from one another, it gives them a commun aggregate id attribute.
This plugins pick a point, the first of the aggregate, and seek, in the distance of research chosen by the user, another one. If this second point is found, is added to the aggregate and the loop starts again untill no more points are added.
The plugin loop untill all points are treated.
This plugin also produces a line layer and a polygon layer to overlap the points and visualize the aggregates.
This plugin was meant to deal with near faunistic or floristic datas, that the user wanted to be regrouped as a station.
The user should cheack that the distance chosen is kept as small as possile in order to avoid to extended groups as chain-group effect can compromise the results.
WARNING !: it Works with projected datas only, in other words do not use geographical (long-lat type) reference systems !

