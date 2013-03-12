from itertools import islice
import logging
from random import Random

def default_min_value(data_type):
    '''Return the minimum value for the supplied data type.

    @param data_type: int|float
        The data type.'''

    if data_type is int:
        return 0
    elif data_type is float:
        return 0.0

    raise Exception('Invalid data_type: %s' % data_type)

def default_max_value(data_type):
    '''Return the minimum value for the supplied data type.

    @param data_type: int|float
        The data type.'''

    if data_type is int:
        return 99
    elif data_type is float:
        return 1.0

    raise Exception('Invalid data_type: %s' % data_type)

def generate(num_rows, num_cols, 
        seed=None, 
        data_type=int,
        min_value=None,
        max_value=None,
        page_size=None, 
        page=None):
    '''Generate a block of random data, optionally returning just a page of it.

    @param num_rows: int
        The number of rows in the random block of data.
    @param num_cols: int
        The number of columns in the random block of data.
    @param seed: int
        The seed to use in initializing the randomizer.
    @param data_type: int|float
        The data type of the returned data.
    @param min_value: number
        The minimum value the data can take.
    @param max_value: number
        The maximum value the data can take.
    @param page_size: int
        The number of elements to return in a page.
    @param page: int
        The page to return.'''

    # Validate the data type
    if data_type not in (int, float):
        raise Exception('Invalid data_type: %s' % data_type)

    # Create the randomizer, with the seed
    random = Random(seed)

    # Establish the min and max requested values, which is dependent on the 
    # data type if we are pulling in defaults
    if min_value is None:
        min_value = default_min_value(data_type)

    if max_value is None:
        max_value = default_max_value(data_type)

    # Create the function that will generate the random data, which is 
    # dependent on the data type and min/max values
    if data_type is int:
        random_fn = lambda : random.randint(int(min_value), int(max_value))
    elif data_type is float:
        random_fn = lambda : random.uniform(min_value, max_value)

    logging.debug('Rows: %d', num_rows)
    logging.debug('Columns: %d', num_cols)
    logging.debug('Seed: %s', seed)
    logging.debug('Data type: %s', data_type)
    logging.debug('Minimum value: %s', min_value)
    logging.debug('Maximum value: %s', max_value)
    logging.debug('Page size: %s', page_size)
    logging.debug('Page number: %s', page)

    # Create the generator over all of the rows
    rows = (tuple(random_fn() for _ in xrange(num_cols)) 
            for _ in xrange(num_rows))

    if page_size is not None or page is not None:
        # A specific page was requested. Slice the generator that creates all
        # of the rows.
        
        # First, check the page parameters for missing values, and supply the 
        # defaults when necessary.
        if page_size is None or page_size < 1:
            page_size = 10
        if page is None or page < 1:
            page = 1

        # Compute the number of pages
        num_pages = (num_rows + page_size - 1) / page_size

        # Clamp the page number to the total number of pages
        page = min(page, num_pages)

        # Slice out the requested page
        start = (page - 1) * page_size
        stop = start + page_size

        rows = islice(rows, start, stop)

    for row in rows:
        yield row
