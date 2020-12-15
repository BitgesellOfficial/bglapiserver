import pathlib
from views import *

PROJECT_ROOT = pathlib.Path(__file__).parent


def setup_routes(app):

    # Headers
    app.router.add_route('GET', '/rest/block/headers/{block_pointer}/{count}', get_block_headers)
    app.router.add_route('GET', '/rest/block/headers/{block_pointer}', get_block_headers)

    # Block filters
    if app["block_filters"]:
        app.router.add_route('GET', '/rest/block/filters/headers/{filter_type}/{start_height}/{stop_hash}',
                             get_block_filters_headers)
        app.router.add_route('GET', '/rest/block/filters/batch/headers/{filter_type}/{start_height}/{stop_hash}',
                             get_block_filters_batch_headers)
        app.router.add_route('GET', '/rest/block/filters/{filter_type}/{start_height}/{stop_hash}',
                             get_block_filters)

    # Block
    app.router.add_route('GET', '/rest/block/last', get_block_last)
    app.router.add_route('GET', '/rest/block/{block_pointer}', get_block_by_pointer)
    app.router.add_route('GET', '/rest/block/utxo/{block_pointer}', get_block_utxo) # test after sync completed
    if app["blocks_data"]:
        app.router.add_route('GET', '/rest/block/data/last', get_block_data_last)
        app.router.add_route('GET', '/rest/block/data/{block_pointer}', get_block_data_by_pointer)
    if app["transaction"]:
        app.router.add_route('GET', '/rest/block/transactions/{block_pointer}', get_block_transactions)
        app.router.add_route('GET', '/rest/block/transaction/id/list/{block_pointer}', get_block_transactions_list)
    if app["blockchain_analytica"]:
        app.router.add_route('GET', '/rest/blockchain/state/{block_pointer}', get_blockchain_state)

    # Blocks
    app.router.add_route('GET', '/rest/blocks/last/{n}', get_last_n_blocks)
    app.router.add_route('GET', '/rest/blocks/today', get_daily_blocks)
    app.router.add_route('GET', '/rest/blocks/date/{day}', get_blocks_by_day)
    app.router.add_route('GET', '/rest/blocks/last/{n}/hours', get_last_n_hours_blocks)
    if app["blocks_data"]:
        app.router.add_route('GET', '/rest/blocks/data/last/{n}', get_data_last_n_blocks)
        app.router.add_route('GET', '/rest/blocks/data/today', get_data_daily_blocks)
        app.router.add_route('GET', '/rest/blocks/data/date/{day}', get_data_blocks_by_day)
        app.router.add_route('GET', '/rest/blocks/data/last/{n}/hours', get_data_last_n_hours_blocks)



    # Transaction
        if app["transaction"]:
            app.router.add_route('GET', '/rest/transaction/{tx_pointer}', get_transaction_by_pointer)
            app.router.add_route('GET', '/rest/transaction/hash/by/pointer/{tx_blockchain_pointer}',
                                 get_transaction_hash_by_pointer)
            app.router.add_route('GET', '/rest/transaction/calculate/merkle_proof/{tx_pointer}',
                                 calculate_transaction_merkle_proof)
            if app["merkle_proof"]:
                app.router.add_route('GET', '/rest/transaction/merkle_proof/{tx_pointer}', get_transaction_merkle_proof)
            else:
                app.router.add_route('GET', '/rest/transaction/merkle_proof/{tx_pointer}',
                                     calculate_transaction_merkle_proof)


    # Transactions
        if app["transaction"]:
            app.router.add_route('POST', '/rest/transactions/by/pointer/list', get_transaction_by_pointer_list)
            app.router.add_route('POST', '/rest/transactions/hash/by/blockchain/pointer/list',
                                 get_transaction_hash_by_pointers)


    # Mempool
    app.router.add_route('GET', '/rest/mempool/transactions', get_mempool_transactions)
    if app["mempool_analytica"]:
        app.router.add_route('GET', '/rest/mempool/state', get_mempool_state)
        app.router.add_route('GET', '/rest/mempool/invalid/transactions', get_mempool_invalid_transactions)
        app.router.add_route('GET', '/rest/mempool/doublespend/transactions', get_mempool_doublespend_transactions)
        app.router.add_route('GET', '/rest/mempool/recommended/fee', get_fee)


    # Address
    app.router.add_route('GET', '/rest/address/utxo/{address}', get_address_confirmed_utxo)
    app.router.add_route('GET', '/rest/address/uutxo/{address}', get_address_unconfirmed_utxo)
    if app["transaction_history"]:
        app.router.add_route('GET', '/rest/address/state/{address}', get_address_state_extended)
        app.router.add_route('GET', '/rest/address/transactions/{address}', get_address_transactions)
        app.router.add_route('GET', '/rest/address/unconfirmed/transactions/{address}',
                             get_address_unconfirmed_transactions)
    else:
        app.router.add_route('GET', '/rest/address/state/{address}', get_address_state)


    # Addresses
    app.router.add_route('POST', '/rest/addresses/state/by/address/list', get_address_state_by_list)
    if app["address_state"]:
        app.router.add_route('GET', '/rest/block/addresses/statistics/{pointer}', get_block_addresses_stat)
        app.router.add_route('GET', '/rest/blockchain/addresses/statistics/{pointer}', get_blockchain_addresses_stat)


    # Outpoints
    app.router.add_route('POST', '/rest/outpoints', get_outpoints_info)


    # Default
    app.router.add_route('GET', '/{tail:.*}', about)
    app.router.add_route('POST', '/{tail:.*}', about)