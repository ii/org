## Potaroo with company names subbed out
SELECT A.asn, A.companyname, case when name_yaml is not null then name_yaml  else B.companyname end as name_with_yaml_name FROM ( SELECT asn, companyname FROM `${GCP_BIGQUERY_DATASET}.3_potaroo_with_yaml_name_column`) A LEFT JOIN ( SELECT asn, companyname, name_yaml FROM `${GCP_BIGQUERY_DATASET}.3_potaroo_with_yaml_name_column`) B ON A.asn=B.asn
