.PHONY:
download:
	docker exec -it scraper bash -c "/bin/sh /app/run_downloader.sh ${brand} ${category}"

.PHONY:
extract:
	docker exec -it scraper bash -c "/bin/sh /app/run_extractor.sh ${brand} ${output}"