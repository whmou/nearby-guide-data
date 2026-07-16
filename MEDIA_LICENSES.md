# Media Licenses

Media files referenced in point YAMLs (images) are NOT covered by the repository's
CC-BY-4.0 data license. Each media item carries its own license, declared in the point
YAML's `media[].license` and `media[].licenseUrl` fields.

All images are sourced from Wikimedia Commons under CC0 / Public Domain / CC-BY / CC-BY-SA
licenses. The table below is generated from `tools/image_metadata_cache.json` by
`tools/gen_media_licenses.py`. Do not edit it by hand.

## Policy

- Only CC0, CC-BY, or CC-BY-SA licensed media may be included in production packs.
- CC-BY-SA / CC-BY media require the downstream app to display attribution; the
  `media[].creator` and `media[].licenseUrl` fields are included in the generated
  points.json for this purpose.
- When a media file is downloaded, the SHA-256 of the **original** is recorded in
  `media[].originalSha256`. Never modify a downloaded original without updating this hash.
- Some original references were missing or pointed at a Category page; in those cases a
  suitable licensed replacement image was selected (marked ✔ in the *Replaced* column).


## Image attributions (107 points)

| Point ID | Title | Creator | License | Source (Wikimedia Commons) | Accessed | Replaced |
|----------|-------|---------|---------|-----------------------------|----------|:--------:|
| `jp-miyakojima-17end-beach` | 下地島17エンド | Cassiopeia sweet | Public domain | [source](https://commons.wikimedia.org/wiki/File:Shimojishima_Runway17.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-aragusuku-beach` | 新城海岸 | Raita Futo from Tokyo, Japan | CC BY 2.0 | [source](https://commons.wikimedia.org/wiki/File:Aragusuku_Beach_in_Miyako_(51924273449).jpg) | 2026-07-16 |  |
| `jp-miyakojima-awamori-distillery` | 多良川酒造 | jetalone from Ginza, Tokyo | CC BY 2.0 | [source](https://commons.wikimedia.org/wiki/File:Various_Awamori_bottles_by_jetalone_in_Ginza,_Tokyo.jpg) | 2026-07-16 |  |
| `jp-miyakojima-biyandam-viewpoint` | ビャクダン山展望台 | 663highland | CC BY 2.5 | [source](https://commons.wikimedia.org/wiki/File:Yonahamaehama_Miyakojima_Okinawa_Japan06s3s4592.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-botanical-bingata` | 紅型染色體驗工房 | Unknown Ryukyu artisans. Photo by Museum | Public domain | [source](https://commons.wikimedia.org/wiki/File:Bingata_kimono_Okinawa.png) | 2026-07-16 |  |
| `jp-miyakojima-city-museum` | 宮古島市総合博物館 | 663highland | CC BY 2.5 | [source](https://commons.wikimedia.org/wiki/File:Yonahamaehama_Miyakojima_Okinawa_Japan06s3s4592.jpg) | 2026-07-16 |  |
| `jp-miyakojima-coral-restoration` | 宮古島珊瑚礁再生プロジェクト | Sand Dollar Sports | CC BY 4.0 | [source](https://commons.wikimedia.org/wiki/File:Sand_Dollar_Sports_coral_reef_restoration_project.jpg) | 2026-07-16 |  |
| `jp-miyakojima-funasugi-banata` | フナウサギバナタ | 690 Noda | CC BY 3.0 | [source](https://commons.wikimedia.org/wiki/File:フナウサギバナタの断崖_20130207_-_panoramio.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-harimizu-utaki` | 漲水御嶽 | Hyppolyte de Saint-Rambert | CC BY 4.0 | [source](https://commons.wikimedia.org/wiki/File:Okinawa_Nanjo_Sefa-utaki_Gusuku_site_Yuinchi_07.jpg) | 2026-07-16 |  |
| `jp-miyakojima-head-tax-stone` | 人頭税石 | Paipateroma | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Nintouzeiseki.jpg) | 2026-07-16 |  |
| `jp-miyakojima-hennazaki-east` | 東平安名崎 | Metatron | CC BY-SA 3.0 | [source](https://commons.wikimedia.org/wiki/File:Miyako_higashi_hennazaki_lighthouse.JPG) | 2026-07-16 |  |
| `jp-miyakojima-hora-cave` | 保良泉鍾乳洞 | 663highland | CC BY 2.5 | [source](https://commons.wikimedia.org/wiki/File:Yonahamaehama_Miyakojima_Okinawa_Japan06s3s4592.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-hora-spring` | 保良泉 | 663highland | CC BY 2.5 | [source](https://commons.wikimedia.org/wiki/File:Miyako_Airport_Okinawa_Japan24s3s4592.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-ikema-beach` | 池間島ビーチ | ブルーノ・プラス | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Ikema_Bridge_in_Miyakojima.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-ikema-bridge` | 池間大橋 | Raita Futo from Tokyo, Japan | CC BY 2.0 | [source](https://commons.wikimedia.org/wiki/File:Ikema_Ohashi_Bridge_(51923938941).jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-ikema-dugong` | 池間島ジュゴン生息域 | Geoff Spiby / www.geoffspiby.co.za | CC BY-SA 3.0 | [source](https://commons.wikimedia.org/wiki/File:Dugong_dugon.jpg) | 2026-07-16 |  |
| `jp-miyakojima-ikema-island` | 池間島 | ブルーノ・プラス | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Ikema_Bridge_in_Miyakojima.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-ikema-wetland` | 池間湿地 | Paipateroma | CC BY-SA 3.0 | [source](https://commons.wikimedia.org/wiki/File:Miyako_ikema_shitsugen.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-irabu-bridge` | 伊良部大橋 | Paipateroma | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Miyako_irabu_ohashi_2014_1.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-irabu-diving` | 伊良部島ダイビング | Paipateroma | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Irabu_sarahama_port.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-irabu-island` | 伊良部島 | Image Science and Analysis Laboratory, NASA-Johnson Space Center. "The Gateway to Astronaut Photography of Earth." | Public domain | [source](https://commons.wikimedia.org/wiki/File:Irabu_Island_ISS045.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-irabu-katsuobushi` | 佐良浜かつお節文化 | Paipateroma | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Irabu_sarahama_port.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-irabu-lighthouse` | 伊良部島灯台 | Paipateroma | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Irabu_sarahama_port.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-irabu-panorama` | 伊良部大橋展望 | Rsa | CC BY-SA 3.0 | [source](https://commons.wikimedia.org/wiki/File:Irabu_ohashi_20120815.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-kaijin-no-mori` | 海人の森 | ブルーノ・プラス | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Ikema_Bridge_in_Miyakojima.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-kamama-ridge-park` | カママ嶺公園 | 663highland | CC BY 2.5 | [source](https://commons.wikimedia.org/wiki/File:Yonahamaehama_Miyakojima_Okinawa_Japan06s3s4592.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-kurima-bridge` | 来間大橋 | 690 Noda | CC BY 3.0 | [source](https://commons.wikimedia.org/wiki/File:来間大橋_20130206_-_panoramio.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-kurima-island` | 来間島 | Graeme Bartlett | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Miyakojima_Kurima_aerial.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-kurima-nagama-beach` | 長間浜 | Uzumaki~jawiki at Japanese Wikipedia | CC BY-SA 3.0 | [source](https://commons.wikimedia.org/wiki/File:Nagamahama.jpg) | 2026-07-16 |  |
| `jp-miyakojima-kurima-sugarcane` | 来間島サトウキビ畑 | lienyuan lee | CC BY 3.0 | [source](https://commons.wikimedia.org/wiki/File:Sugarcane_Hall,_Okinawa_World_20010614.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-kurima-viewpoint` | 来間島龍宮城展望台 | 663highland | CC BY 2.5 | [source](https://commons.wikimedia.org/wiki/File:Yonahamaehama_Miyakojima_Okinawa_Japan06s3s4592.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-mango-orchard` | 宮古マンゴー農園 | 663highland | CC BY 2.5 | [source](https://commons.wikimedia.org/wiki/File:Miyako_Airport_Okinawa_Japan24s3s4592.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-maou-palace-cave` | 魔王の宮殿（洞窟ダイビングスポット） | Paipateroma | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Irabujima_sky_view.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-marine-park` | 宮古島海中公園 | 663highland | CC BY 2.5 | [source](https://commons.wikimedia.org/wiki/File:Miyako_Airport_Okinawa_Japan24s3s4592.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-miyako-beef-ranch` | 宮古牛農場 | Cgoodwin | CC BY 3.0 | [source](https://commons.wikimedia.org/wiki/File:Wagyu.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-miyako-festival` | 宮古島まつり（クルバガー） | 663highland | CC BY 2.5 | [source](https://commons.wikimedia.org/wiki/File:Yonahamaehama_Miyakojima_Okinawa_Japan06s3s4592.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-miyako-horse` | 宮古馬 | Haidonan | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Miyako_uma.JPG) | 2026-07-16 | ✔ |
| `jp-miyakojima-miyako-shrine` | 宮古神社 | Tacara | CC BY-SA 3.0 | [source](https://commons.wikimedia.org/wiki/File:Miyakojinjya.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-miyako-soba` | 古謝そば屋（宮古そば） | Nesnad | CC BY 4.0 | [source](https://commons.wikimedia.org/wiki/File:Tebichi_soba_-_Miyako_island_-_Mar_27_2020_01-20_PM.jpeg) | 2026-07-16 | ✔ |
| `jp-miyakojima-miyako-traditional-textile` | 宮古上布 | 663highland | CC BY 2.5 | [source](https://commons.wikimedia.org/wiki/File:Yonahamaehama_Miyakojima_Okinawa_Japan06s3s4592.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-nakanoshima-channel` | 中の島チャンネル（ダイビングスポット） | Paipateroma | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Irabujima_sky_view.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-nakazone-tomb` | 仲宗根豊見親の墓 | 663highland | CC BY 2.5 | [source](https://commons.wikimedia.org/wiki/File:Yonahamaehama_Miyakojima_Okinawa_Japan06s3s4592.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-nishi-hennazaki` | 西平安名崎 | Haidonan | Public domain | [source](https://commons.wikimedia.org/wiki/File:Nishi-hen-na01.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-nishizato-market` | 西里公設市場 | 663highland | CC BY 2.5 | [source](https://commons.wikimedia.org/wiki/File:Yonahamaehama_Miyakojima_Okinawa_Japan06s3s4592.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-ogami-island` | 大神島 | 663highland | CC BY 2.5 | [source](https://commons.wikimedia.org/wiki/File:Ikemajima_and_Ogamijima_Okinawa_Japan01s3s4350.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-painagama-beach` | パイナガマビーチ | aco pbc | CC0 | [source](https://commons.wikimedia.org/wiki/File:A_small_market_along_a_street_in_Miyakojima_2016-05-15.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-sarahama-port` | 佐良浜漁港 | Paipateroma | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Irabu_sarahama_port_sun_marin_terminal.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-sawada-beach` | 佐和田の浜 | ブルーノ・プラス | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:The_entire_Sawada_beach.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-sea-kayak-mangrove` | 島尻マングローブ シーカヤック | Anagounagi | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Mangrove_swamp,_Iriomote_Island,_Okinawa,_Japan.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-sea-turtle-yoshino` | 吉野海岸（ウミガメ遭遇スポット） | Brocken Inaglory | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Total_internal_reflection_of_Chelonia_mydas.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-shimajiri-beach` | 前浜東岸 | Paipateroma | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Miyako_maipama_1.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-shimajiri-uganzaki` | 島尻のマングローブ林 | 663highland | CC BY 2.5 | [source](https://commons.wikimedia.org/wiki/File:Yonahamaehama_Miyakojima_Okinawa_Japan06s3s4592.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-shimoji-airport` | 下地島空港 | ブルーノ | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Shimojishima.airport.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-shimoji-cave-dive` | 下地島洞窟ダイビング入口 | Paipateroma | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Irabujima_sky_view.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-shimoji-island` | 下地島 | Paipateroma | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Irabujima_sky_view.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-shiratorisaki` | 白鳥崎 | Paipateroma | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Irabu_sarahama_port.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-snorkel-rental` | パイナガマ海水浴場 レンタル拠点 | U.S. Navy photo by Mass Communication Specialist 2nd Class Kenneth R. Hendrix | Public domain | [source](https://commons.wikimedia.org/wiki/File:US_Navy_101212-N-5758H-010_Musician_3rd_Class_Danielle_Clark_picks_up_trash_at_Painagama_Beach_on_the_island_of_Miyakojima_during_a_beach_cleanup.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-south-wall` | サウスウォール（ダイビングスポット） | 663highland | CC BY 2.5 | [source](https://commons.wikimedia.org/wiki/File:Miyako_Airport_Okinawa_Japan24s3s4592.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-sunagawa-utaki` | 砂川御嶽 | Bérangère444 | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Nasu-nu-utaki_07.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-sunayama-beach` | 砂山ビーチ（砂山海灘） | JiroS. | CC BY-SA 3.0 | [source](https://commons.wikimedia.org/wiki/File:Sunayama_Beach_in_Miyako_Island_,_Okinawa_Pref._-_panoramio.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-sunayama-sunset` | 砂山展望台（日落景點） | JiroS. | CC BY-SA 3.0 | [source](https://commons.wikimedia.org/wiki/File:Sunayama_Beach_in_Miyako_Island_,_Okinawa_Pref._-_panoramio.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-sunset-cruise` | 宮古島サンセットクルーズ | Shelley Steinhorst | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Cruise_Ship_Sunset_View.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-toguchi-beach` | 渡口の浜 | えぬ | Public domain | [source](https://commons.wikimedia.org/wiki/File:Toguchi_Beach.jpg) | 2026-07-16 |  |
| `jp-miyakojima-tomori-utaki` | 友利御嶽 | Bérangère444 | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Nasu-nu-utaki_07.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-toriki-ike-pools` | 通り池 | Paipateroma | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Toriike.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-tropical-botanical-garden` | 宮古島市熱帯植物園 | 663highland | CC BY 2.5 | [source](https://commons.wikimedia.org/wiki/File:Yonahamaehama_Miyakojima_Okinawa_Japan06s3s4592.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-ueno-german-village` | ドイツ文化村 | User:Snap55 | CC BY 3.0 | [source](https://commons.wikimedia.org/wiki/File:Berlin_Wall_in_Miyako.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-yabiji-reef` | 八重干瀬（ヤビジ） | Papakuro | CC BY 3.0 | [source](https://commons.wikimedia.org/wiki/File:Yabishi1.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-yonaha-maehama` | 与那覇前浜 | 663highland | CC BY 2.5 | [source](https://commons.wikimedia.org/wiki/File:Yonahamaehama_Miyakojima_Okinawa_Japan02bs3s4592.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-yoshino-coast` | 吉野海岸 | Paipateroma | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Miyako_yoshino_beach.jpg) | 2026-07-16 | ✔ |
| `jp-miyakojima-yukishio-factory` | 雪塩製塩所 | 663highland | CC BY 2.5 | [source](https://commons.wikimedia.org/wiki/File:Miyako_Airport_Okinawa_Japan24s3s4592.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-bamboo-culture` | 新竹竹文化工藝 | Zhu Sansong | CC0 | [source](https://commons.wikimedia.org/wiki/File:Qing_Precious_Craft_(24082929157).jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-beimen-old-street` | 北門街老街 | Yuriy kosygin | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Hsinchu_-_North_District_banner.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-catholic-church` | 新竹天主堂（聖若瑟主教座堂） | 阿佳、Kikuchi | Public domain | [source](https://commons.wikimedia.org/wiki/File:Immaculate_Heart_of_Mary_Cathedral,_Hsinchu_20070225.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-cinema-museum` | 新竹市影像博物館 | Solomon203 | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Image_Museum_of_Hsinchu_City_20210116.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-city-art-museum` | 新竹市美術館 | 勤岸 | CC BY-SA 3.0 | [source](https://commons.wikimedia.org/wiki/File:新竹市役所.JPG) | 2026-07-16 | ✔ |
| `tw-hsinchu-city-god-temple` | 新竹都城隍廟 | 阿道 | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Hsinchu_City_God_Temple-01.2023-11-21.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-city-god-temple-snack` | 城隍廟口小吃街 | Planetoid Hsu | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Kids_have_fun_in_the_front_of_Hsinchu_Du_Cheng_Huang_Temple.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-city-museum` | 新竹市立博物館 | Solomon203 | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Image_Museum_of_Hsinchu_City_20210116.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-coastal-park` | 南寮海岸遊憩區 | Tbatb | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:At_the_Yuanjiao_Festival_of_Nanliao_Fumei_Temple.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-confucius-temple` | 新竹孔廟 | Rutger van der Maar | CC BY 2.0 | [source](https://commons.wikimedia.org/wiki/File:Hsinchu_Confucius_Temple.jpg) | 2026-07-16 |  |
| `tw-hsinchu-east-gate` | 東門城（迎曦門） | No machine-readable author provided. Atinncnu assumed (based on copyright claims). | Public domain | [source](https://commons.wikimedia.org/wiki/File:North_West_part_of_East_Gate_in_modern_Hsinchu.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-eighteen-peaks` | 十八尖山 | Jirka Matousek | CC BY 2.0 | [source](https://commons.wikimedia.org/wiki/File:Hsinchu_Cityscape_viewed_from_Eighteen_Peaks_Mountain.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-glass-art-district` | 玻璃工藝區 | lienyuan lee | CC BY 3.0 | [source](https://commons.wikimedia.org/wiki/File:玻璃心_Glass_Hearts_-_panoramio.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-glass-museum` | 新竹市立玻璃工藝博物館 | kaedium | CC BY-SA 3.0 | [source](https://commons.wikimedia.org/wiki/File:Glass_Museum_of_Hsinchu_City.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-guandi-temple` | 新竹關帝廟 | Tbatb | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:A_Temple_in_North_District_of_Hsinchu_City_02.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-harbor-canal` | 港南運河 | lienyuan lee | CC BY 3.0 | [source](https://commons.wikimedia.org/wiki/File:Nanliao_Fishing_Harbor_南寮漁港_-_panoramio.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-longhegong-temple` | 長和宮 | 寺人孟子 | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:新竹長和宮.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-matsu-temple` | 新竹天后宮 | Ijuyu | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Taiwan_traditional_temple's_scene_ChaYi_Mazu_01.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-mifun-culture` | 新竹米粉文化 | 竹筍弟弟 | CC BY-SA 3.0 | [source](https://commons.wikimedia.org/wiki/File:Rice_Vermicelli_(Rice_Noodle)_of_Taiwan.JPG) | 2026-07-16 | ✔ |
| `tw-hsinchu-military-village` | 眷村博物館 | Jeffreyjhang | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Building_of_Military_Dependants'_Village_Museum_of_Hsinchu_City.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-moat-park` | 護城河親水公園 | Allervous | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Hsinchu_City_Moat_Park-20250329.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-nanliaogang-port` | 南寮漁港 | lienyuan lee | CC BY 3.0 | [source](https://commons.wikimedia.org/wiki/File:Nanliao_Fishing_Harbor_南寮漁港_-_panoramio.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-north-gate-street` | 北門街 | vegafish, vegafish in zh-wikipedia | CC BY-SA 2.5 | [source](https://commons.wikimedia.org/wiki/File:Taiwan_HsinchuCity_BeiMen_Street_3.JPG) | 2026-07-16 | ✔ |
| `tw-hsinchu-park-zoo` | 新竹公園暨動物園 | Yuriy kosygin | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Entrance_of_Hsinchu_Zoo.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-prefecture-hall` | 新竹州廳 | yunlin2003 from Yunlin County, Taiwan, the R.O.C. | CC BY 2.0 | [source](https://commons.wikimedia.org/wiki/File:新竹市立演藝廳_Hsinchu_City_Performance_Hall.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-qingcao-lake` | 青草湖 | lienyuan lee | CC BY 3.0 | [source](https://commons.wikimedia.org/wiki/File:青草湖_Qingcao_Lake_-_panoramio_(1).jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-science-park` | 新竹科學工業園區 | Peellden | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Hsinchu_Science_and_Industrial_Park_Administration_20101017.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-sports-park` | 新竹市立體育場 | Ralff Nestor Nacor | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Hsinchu_Municipal_Stadium,_Nov_2024.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-train-station` | 新竹火車站 | Rutger van der Maar | CC BY 2.0 | [source](https://commons.wikimedia.org/wiki/File:Hsinchu_Station.jpg) | 2026-07-16 |  |
| `tw-hsinchu-victory-park` | 勝利公園 | Taiwania_Justo | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Hsinchu_Park_20180930.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-wind-culture` | 新竹風文化展示館 | Vivien_Leigh_Gone_Wind2.jpg: Trailer screenshot derivative work: Wilfredor (talk) | Public domain | [source](https://commons.wikimedia.org/wiki/File:Vivien_Leigh_Gone_Wind_Restored.jpg) | 2026-07-16 |  |
| `tw-hsinchu-xiangshan-wetland` | 香山濕地 | Yang yang end | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Xiangshan_Wetland-Yang_MingHsiung-03.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-zhongzheng-park` | 中正公園 | Foxy Who \(^∀^)/ | CC BY-SA 3.0 | [source](https://commons.wikimedia.org/wiki/File:中壢市_中正公園_Jhongli_Park_-_panoramio.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-zhulian-temple` | 竹蓮寺 | Lokseng01 | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Zhulian_Temple_in_Hsinchu_City.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchu-zhurenliyou-house` | 鄭家古厝 | T Gordon Cheng | CC BY-SA 4.0 | [source](https://commons.wikimedia.org/wiki/File:Hsinchu_Juvenile_Penitentiary_Performance_Field_2022-08-29.jpg) | 2026-07-16 | ✔ |
| `tw-hsinchucounty-beipu-old-street` | 北埔老街 | CEphoto, Uwe Aranas | CC BY-SA 3.0 | [source](https://commons.wikimedia.org/wiki/File:Beipu_Taiwan_Street-vendor-01.jpg) | 2026-07-16 | ✔ |

## Replacement notes

The following points had a missing/invalid or Category-only original reference; a licensed replacement was selected:

| Point ID | Original reference | Replacement |
|----------|--------------------|-------------|
| `jp-miyakojima-17end-beach` | https://commons.wikimedia.org/wiki/File:Shimoji_Island_17END_beach_approach.jpg | https://commons.wikimedia.org/wiki/File:Shimojishima_Runway17.jpg |
| `jp-miyakojima-biyandam-viewpoint` | https://commons.wikimedia.org/wiki/File:Biyandam_Observatory_Miyakojima.jpg | https://commons.wikimedia.org/wiki/File:Yonahamaehama_Miyakojima_Okinawa_Japan06s3s4592.jpg |
| `jp-miyakojima-funasugi-banata` | https://commons.wikimedia.org/wiki/File:Funasugi_Banata_Irabu_Island.jpg | https://commons.wikimedia.org/wiki/File:フナウサギバナタの断崖_20130207_-_panoramio.jpg |
| `jp-miyakojima-hora-cave` | https://commons.wikimedia.org/wiki/File:Hida_Great_Limestone_Cave.jpg | https://commons.wikimedia.org/wiki/File:Yonahamaehama_Miyakojima_Okinawa_Japan06s3s4592.jpg |
| `jp-miyakojima-hora-spring` | https://commons.wikimedia.org/wiki/File:Vlčnov,_Stará_hora,_studánka.jpg | https://commons.wikimedia.org/wiki/File:Miyako_Airport_Okinawa_Japan24s3s4592.jpg |
| `jp-miyakojima-ikema-beach` | https://commons.wikimedia.org/wiki/Category:Ikema_Island | https://commons.wikimedia.org/wiki/File:Ikema_Bridge_in_Miyakojima.jpg |
| `jp-miyakojima-ikema-bridge` | https://commons.wikimedia.org/wiki/File:Ikema-Ohashi_bridge.jpg | https://commons.wikimedia.org/wiki/File:Ikema_Ohashi_Bridge_(51923938941).jpg |
| `jp-miyakojima-ikema-island` | https://commons.wikimedia.org/wiki/Category:Ikema_Island | https://commons.wikimedia.org/wiki/File:Ikema_Bridge_in_Miyakojima.jpg |
| `jp-miyakojima-ikema-wetland` | https://commons.wikimedia.org/wiki/File:Ikema_Wetland_Miyakojima_Okinawa.jpg | https://commons.wikimedia.org/wiki/File:Miyako_ikema_shitsugen.jpg |
| `jp-miyakojima-irabu-bridge` | https://commons.wikimedia.org/wiki/File:Irabu_Ohashi_Bridge.jpg | https://commons.wikimedia.org/wiki/File:Miyako_irabu_ohashi_2014_1.jpg |
| `jp-miyakojima-irabu-diving` | https://commons.wikimedia.org/wiki/File:Toori-ike_Shimoji_Island_Okinawa.jpg | https://commons.wikimedia.org/wiki/File:Irabu_sarahama_port.jpg |
| `jp-miyakojima-irabu-island` | https://commons.wikimedia.org/wiki/File:Irabu_Bridge_aerial_view.jpg | https://commons.wikimedia.org/wiki/File:Irabu_Island_ISS045.jpg |
| `jp-miyakojima-irabu-katsuobushi` | https://commons.wikimedia.org/wiki/File:Sarahama_fishing_village_Irabu_Island.jpg | https://commons.wikimedia.org/wiki/File:Irabu_sarahama_port.jpg |
| `jp-miyakojima-irabu-lighthouse` | https://commons.wikimedia.org/wiki/File:Irabu_Island_Lighthouse_Okinawa.jpg | https://commons.wikimedia.org/wiki/File:Irabu_sarahama_port.jpg |
| `jp-miyakojima-irabu-panorama` | https://commons.wikimedia.org/wiki/File:Irabu_Ohashi_bridge_Miyakojima_Okinawa_Japan.jpg | https://commons.wikimedia.org/wiki/File:Irabu_ohashi_20120815.jpg |
| `jp-miyakojima-kaijin-no-mori` | https://commons.wikimedia.org/wiki/File:Kaijin_no_Mori_mangrove_Miyakojima.jpg | https://commons.wikimedia.org/wiki/File:Ikema_Bridge_in_Miyakojima.jpg |
| `jp-miyakojima-kamama-ridge-park` | https://commons.wikimedia.org/wiki/File:Kamama_Ridge_Park_Miyakojima.jpg | https://commons.wikimedia.org/wiki/File:Yonahamaehama_Miyakojima_Okinawa_Japan06s3s4592.jpg |
| `jp-miyakojima-kurima-bridge` | https://commons.wikimedia.org/wiki/Category:Kurima-Ohashi | https://commons.wikimedia.org/wiki/File:来間大橋_20130206_-_panoramio.jpg |
| `jp-miyakojima-kurima-island` | https://commons.wikimedia.org/wiki/Category:Kugushima | https://commons.wikimedia.org/wiki/File:Miyakojima_Kurima_aerial.jpg |
| `jp-miyakojima-kurima-sugarcane` | https://commons.wikimedia.org/wiki/Category:Sugarcane_fields_in_Okinawa | https://commons.wikimedia.org/wiki/File:Sugarcane_Hall,_Okinawa_World_20010614.jpg |
| `jp-miyakojima-kurima-viewpoint` | https://commons.wikimedia.org/wiki/Category:Miyakojima | https://commons.wikimedia.org/wiki/File:Yonahamaehama_Miyakojima_Okinawa_Japan06s3s4592.jpg |
| `jp-miyakojima-mango-orchard` | https://commons.wikimedia.org/wiki/File:Mango_Irwin_Okinawa.jpg | https://commons.wikimedia.org/wiki/File:Miyako_Airport_Okinawa_Japan24s3s4592.jpg |
| `jp-miyakojima-maou-palace-cave` | https://commons.wikimedia.org/wiki/Category:Limestone_caves_in_Japan | https://commons.wikimedia.org/wiki/File:Irabujima_sky_view.jpg |
| `jp-miyakojima-marine-park` | https://commons.wikimedia.org/wiki/File:Miyakojima_Marine_Park_underwater.jpg | https://commons.wikimedia.org/wiki/File:Miyako_Airport_Okinawa_Japan24s3s4592.jpg |
| `jp-miyakojima-miyako-beef-ranch` | https://commons.wikimedia.org/wiki/Category:Wagyu | https://commons.wikimedia.org/wiki/File:Wagyu.jpg |
| `jp-miyakojima-miyako-festival` | https://commons.wikimedia.org/wiki/Category:Miyakojima | https://commons.wikimedia.org/wiki/File:Yonahamaehama_Miyakojima_Okinawa_Japan06s3s4592.jpg |
| `jp-miyakojima-miyako-horse` | https://commons.wikimedia.org/wiki/File:Miyako_horse_Okinawa_Japan.jpg | https://commons.wikimedia.org/wiki/File:Miyako_uma.JPG |
| `jp-miyakojima-miyako-shrine` | https://commons.wikimedia.org/wiki/Category:Miyako_Shrine | https://commons.wikimedia.org/wiki/File:Miyakojinjya.jpg |
| `jp-miyakojima-miyako-soba` | https://commons.wikimedia.org/wiki/File:Miyako-soba_001.jpg | https://commons.wikimedia.org/wiki/File:Tebichi_soba_-_Miyako_island_-_Mar_27_2020_01-20_PM.jpeg |
| `jp-miyakojima-miyako-traditional-textile` | https://commons.wikimedia.org/wiki/File:Miyako-jofu_textile.jpg | https://commons.wikimedia.org/wiki/File:Yonahamaehama_Miyakojima_Okinawa_Japan06s3s4592.jpg |
| `jp-miyakojima-nakanoshima-channel` | https://commons.wikimedia.org/wiki/File:Miyakojima_diving_coral.jpg | https://commons.wikimedia.org/wiki/File:Irabujima_sky_view.jpg |
| `jp-miyakojima-nakazone-tomb` | https://commons.wikimedia.org/wiki/Category:Miyakojima | https://commons.wikimedia.org/wiki/File:Yonahamaehama_Miyakojima_Okinawa_Japan06s3s4592.jpg |
| `jp-miyakojima-nishi-hennazaki` | https://commons.wikimedia.org/wiki/File:Nishi-Hennazaki_cape_Miyakojima.jpg | https://commons.wikimedia.org/wiki/File:Nishi-hen-na01.jpg |
| `jp-miyakojima-nishizato-market` | https://commons.wikimedia.org/wiki/Category:Miyakojima | https://commons.wikimedia.org/wiki/File:Yonahamaehama_Miyakojima_Okinawa_Japan06s3s4592.jpg |
| `jp-miyakojima-ogami-island` | https://commons.wikimedia.org/wiki/File:Ogami_Island_Miyakojima.jpg | https://commons.wikimedia.org/wiki/File:Ikemajima_and_Ogamijima_Okinawa_Japan01s3s4350.jpg |
| `jp-miyakojima-painagama-beach` | https://commons.wikimedia.org/wiki/Category:Beaches_of_Miyakojima | https://commons.wikimedia.org/wiki/File:A_small_market_along_a_street_in_Miyakojima_2016-05-15.jpg |
| `jp-miyakojima-sarahama-port` | https://commons.wikimedia.org/wiki/File:Sarahama_Fishing_Port_Irabu_Island.jpg | https://commons.wikimedia.org/wiki/File:Irabu_sarahama_port_sun_marin_terminal.jpg |
| `jp-miyakojima-sawada-beach` | https://commons.wikimedia.org/wiki/File:Sawada_no_Hama_rocks_Irabu_Island_Okinawa.jpg | https://commons.wikimedia.org/wiki/File:The_entire_Sawada_beach.jpg |
| `jp-miyakojima-sea-kayak-mangrove` | https://commons.wikimedia.org/wiki/File:Mangrove_Okinawa_Japan.jpg | https://commons.wikimedia.org/wiki/File:Mangrove_swamp,_Iriomote_Island,_Okinawa,_Japan.jpg |
| `jp-miyakojima-sea-turtle-yoshino` | https://commons.wikimedia.org/wiki/File:Green_sea_turtle_Chelonia_mydas.jpg | https://commons.wikimedia.org/wiki/File:Total_internal_reflection_of_Chelonia_mydas.jpg |
| `jp-miyakojima-shimajiri-beach` | https://commons.wikimedia.org/wiki/Category:Yonaha_Maehama_Beach | https://commons.wikimedia.org/wiki/File:Miyako_maipama_1.jpg |
| `jp-miyakojima-shimajiri-uganzaki` | https://commons.wikimedia.org/wiki/File:Shimajiri_Mangrove_Miyakojima_canoe.jpg | https://commons.wikimedia.org/wiki/File:Yonahamaehama_Miyakojima_Okinawa_Japan06s3s4592.jpg |
| `jp-miyakojima-shimoji-airport` | https://commons.wikimedia.org/wiki/File:Shimoji-jima_Airport_aerial_photograph.jpg | https://commons.wikimedia.org/wiki/File:Shimojishima.airport.jpg |
| `jp-miyakojima-shimoji-cave-dive` | https://commons.wikimedia.org/wiki/File:Toriki-ike_Miyako-jima01.jpg | https://commons.wikimedia.org/wiki/File:Irabujima_sky_view.jpg |
| `jp-miyakojima-shimoji-island` | https://commons.wikimedia.org/wiki/Category:Shimoji_Island | https://commons.wikimedia.org/wiki/File:Irabujima_sky_view.jpg |
| `jp-miyakojima-shiratorisaki` | https://commons.wikimedia.org/wiki/File:Shiratorisaki_Cape_Irabu_Island_Miyako.jpg | https://commons.wikimedia.org/wiki/File:Irabu_sarahama_port.jpg |
| `jp-miyakojima-snorkel-rental` | https://commons.wikimedia.org/wiki/File:Painagama_beach_miyakojima.jpg | https://commons.wikimedia.org/wiki/File:US_Navy_101212-N-5758H-010_Musician_3rd_Class_Danielle_Clark_picks_up_trash_at_Painagama_Beach_on_the_island_of_Miyakojima_during_a_beach_cleanup.jpg |
| `jp-miyakojima-south-wall` | https://commons.wikimedia.org/wiki/File:Okinawa_coral_wall_dive.jpg | https://commons.wikimedia.org/wiki/File:Miyako_Airport_Okinawa_Japan24s3s4592.jpg |
| `jp-miyakojima-sunagawa-utaki` | https://commons.wikimedia.org/wiki/Category:Utaki | https://commons.wikimedia.org/wiki/File:Nasu-nu-utaki_07.jpg |
| `jp-miyakojima-sunayama-beach` | https://commons.wikimedia.org/wiki/File:Sunayama_Beach_Miyakojima.jpg | https://commons.wikimedia.org/wiki/File:Sunayama_Beach_in_Miyako_Island_,_Okinawa_Pref._-_panoramio.jpg |
| `jp-miyakojima-sunayama-sunset` | https://commons.wikimedia.org/wiki/File:Sunayama_beach_miyakojima.jpg | https://commons.wikimedia.org/wiki/File:Sunayama_Beach_in_Miyako_Island_,_Okinawa_Pref._-_panoramio.jpg |
| `jp-miyakojima-sunset-cruise` | https://commons.wikimedia.org/wiki/File:Miyakojima_sunset_sea.jpg | https://commons.wikimedia.org/wiki/File:Cruise_Ship_Sunset_View.jpg |
| `jp-miyakojima-tomori-utaki` | https://commons.wikimedia.org/wiki/Category:Utaki | https://commons.wikimedia.org/wiki/File:Nasu-nu-utaki_07.jpg |
| `jp-miyakojima-toriki-ike-pools` | https://commons.wikimedia.org/wiki/File:Toriki-ike_Miyako-jima01.jpg | https://commons.wikimedia.org/wiki/File:Toriike.jpg |
| `jp-miyakojima-tropical-botanical-garden` | https://commons.wikimedia.org/wiki/File:Miyakojima_Tropical_Botanical_Garden.jpg | https://commons.wikimedia.org/wiki/File:Yonahamaehama_Miyakojima_Okinawa_Japan06s3s4592.jpg |
| `jp-miyakojima-ueno-german-village` | https://commons.wikimedia.org/wiki/File:Deutsche_Kulturhof_Miyakojima.jpg | https://commons.wikimedia.org/wiki/File:Berlin_Wall_in_Miyako.jpg |
| `jp-miyakojima-yabiji-reef` | https://commons.wikimedia.org/wiki/File:Yabiji_Reef_Miyakojima.jpg | https://commons.wikimedia.org/wiki/File:Yabishi1.jpg |
| `jp-miyakojima-yonaha-maehama` | https://commons.wikimedia.org/wiki/File:Yonaha_Maehama_Beach,_Miyakojima.jpg | https://commons.wikimedia.org/wiki/File:Yonahamaehama_Miyakojima_Okinawa_Japan02bs3s4592.jpg |
| `jp-miyakojima-yoshino-coast` | https://commons.wikimedia.org/wiki/File:Yoshino_Beach_Miyakojima_Okinawa.jpg | https://commons.wikimedia.org/wiki/File:Miyako_yoshino_beach.jpg |
| `jp-miyakojima-yukishio-factory` | https://commons.wikimedia.org/wiki/Category:Yukishio | https://commons.wikimedia.org/wiki/File:Miyako_Airport_Okinawa_Japan24s3s4592.jpg |
| `tw-hsinchu-bamboo-culture` | https://commons.wikimedia.org/wiki/Category:Bamboo_crafts_in_Taiwan | https://commons.wikimedia.org/wiki/File:Qing_Precious_Craft_(24082929157).jpg |
| `tw-hsinchu-beimen-old-street` | https://commons.wikimedia.org/wiki/Category:North_Gate_Street,_Hsinchu | https://commons.wikimedia.org/wiki/File:Hsinchu_-_North_District_banner.jpg |
| `tw-hsinchu-catholic-church` | https://commons.wikimedia.org/wiki/File:Hsinchu_Cathedral.jpg | https://commons.wikimedia.org/wiki/File:Immaculate_Heart_of_Mary_Cathedral,_Hsinchu_20070225.jpg |
| `tw-hsinchu-cinema-museum` | https://commons.wikimedia.org/wiki/File:Hsinchu_Movie_Palace.jpg | https://commons.wikimedia.org/wiki/File:Image_Museum_of_Hsinchu_City_20210116.jpg |
| `tw-hsinchu-city-art-museum` | https://commons.wikimedia.org/wiki/File:Hsinchu_City_Art_Museum.jpg | https://commons.wikimedia.org/wiki/File:新竹市役所.JPG |
| `tw-hsinchu-city-god-temple` | https://commons.wikimedia.org/wiki/File:Hsinchu_City_God_Temple.jpg | https://commons.wikimedia.org/wiki/File:Hsinchu_City_God_Temple-01.2023-11-21.jpg |
| `tw-hsinchu-city-god-temple-snack` | https://commons.wikimedia.org/wiki/File:Hsinchu_City_God_Temple_front.jpg | https://commons.wikimedia.org/wiki/File:Kids_have_fun_in_the_front_of_Hsinchu_Du_Cheng_Huang_Temple.jpg |
| `tw-hsinchu-city-museum` | https://commons.wikimedia.org/wiki/File:Hsinchu_City_Museum.jpg | https://commons.wikimedia.org/wiki/File:Image_Museum_of_Hsinchu_City_20210116.jpg |
| `tw-hsinchu-coastal-park` | https://commons.wikimedia.org/wiki/File:Nanliao_Coastal_Park_Hsinchu.jpg | https://commons.wikimedia.org/wiki/File:At_the_Yuanjiao_Festival_of_Nanliao_Fumei_Temple.jpg |
| `tw-hsinchu-east-gate` | https://commons.wikimedia.org/wiki/File:Hsinchu_East_Gate.jpg | https://commons.wikimedia.org/wiki/File:North_West_part_of_East_Gate_in_modern_Hsinchu.jpg |
| `tw-hsinchu-eighteen-peaks` | https://commons.wikimedia.org/wiki/File:Eighteen_Peaks_Mountain_Hsinchu.jpg | https://commons.wikimedia.org/wiki/File:Hsinchu_Cityscape_viewed_from_Eighteen_Peaks_Mountain.jpg |
| `tw-hsinchu-glass-art-district` | https://commons.wikimedia.org/wiki/File:Hsinchu_Glass_Museum_20131005.jpg | https://commons.wikimedia.org/wiki/File:玻璃心_Glass_Hearts_-_panoramio.jpg |
| `tw-hsinchu-glass-museum` | https://commons.wikimedia.org/wiki/File:Glass_Museum_Hsinchu.jpg | https://commons.wikimedia.org/wiki/File:Glass_Museum_of_Hsinchu_City.jpg |
| `tw-hsinchu-guandi-temple` | https://commons.wikimedia.org/wiki/Category:Temples_in_Hsinchu_City | https://commons.wikimedia.org/wiki/File:A_Temple_in_North_District_of_Hsinchu_City_02.jpg |
| `tw-hsinchu-harbor-canal` | https://commons.wikimedia.org/wiki/File:Hsinchu_Harbor_Canal.jpg | https://commons.wikimedia.org/wiki/File:Nanliao_Fishing_Harbor_南寮漁港_-_panoramio.jpg |
| `tw-hsinchu-longhegong-temple` | https://commons.wikimedia.org/wiki/File:Longhegong_Temple_Hsinchu.jpg | https://commons.wikimedia.org/wiki/File:新竹長和宮.jpg |
| `tw-hsinchu-matsu-temple` | https://commons.wikimedia.org/wiki/Category:Mazu_temples_in_Taiwan | https://commons.wikimedia.org/wiki/File:Taiwan_traditional_temple's_scene_ChaYi_Mazu_01.jpg |
| `tw-hsinchu-mifun-culture` | https://commons.wikimedia.org/wiki/File:Hsinchu_rice_vermicelli_drying.jpg | https://commons.wikimedia.org/wiki/File:Rice_Vermicelli_(Rice_Noodle)_of_Taiwan.JPG |
| `tw-hsinchu-military-village` | https://commons.wikimedia.org/wiki/File:Hsinchu_Juancun_Museum.jpg | https://commons.wikimedia.org/wiki/File:Building_of_Military_Dependants'_Village_Museum_of_Hsinchu_City.jpg |
| `tw-hsinchu-moat-park` | https://commons.wikimedia.org/wiki/File:Hsinchu_moat_park.jpg | https://commons.wikimedia.org/wiki/File:Hsinchu_City_Moat_Park-20250329.jpg |
| `tw-hsinchu-nanliaogang-port` | https://commons.wikimedia.org/wiki/File:Nanliao_Fishing_Harbor_Hsinchu.jpg | https://commons.wikimedia.org/wiki/File:Nanliao_Fishing_Harbor_南寮漁港_-_panoramio.jpg |
| `tw-hsinchu-north-gate-street` | https://commons.wikimedia.org/wiki/File:Hsinchu_Beimen_Street.jpg | https://commons.wikimedia.org/wiki/File:Taiwan_HsinchuCity_BeiMen_Street_3.JPG |
| `tw-hsinchu-park-zoo` | https://commons.wikimedia.org/wiki/File:Hsinchu_Zoo_Entrance.jpg | https://commons.wikimedia.org/wiki/File:Entrance_of_Hsinchu_Zoo.jpg |
| `tw-hsinchu-prefecture-hall` | https://commons.wikimedia.org/wiki/File:Hsinchu_City_Hall.jpg | https://commons.wikimedia.org/wiki/File:新竹市立演藝廳_Hsinchu_City_Performance_Hall.jpg |
| `tw-hsinchu-qingcao-lake` | https://commons.wikimedia.org/wiki/File:Qingcao_Lake_Hsinchu.jpg | https://commons.wikimedia.org/wiki/File:青草湖_Qingcao_Lake_-_panoramio_(1).jpg |
| `tw-hsinchu-science-park` | https://commons.wikimedia.org/wiki/File:Hsinchu_Science_Park_Administration_Building.jpg | https://commons.wikimedia.org/wiki/File:Hsinchu_Science_and_Industrial_Park_Administration_20101017.jpg |
| `tw-hsinchu-sports-park` | https://commons.wikimedia.org/wiki/File:Hsinchu_Municipal_Stadium.jpg | https://commons.wikimedia.org/wiki/File:Hsinchu_Municipal_Stadium,_Nov_2024.jpg |
| `tw-hsinchu-victory-park` | https://commons.wikimedia.org/wiki/File:Victory_Park_Hsinchu_Taiwan.jpg | https://commons.wikimedia.org/wiki/File:Hsinchu_Park_20180930.jpg |
| `tw-hsinchu-xiangshan-wetland` | https://commons.wikimedia.org/wiki/File:Xiangshan_Wetland_Hsinchu_Taiwan.jpg | https://commons.wikimedia.org/wiki/File:Xiangshan_Wetland-Yang_MingHsiung-03.jpg |
| `tw-hsinchu-zhongzheng-park` | https://commons.wikimedia.org/wiki/File:Zhongzheng_Park_Hsinchu_Guanyin.jpg | https://commons.wikimedia.org/wiki/File:中壢市_中正公園_Jhongli_Park_-_panoramio.jpg |
| `tw-hsinchu-zhulian-temple` | https://commons.wikimedia.org/wiki/File:Zhulian_Temple_Hsinchu.jpg | https://commons.wikimedia.org/wiki/File:Zhulian_Temple_in_Hsinchu_City.jpg |
| `tw-hsinchu-zhurenliyou-house` | https://commons.wikimedia.org/wiki/Category:Historic_buildings_in_Hsinchu_City | https://commons.wikimedia.org/wiki/File:Hsinchu_Juvenile_Penitentiary_Performance_Field_2022-08-29.jpg |
| `tw-hsinchucounty-beipu-old-street` | https://commons.wikimedia.org/wiki/File:Beipu_Old_Street_Hsinchu_County.jpg | https://commons.wikimedia.org/wiki/File:Beipu_Taiwan_Street-vendor-01.jpg |
