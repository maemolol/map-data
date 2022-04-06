# Mapping guide

## Setting up your dataset

Firstly, decide on a namespace. Ideally they are 3 letters long, and will always appear at the start of every component (and node) that you will be plotting. This is to make sure that no two components have the same ID across the map.

A list of namespaces can be found in #namespace-list in the MRT Mapping Services discord.

## Mapping the place (Stencil)

Stencil is an online map data editor made by \_\_7d. You can access it online at [https://mrt-map.github.io/stencil].

The current version as of writing is **v1.1b4**.

A manual should already be provided in Stencil itself. Give it a read, and start plotting your components.

After plotting, export the data (there should be two files).

## Uploading the data

Fork this repository and commit and push your files in there. Components go to the `comps` (or `pla`) folder, and nodes go to the `nodes` folder.

When you are done, create a pull request onto this main repository. After 7d handchecks the data for any mistakes or noncompliances, the data is merged and will be rendered in the next scheduled render.

## Component ID naming guidelines
**Remember namespace prefix!** Prefix them like this: `<namespace>-<node name>`, eg `enc-cabrilloAv`
**No spaces in IDs**
**Roads** just state the name: `<name>`. Eg `enc-cabrilloAv`
**Double-lined roads, eg A/B roads** use `<name><n|s|e|w>`, eg `B209n`.
**Buildings, parks, platforms, etc** just state the name too: `<name>`. if you have similar buildings with no names ID them with A B C D etc. Eg `enc-officeB`
**Grouping componentss** Use `<group name>-<name etc>`, eg. `frn-cityHall-pondA1-sidewalkB8`

## Steps to map a city
1a. Map the roads. They are linear components. if there is an intersection, two roads can go onto one road.
- A list of road types: localHighwaySlip, bRoadSlip, aRoadSlip, localPedestrianQuaternaryRoad, localQuaternaryRoad, localPedestrianTertiaryRoad, localTertiaryRoad, localSecondaryRoad, localMainRoad, localHighway, bRoad, aRoad, rail
- If it is one-way, append the type name with ` oneway` (including the space) For example, `localHighway oneway`
- If it is elevated or underground, append `_elevated` or `_underground`. For example, `localHighway_underground`
- Road crossing? Use `pedestrianCrossing` (point component) on a node where there is a crossing
- Dont map sidewalks!
- Highways should be mapped with two components, both oneway
1b. Map the paths in the city. This includes alleyways, park paths, but **not sidewalks**
- The type is `pathway`. `_elevated` or `_underground` can also be appended.
-  If your path is in the park you can map it together with the park
2a. Map the railways going through the town. The tracks are linear as well. 
- The only type is `rail`.
- `_elevated` and `_underground` also can be appended too.
- Rail crossing? Use `railCrossing` (point component)
2b. Map the stations in the town.
- The type for station buildings is `transportBuilding` and for platforms is `platform`. If you have underground structures, append `_underground`.
- The platform and the track components should share nodes, ie they shd be connected.
- Mark stations with `railStation` (its a point component, ie it only requires one node), and `undergroundExit` for underground exits
3a. Map the buildings.
- The type is `building`. There is also an `_underground` prefix. For city halls, use `cityHall`.
- The buildings should not connect to the road.
- This requires a lot of nodes :P
- If you have rooftop gardens, map those as well.
3b. Map the parks.
- The type for the area is `park`. (Not a point component).
- If you have a national park, don't map it yet.
- If you have a plaza, use `plaza`.
4. Mark individual services (optional)
- All are point components. They are parking, bikeRack, shop, restaurant, hotel, arcade, supermarket, clinic, library, placeOfWorship, petrol, cinema, bank, gym, shelter, playground, fountain, taxiStand, pickUpDropOff, attraction
5. Map the zones of the city.
- Types: residentialArea, industrialArea, commercialArea, officeArea, residentialOfficeArea, schoolArea, healthArea, agricultureArea, militaryArea
- If you have a national park area dont use this
- You can anchor to other nodes for this, if possible.
6. Map heliports, seaplane ports, waterports, airports and bus stops.
- Types: gate, apron, taxiway, runway, helipad. Gate and Helipad are area components btw, not a point. Taxiway and runway are lines
- For buildings use `transportBuilding`
- Mark bus stops and waterports with `ferryStop` or `busStop`
- If it is a local ferry you can also map the route with `ferryLine`
7. Map the natural features around your town. This includes national parks and empty patches
- Types: grass, shrub, forest, stone, sand
- If you have lakes use `waterSmall`, if you are next to a large ocean use `waterLarge`
- If you have a small island use `landSmall`; or if its large (like Kazeshima) use `landLarge`
8. Map the subdivisions and town borders. 
- Types: `subdistrict`, `district`, `town`
- They are area components btw

## Important things to remember
- Always namespace all nodes and componentss. This can be done by providing a 3-letter prefix followed by a dash. For example, `abc-IdkRoad` instead of just `IdkRoad`.
- If you are mapping, do check with me often if the format is correct. You might be mapping it wrong, who knows?
- You can reference nodes from another namespace.

## FAQ
* **This Github thing is too convoluted for me!** You can just dm it to 7d, he will check and upload it for you :)
