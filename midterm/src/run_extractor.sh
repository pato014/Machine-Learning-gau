BRAND=my_auto
CATEGORY=$2


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

if [ -d "brands/${BRAND}" ]
then
    cd brands/${BRAND}/scraper/spiders/ \
    && scrapy crawl "extractor" -a brand=${BRAND} -a category=${CATEGORY} -O ${CATEGORY}.jsonl
else
    echo "Error: Brand \"${BRAND}\" not implemented!"
fi
