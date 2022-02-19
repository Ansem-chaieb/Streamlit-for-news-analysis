def bbc_content(soup):
    cont2 = soup.find("div", {"id": "index-page"})
    # =================================================================================== #
    #                             1. Tops component                                       #
    # =================================================================================== #
    topos = cont2.find("div", {"id": "topos-component"})
    topos_cont = topos.find("div", {"class": "no-mpu"}).find(
        "div", {"class": "gel-layout__item gel-1/1"}
    )
    main1 = topos_cont.find(
        "div",
        {
            "class": "gel-layout__item gs-u-pb+@m gel-1/1 gel-1/1@xl gel-2/5@xxl gs-u-ml0 nw-o-keyline nw-o-no-keyline@m"
        },
    )
    main2 = topos_cont.find(
        "div",
        {
            "class": "gel-layout__item gel-1/1 gel-3/5@xxl gs-u-display-none@xl gs-u-display-block@xxl"
        },
    )
    # =================================================================================== #
    #                             2. global climates                                      #
    # =================================================================================== #
    Global = cont2.find(
        "div", {"aria-labelledby": "nw-c-Globalclimatesummit__title"}
    )
    Global_cont = Global.find(
        "div",
        {"class": "nw-c-5-slice gel-layout gel-layout--equal b-pw-1280"},
    )
    # =================================================================================== #
    #                             3. climates                                             #
    # =================================================================================== #
    climate = cont2.find(
        "div", {"aria-labelledby": "nw-c-Climatebasics__title"}
    )
    climate_cont = climate.find(
        "div",
        {"class": "nw-c-5-slice gel-layout gel-layout--equal b-pw-1280"},
    )
    # =================================================================================== #
    #                             4. features                                             #
    # =================================================================================== #
    features = cont2.find("div", {"aria-labelledby": "nw-c-Features__title"})
    features_cont = features.find(
        "div",
        {"class": "nw-c-5-slice gel-layout gel-layout--equal b-pw-1280"},
    )
    # =================================================================================== #
    #                             5. Latest Updates                                       #
    # =================================================================================== #

    api = [
        "https://push.api.bbci.co.uk/batch?t=%2Fdata%2Fbbc-morph-%7Blx-commentary-data-paged%2Fabout%2Fe6369e45-f838-49cc-b5ac-857ed182e549%2FisUk%2Ffalse%2Flimit%2F20%2FnitroKey%2Flx-nitro%2FpageNumber%",
        "2F",
        "%2Fversion%2F1.5.6%2Clx-commentary-src-paged%2Fabout%2Fe6369e45-f838-49cc-b5ac-857ed182e549%2FisUk%2Ffalse%2Flimit%2F20%2FnitroKey%2Flx-nitro%2FpageNumber%",
        "%2Fversion%2F1.5.6%7D?timeout=5"]

    class1 = [
        "gel-layout__item gs-u-pb+@m gel-1/3@m gel0-1/4@xl gel-1/3@xxl nw-o-keyline nw-o-no-keyline@m",
        "gel-layout__item gs-u-pb+@m gel-1/3@m gel-1/4@xl gel-1/3@xxl nw-o-keyline nw-o-no-keyline@m",
    ]

    class2 = [
        "gel-layout__item gel-1/3@m gel-1/4@l gel-1/5@xxl nw-o-keyline nw-o-no-keyline@m",
        "gel-layout__item gel-1/4@l gel-2/5@xxl",
    ]

    sub_class2 = [
        "gel-layout__item gel-1/2@xs gel-1/1@l gel-1/2@xxl nw-o-keyline--bottom nw-o-keyline nw-o-no-keyline@xs nw-o-keyline@l nw-o-no-keyline@xxl nw-o-keyline-vertical@xs nw-o-no-keyline-vertical@l",
        "gel-layout__item gel-1/2@xs gel-1/1@l gel-1/2@xxl",
    ]

    return main1, main2, Global_cont, climate_cont, features_cont, api, class1, class2,sub_class2