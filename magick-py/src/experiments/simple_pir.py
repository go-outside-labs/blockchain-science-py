# -*- encoding: utf-8 -*-
# src/experiments/simple_pir.py
# Experiment with PIR.

from src.primitives.regev import Regev
from src.primitives.message import Message
from src.utils.os import log_info, log_debug


def no_encryption_example() -> None:
    """
        Run a tutorial presenting the logic of a PIR experiment 
        without encryption.
    """

    ########################################################################
    # 1. Represent a database as a square matrix, where the columns are 
    #    the database entries and the rows are the database attributes
    ########################################################################
    log_debug('In this PIR tutorial, we represent a database as a square matrix, ' + 
        'where columns are the database entries and rows are the database attributes.')
    
    log_debug('We start the class Message(), creating a random database ' +
                    'with mod 500, and 20 entries and 20 attributes.\n')

    msg = Message()
    db = msg.create_random_message(500, 20, 20)
    
    log_debug(f'db: {db}\n')

    ########################################################################
    # 2. Create some random query value for row and column
    ########################################################################
    log_debug('Now, let\'s create a random query value for row and column. ' +
                                            'Say, row 10 and column 10.')
    
    query_row = 10
    query_col = 10

    log_debug(f'query_row: {query_row}, query_col: {query_col}\n')

    ########################################################################
    # 3. Create a message that is 5 at the query column and 0 elsewhere
    ########################################################################
    log_debug('Let\'s create a query message vector, of size 500, that is 1 at ' +
                                            'the query column and 0 elsewhere.')
    query = msg.create_zero_message(500, 20, 1)
    query.set_query_element(query_col, 0, 1)

    log_debug(f'query vector: {query.message}')

    ########################################################################
    # 4. Compute resulting message vector
    ########################################################################
    log_debug('Let\'s compute the resulting message vector, which is the ' +
                               'dot product of the database and the query.')
    
    result = db * query
    log_debug(f'result = db * query: {result}\n')

    ########################################################################
    # 5. Compute msg retrieved from the database
    ########################################################################
    log_debug('Finally, let\'s compute the message retrieved from the database, ' + 
                    'by getting the element at the query row and column.')
    log_debug(f'db.get_query_element({query_row}, {query_col}): {db.get_query_element(query_row, query_col)}\n')

    log_debug('This should be the same as the result message vector element at the query row.')
    log_debug(f'result.get_query_element({query_row}, 0): {result.get_query_element(query_row, 0)}\n')

    correct_retrieval = result.get_query_element(query_row, 0) == \
                        db.get_query_element(query_row, query_col)

    log_info(f'Are they the same? Did we get a correct retrieval? {correct_retrieval}')


def secret_key_regev_example() -> None:
    """Run a secret key Regev encryption and decryption PIR experiment."""
    ########################################################################
    # 1. Represent a database as a square matrix, where the columns are 
    #    the database entries and the rows are the database attributes
    ########################################################################
    
    regev = Regev()
    msg = Message()

    log_debug('1. We start creating a random message vector ' + 
                                 'as a square m x m database with mod p')
    
    db = msg.create_random_message(regev.p, regev.m, regev.m)
    log_debug(f'db: {db}\n')

    ########################################################################
    # 2. Create some random query value for row and column
    ########################################################################
    log_debug('2. Now, let\'s create a random query value for row and column.')
   
    # TODO: Crete a PIR class and add these attributes.
    # TODO: add these hard coded values to the .env
    query_row = 5
    query_col = 5

    log_debug(f'query_row: {query_row}, query_col: {query_col}\n')

    ########################################################################
    # 3. Create query message vector
    ########################################################################
    log_debug('3. Let\'s create a query message vector, of size m, that is 1 at ' +
                                            'the query column and 0 elsewhere.')                

    query = msg.create_zero_message(regev.mod, regev.m, 1)
    query.set_query_element(query_col, 0, 1)

    log_debug(f'query vector: {query.message}\n')

    ########################################################################
    # 4. Encrypt query message vector
    ########################################################################
    log_debug('4. Let\'s encrypt the query message vector, calculating A and e.')
   
    _, A, e = regev.create_message_setup()

    # Here we could either use mod or p as the scaling factor.
    s = regev.create_secret_key()

    log_debug(f'The secret key s: {s}')

    ########################################################################
    # 5. Scale query vector by delta = mod / p and db vector from p to mod
    ########################################################################
    log_debug('5. We scale the query vector by delta=mod/p and db vector to 1/p')

    scaled_query = query.calculate_scaling(regev.mod, regev.p, regev.mod)
    scaled_db = db.calculate_scaling(1, 1, regev.mod)

    log_debug(f'scaled_query: {scaled_query}')
    log_debug(f'scaled_db: {scaled_db}\n')

    ########################################################################
    # 6. Encryption by calculating B and ciphertext c
    ########################################################################
    log_debug('6. Let\'s encrypt the query vector by calculating B and ciphertext c.')
    c_query = regev.calculate_encryption(A, s, e, scaled_query)

    log_debug(f'c_query: {c_query}\n')

    ########################################################################
    # 7. Compute encrypted result
    ########################################################################
    log_debug('7. Let\'s compute the encrypted result by calculating the dot ' +
                 'product of the encrypted query and the encrypted database.') 

    c_result = (scaled_db * c_query[0], scaled_db * c_query[1])

    log_debug(f'c_result: {c_result}\n')

    ########################################################################
    # 8. Calculate the decryption of the ciphertext c_result to find the
    #    result of the PIR query at the query_col th column
    ########################################################################
    log_debug('8. Let\'s calculate the decryption of the ciphertext c_result')                 
    m1 = regev.calculate_decryption(s, c_result)

    log_debug(f'm1: {m1}\n') 

    ########################################################################
    # 9. Scale the result by p / mod
    ########################################################################
    log_debug('9. Let\'s scale the result by p / mod.')
    m1_scaled = m1.calculate_scaling(regev.p, regev.mod, regev.p)

    log_debug(f'm1_scaled: {m1_scaled}\n')

    ########################################################################    
    # 10. The message vector m1_scaled should be equal to the db at the 
    # query vector query_row, query_col, showing that PIR works.
    ########################################################################
    log_debug('10. The message vector m1_scaled should be equal to the db at ' +
               'the query vector query_row, query_col, showing that PIR works.')  

    log_debug(f'db.get_query_element({query_row}, {query_col}): {db.get_query_element(query_row, query_col)}') 
    log_debug(f'm1_scaled.get_query_element({query_row}, 0): {m1_scaled.get_query_element(query_row, 0)}\n')            

    correct_retrieval = m1_scaled.get_query_element(query_row, 0) == \
                        scaled_db.get_query_element(query_row, query_col)

    log_info(f'Are they the same? Did we get a correct retrieval? {correct_retrieval}\n')
