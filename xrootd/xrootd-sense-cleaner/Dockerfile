ARG RELEASE=latest
FROM cmscaltech/base_image:$RELEASE
# NOTES
# 2024 Feb 7th - Move to cmscaltech/base_image (which is based on OSG Image. See base_image repo)

ADD sense-cleaner.sh /etc/sense-cleaner.sh

ENTRYPOINT ["/etc/sense-cleaner.sh"]
