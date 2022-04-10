import json
import logging
import shutil
from pathlib import Path

import boto3
from django.forms import model_to_dict

from config.settings.common import env
from umbrella.contracts.models import Contract, Node, CLAUSE_TYPE_KDP_TYPES_MAPPING
from umbrella.core.exceptions import UmbrellaError

LOCAL_ROOT = Path(env('AWS_DOWNLOADS_LOCAL_ROOT'))
BUCKET_NAME = env('AWS_ANALYTICS_BUCKET_NAME')
BUCKET = boto3.resource('s3').Bucket(BUCKET_NAME)

logger = logging.getLogger('load_aws_analytics_jsons_to_db')


def download_s3_file(aws_file):
    local_file = str(LOCAL_ROOT / aws_file)
    BUCKET.download_file(aws_file, local_file)
    logger.info(f"Downloaded '{local_file}'.")
    return local_file


# Download analytics json files
def download_s3_folder(aws_dir):
    local_dir = LOCAL_ROOT / aws_dir
    shutil.rmtree(local_dir, ignore_errors=True)
    local_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Cleaned dir '{local_dir}'.")

    aws_files = BUCKET.objects.filter(Prefix=aws_dir).all()
    if not list(aws_files):
        raise UmbrellaError(f"No data for contract '{aws_dir}'.")

    downloaded_files = []
    for aws_file in aws_files:
        # To run download only for file, folder is also present in aws_files
        if aws_file.key.endswith('.json'):
            downloaded_file = download_s3_file(aws_file.key)
            downloaded_files.append(downloaded_file)
    return downloaded_files


def parse_node(node_type, clause_type, node_json, contract):
    node = Node.create(
        type=node_type,
        content=node_json,
    )

    clause_types = CLAUSE_TYPE_KDP_TYPES_MAPPING.keys()
    if node_type in clause_types:
        node.contract = contract
    else:
        para_id = node_json["paraId"]
        clause = Node.objects.filter(type=clause_type, contract=contract, content__paraId=para_id).first()
        node.clause = clause

    node.save()
    return node


def parse_node_list(json_data, contract):
    clause_type = get_clause_type_from_json_data(json_data)
    for node_type, nodes_list in json_data.items():
        for node_json in nodes_list:
            node = parse_node(node_type, clause_type, node_json, contract)
            logger.info(f"Parsed node {model_to_dict(node)}")


# Parse analytics json files
def parse_clause_json(file_path):
    # TODO: return count of objects created
    contract = get_contract_from_file_path(file_path)
    logger.info(f"Parsing '{file_path}'.")
    with Path(file_path).open(mode="rb") as f:
        json_data = json.load(f)
        parse_node_list(json_data, contract)


def get_contract_from_file_path(file_path):
    upper_uuid = file_path.split("/")[-2]
    contract_uuid = upper_uuid.lower()
    contract = Contract.objects.filter(id=contract_uuid).first()
    if not contract:
        raise UmbrellaError(f"No Contracts with id: {contract_uuid}")
    return contract


def get_clause_type_from_json_data(json_data):
    json_keys = set(json_data)
    available_clause_types = set(CLAUSE_TYPE_KDP_TYPES_MAPPING)
    common_clauses = json_keys & available_clause_types
    if len(common_clauses) != 1:
        msg = f"File should contain 1 clause, but contains {len(common_clauses)}: {common_clauses}"
        raise UmbrellaError(msg)
    clause_type = list(common_clauses)[0]
    return clause_type
