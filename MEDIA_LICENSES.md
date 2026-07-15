# Media Licenses

Media files referenced in point YAMLs (images, etc.) are NOT covered by the repository's
CC-BY-4.0 data license. Each media item carries its own license, declared in the point
YAML's `media[].license` and `media[].licenseUrl` fields.

## Common licenses used in this repository

| License ID       | Full name                                         | URL                                                         |
|------------------|---------------------------------------------------|-------------------------------------------------------------|
| CC0-1.0          | Creative Commons Zero v1.0 Universal              | https://creativecommons.org/publicdomain/zero/1.0/          |
| CC-BY-2.0        | Creative Commons Attribution 2.0 Generic          | https://creativecommons.org/licenses/by/2.0/                |
| CC-BY-3.0        | Creative Commons Attribution 3.0 Unported         | https://creativecommons.org/licenses/by/3.0/                |
| CC-BY-4.0        | Creative Commons Attribution 4.0 International    | https://creativecommons.org/licenses/by/4.0/                |
| CC-BY-SA-3.0     | Creative Commons Attribution-ShareAlike 3.0       | https://creativecommons.org/licenses/by-sa/3.0/             |
| CC-BY-SA-4.0     | Creative Commons Attribution-ShareAlike 4.0       | https://creativecommons.org/licenses/by-sa/4.0/             |

## Policy

- Only CC0, CC-BY, or CC-BY-SA licensed media may be included in production packs.
- CC-BY-SA media in `compact` distribution packs requires the downstream app to display
  license attribution; the `media[].creator` and `media[].licenseUrl` fields are included
  in the generated points.json for this purpose.
- When a media file is downloaded and stored in the repository, its SHA-256 is recorded
  in `media[].originalSha256`. Never modify a downloaded media file without updating this hash.
