# Downloads latest available data from AI2's servers.

DATE=2020-04-24
DATA_DIR=data

wget https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/"${DATE}"/comm_use_subset.tar.gz -P "${DATA_DIR}"
wget https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/"${DATE}"/noncomm_use_subset.tar.gz -P "${DATA_DIR}"
wget https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/"${DATE}"/custom_license.tar.gz -P "${DATA_DIR}"
wget https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/"${DATE}"/biorxiv_medrxiv.tar.gz -P "${DATA_DIR}"
wget https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/"${DATE}"/metadata.csv -P "${DATA_DIR}"

mkdir "${DATA_DIR}"/comm_use_subset "${DATA_DIR}"/noncomm_use_subset "${DATA_DIR}"/custom_license "${DATA_DIR}"/biorxiv_medrxiv

tar -zxvf "${DATA_DIR}"/comm_use_subset.tar.gz -C "${DATA_DIR}"/comm_use_subset/
tar -zxvf "${DATA_DIR}"/noncomm_use_subset.tar.gz -C "${DATA_DIR}"/noncomm_use_subset/
tar -zxvf "${DATA_DIR}"/custom_license.tar.gz -C "${DATA_DIR}"/custom_license/
tar -zxvf "${DATA_DIR}"/biorxiv_medrxiv.tar.gz -C "${DATA_DIR}"/biorxiv_medrxiv/

rm "${DATA_DIR}"/comm_use_subset.tar.gz "${DATA_DIR}"/noncomm_use_subset.tar.gz "${DATA_DIR}"/custom_license.tar.gz "${DATA_DIR}"/biorxiv_medrxiv.tar.gz
