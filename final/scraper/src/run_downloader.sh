BRAND=toom
CATEGORY=test_farbe
URLS_SOURCE=$3
PRODUCT_URLS=$4
URLS_AMOUNT=$5
IMAGES=$6


if [ -z "${BRAND}" ]
then
    echo "Please, enter the brand name:"
    read BRAND
fi

if [ -z "${CATEGORY}" ]
then
    echo "Please, enter the category:"
    read CATEGORY
fi

if [ -z "${URLS_SOURCE}" ]
then
    echo "Would you like to extract files from product URLs list? y/n"
    read URLS_SOURCE
fi

if [ "$URLS_SOURCE" = "y" ]; then
    echo "Extracting files from product URLs list..."
    cd brands/${BRAND}/scraper/spiders/ \
    && scrapy runspider downloader.py -a brand=${BRAND} -a category=${CATEGORY} -a source=${URLS_SOURCE:-"0"} -a urls=${PRODUCT_URLS:-"0"} -a urls_amount=${URLS_AMOUNT:-"0"} -a images=${IMAGES:-"n"};
    echo "Files extracted!"
    exit 0
elif [ "$URLS_SOURCE" = "n" ]; then
    echo "OK"
else
    echo "Invalid input."
    exit 0
fi

if [ -z "${PRODUCT_URLS}" ]
then
    echo "Would you like to generate product urls list? y/n"
    read PRODUCT_URLS
fi

if [ "$PRODUCT_URLS" = "y" ]; then
    if [ -z "${URLS_AMOUNT}" ]; then
        echo "How many urls would you like to save?"
        read URLS_AMOUNT
    fi

    echo "Generating product URLs list..."
elif [ "$PRODUCT_URLS" = "n" ]; then
    echo "OK"
else
    echo "Invalid input."
    exit 0
fi

if [ -d "brands/${BRAND}" ]
then
    cd brands/${BRAND}/truum_scraper/spiders/ \
    && scrapy runspider downloader.py -a brand=${BRAND} -a category=${CATEGORY} -a source=${URLS_SOURCE} -a urls=${PRODUCT_URLS:-"0"} -a urls_amount=${URLS_AMOUNT:-"0"} -a images=${IMAGES:-"n"};
else
    echo "Error: Brand \"${BRAND}\" not implemented!"
fi
